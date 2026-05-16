import hashlib
import os
import re
import secrets
import sqlite3
import time
import json

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import math


app = Flask(__name__)

# ─── 반드시 Render 환경변수에서만 설정 — 코드에 기본값 없음 ───
_secret = os.environ.get("SECRET_KEY")
_pw = os.environ.get("APP_PASSWORD")
if not _secret or not _pw:
    raise RuntimeError("SECRET_KEY 와 APP_PASSWORD 환경변수를 Render에서 설정하세요.")

app.secret_key = _secret

cookie_secure_env = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() in {"1", "true", "yes", "on"}

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=cookie_secure_env,
)

# 비밀번호를 해시로만 보관 (평문 메모리 상주 방지)
PW_HASH = hashlib.sha256(_pw.encode()).hexdigest()
del _pw  # 평문 즉시 제거

# ─── 브루트포스 방지: IP별 실패 횟수 추적 ───
_fail: dict = {}  # {ip: (count, last_time)}
MAX_FAIL = 5
LOCKOUT = 300  # 5분

# ─── DB 경로 ───
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "diary.db"))

VALID_YEAR_MONTH = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")
KOREAN_YEAR_MONTH = re.compile(r"^(\d{4})\s*년\s*(\d{1,2})\s*월$")


def error_response(error: str, status: int = 400, *, code: str | None = None):
    payload = {"error": error, "code": code or error}
    return jsonify(payload), status


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def normalize_input_date(value: str, *, allow_korean: bool = False):
    """Normalize year-month input; optionally accepts Korean legacy format."""
    if value is None:
        return None
    if not isinstance(value, str):
        return None

    value = value.strip()
    if not value:
        return None

    if VALID_YEAR_MONTH.fullmatch(value):
        return value

    if allow_korean:
        match = KOREAN_YEAR_MONTH.fullmatch(value)
        if match:
            year = match.group(1)
            month = int(match.group(2))
            if 1 <= month <= 12:
                return f"{year}-{month:02d}"

    return None


def get_csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def require_csrf():
    expected = session.get("csrf_token")
    provided = request.headers.get("X-CSRF-Token")
    if not expected or not provided or not secrets.compare_digest(str(provided), str(expected)):
        return error_response("csrf validation failed", 403, code="csrf_failed")
    return None


def validate_text_field(value, field_name: str, *, max_length: int = 5000, default: str = ""):
    if value is None:
        return default, None
    if not isinstance(value, str):
        return None, error_response(f"{field_name} must be string", 400, code=f"invalid_{field_name}")
    if len(value) > max_length:
        return None, error_response(f"{field_name} too long", 400, code=f"invalid_{field_name}")
    return value, None


def validate_entry_type(value):
    if value is None:
        return "manual", None
    if not isinstance(value, str):
        return None, error_response("invalid entry_type", 400, code="invalid_entry_type")
    normalized = value.strip().lower()
    if normalized not in {"manual", "retro"}:
        return None, error_response("invalid entry_type", 400, code="invalid_entry_type")
    return normalized, None


def validate_confidence(value):
    if value is None:
        return 1.0, None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None, error_response("invalid confidence", 400, code="invalid_confidence")
    numeric = float(value)
    if math.isfinite(numeric) is False or numeric < 0.0 or numeric > 1.0:
        return None, error_response("invalid confidence", 400, code="invalid_confidence")
    return numeric, None


def _column_names(conn, table_name: str):
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [r["name"] for r in rows]


def ensure_diary_schema():
    """Ensure diary table exists and contains migration columns."""
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        columns = _column_names(conn, "diary")

        if not columns:
            conn.execute(
                """
                CREATE TABLE diary (
                    date TEXT PRIMARY KEY,
                    f1 TEXT DEFAULT '',
                    f2 TEXT DEFAULT '',
                    f3 TEXT DEFAULT '',
                    f4 TEXT DEFAULT '',
                    entry_type TEXT DEFAULT 'manual',
                    confidence REAL DEFAULT 1.0,
                    source_note TEXT DEFAULT '',
                    created_at TEXT DEFAULT (datetime('now','localtime')),
                    updated TEXT DEFAULT (datetime('now','localtime'))
                )
                """
            )
            return

        # Add missing columns for legacy tables.
        if "entry_type" not in columns:
            conn.execute("ALTER TABLE diary ADD COLUMN entry_type TEXT DEFAULT 'manual'")
        if "confidence" not in columns:
            conn.execute("ALTER TABLE diary ADD COLUMN confidence REAL DEFAULT 1.0")
        if "source_note" not in columns:
            conn.execute("ALTER TABLE diary ADD COLUMN source_note TEXT DEFAULT ''")
        if "created_at" not in columns:
            now = int(time.time())
            conn.execute("ALTER TABLE diary ADD COLUMN created_at TEXT")
            conn.execute("UPDATE diary SET created_at = datetime(?, 'unixepoch', 'localtime')", (now,))

        # Backfill added/legacy fields for all rows.
        conn.execute(
            """
            UPDATE diary
            SET
                entry_type = COALESCE(NULLIF(entry_type, ''), 'manual'),
                confidence = COALESCE(confidence, 1.0),
                source_note = COALESCE(source_note, ''),
                created_at = COALESCE(created_at, updated, datetime('now','localtime'))
            """
        )


def normalize_existing_diary_dates():
    """Normalize legacy date formats to YYYY-MM and fill migration defaults."""
    ensure_diary_schema()
    normalized_rows = []

    def _is_empty(value):
        return value is None or value == ""

    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT rowid, date, f1, f2, f3, f4, entry_type, confidence, source_note FROM diary"
        ).fetchall()

        for row in rows:
            normalized = normalize_input_date(row["date"], allow_korean=True)
            if normalized is None:
                continue

            if normalized == row["date"]:
                continue

            existing = conn.execute(
                "SELECT rowid, f1, f2, f3, f4, entry_type, confidence, source_note, created_at, updated FROM diary WHERE date = ?",
                (normalized,),
            ).fetchone()

            if existing:
                payload = {
                    "f1": existing["f1"] if not _is_empty(existing["f1"]) else row["f1"],
                    "f2": existing["f2"] if not _is_empty(existing["f2"]) else row["f2"],
                    "f3": existing["f3"] if not _is_empty(existing["f3"]) else row["f3"],
                    "f4": existing["f4"] if not _is_empty(existing["f4"]) else row["f4"],
                    "entry_type": existing["entry_type"] if not _is_empty(existing["entry_type"]) else row["entry_type"],
                    "confidence": existing["confidence"] if existing["confidence"] is not None else row["confidence"],
                    "source_note": existing["source_note"] if not _is_empty(existing["source_note"]) else row["source_note"],
                }
                conn.execute(
                    """
                    UPDATE diary
                    SET
                        f1 = ?,
                        f2 = ?,
                        f3 = ?,
                        f4 = ?,
                        entry_type = ?,
                        confidence = ?,
                        source_note = ?
                    WHERE date = ?
                    """,
                    (
                        payload["f1"],
                        payload["f2"],
                        payload["f3"],
                        payload["f4"],
                        payload["entry_type"],
                        payload["confidence"],
                        payload["source_note"],
                        normalized,
                    ),
                )
                conn.execute("DELETE FROM diary WHERE rowid = ?", (row["rowid"],))
            else:
                conn.execute(
                    "UPDATE diary SET date = ? WHERE rowid = ?",
                    (normalized, row["rowid"]),
                )

        conn.execute(
            """
            UPDATE diary
            SET
                entry_type = COALESCE(NULLIF(entry_type, ''), 'manual'),
                confidence = COALESCE(confidence, 1.0),
                source_note = COALESCE(source_note, ''),
                created_at = COALESCE(created_at, updated, datetime('now','localtime'))
            """
        )
        normalized_rows = conn.execute("SELECT * FROM diary ORDER BY date").fetchall()

    return [dict(row) for row in normalized_rows]


def init_db():
    ensure_diary_schema()
    normalize_existing_diary_dates()


def score_band_summary(score):
    try:
        numeric = float(score)
    except (TypeError, ValueError):
        return "해석 정보 없음"

    if not math.isfinite(numeric):
        return "해석 정보 없음"

    if numeric >= 70:
        return "강점 구간"
    if numeric >= 40:
        return "균형 구간"
    return "보완 구간"


def confidence_phrase(confidence):
    try:
        numeric = float(confidence)
    except (TypeError, ValueError):
        return "신뢰 정보 없음"

    if not math.isfinite(numeric):
        return "신뢰 정보 없음"

    if numeric >= 0.8:
        return "높은 신뢰"
    if numeric >= 0.5:
        return "중간 신뢰"
    return "낮은 신뢰"


def build_label_interpretation(label, score, evidence, confidence):
    label_names = {
        "job": "일/역할",
        "gui": "관계",
        "hlt": "건강",
    }
    label_name = label_names.get(label, label)
    summary = score_band_summary(score)
    trust = confidence_phrase(confidence)
    evidence_text = evidence.strip() if isinstance(evidence, str) and evidence.strip() else "기록 없음"
    return f"{label_name}: {summary} ({trust}). 근거: {evidence_text}"


def load_saju_data_rows():
    json_path = os.path.join(os.path.dirname(__file__), "saju_data.json")
    if not os.path.exists(json_path):
        return []

    try:
        with open(json_path, encoding="utf-8") as f:
            rows = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(rows, list):
        return []

    return [row for row in rows if isinstance(row, dict)]


def load_saju_data_index():
    index = {}
    for row in load_saju_data_rows():
        key = normalize_input_date(row.get("date"), allow_korean=True)
        if not key:
            continue
        index[key] = row
    return index


def build_interpretation(diary_row, saju_row):
    evidence_map = {
        "job": diary_row.get("f1", ""),
        "gui": diary_row.get("f2", ""),
        "hlt": diary_row.get("f3", ""),
    }
    confidence = diary_row.get("confidence", 1.0)

    if not isinstance(saju_row, dict):
        return {
            label: build_label_interpretation(label, None, evidence, confidence)
            for label, evidence in evidence_map.items()
        }

    return {
        label: build_label_interpretation(label, saju_row.get(label), evidence, confidence)
        for label, evidence in evidence_map.items()
    }


init_db()


# ════════════════════════════════════════
#  인증
# ════════════════════════════════════════
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    ip = request.remote_addr or "unknown"
    if request.method == "POST":
        cnt, last = _fail.get(ip, (0, 0))
        now = time.time()
        # 잠금 확인
        if cnt >= MAX_FAIL and now - last < LOCKOUT:
            remain = int(LOCKOUT - (now - last))
            return render_template("login.html", error=f"잠시 후 다시 시도하세요. ({remain}초 남음)")
        # 비밀번호 검증 (해시 비교)
        input_hash = hashlib.sha256(request.form.get("pw", "").encode()).hexdigest()
        if input_hash == PW_HASH:
            _fail.pop(ip, None)
            session.permanent = False
            session["ok"] = True
            get_csrf_token()
            return redirect(url_for("index"))
        # 실패 기록
        _fail[ip] = (cnt + 1, now)
        error = f"비밀번호가 틀렸습니다. ({cnt + 1}/{MAX_FAIL}회)"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def need_auth():
    if not session.get("ok"):
        return redirect(url_for("login"))


# ════════════════════════════════════════
#  메인 페이지
# ════════════════════════════════════════
@app.route("/")
def index():
    r = need_auth()
    if r:
        return r
    return render_template("index.html", csrf_token=get_csrf_token())


# ════════════════════════════════════════
#  API: 사주 데이터 (1979~2079)
# ════════════════════════════════════════
@app.route("/api/saju")
def saju_api():
    if not session.get("ok"):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(load_saju_data_rows())


# ════════════════════════════════════════
#  API: 일기 CRUD
# ════════════════════════════════════════
@app.route("/api/diary", methods=["GET"])
def diary_get():
    if not session.get("ok"):
        return error_response("unauthorized", 401)
    with get_db_connection() as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("SELECT * FROM diary ORDER BY date").fetchall()

    saju_index = load_saju_data_index()
    payload = []
    for row in rows:
        item = dict(row)
        saju_row = saju_index.get(item.get("date"))
        item["interpretation"] = build_interpretation(item, saju_row)
        payload.append(item)

    return jsonify(payload)


@app.route("/api/diary", methods=["POST"])
def diary_save():
    if not session.get("ok"):
        return error_response("unauthorized", 401)

    csrf_failure = require_csrf()
    if csrf_failure:
        return csrf_failure

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("invalid_payload", 400, code="invalid_payload")

    date_raw = data.get("date")
    date = normalize_input_date(date_raw)
    if not date:
        return error_response("invalid date", 400, code="invalid_date")

    f1, err = validate_text_field(data.get("f1"), "f1")
    if err:
        return err
    f2, err = validate_text_field(data.get("f2"), "f2")
    if err:
        return err
    f3, err = validate_text_field(data.get("f3"), "f3")
    if err:
        return err
    f4, err = validate_text_field(data.get("f4"), "f4")
    if err:
        return err
    source_note, err = validate_text_field(data.get("source_note"), "source_note")
    if err:
        return err

    entry_type, err = validate_entry_type(data.get("entry_type"))
    if err:
        return err

    confidence, err = validate_confidence(data.get("confidence"))
    if err:
        return err

    with get_db_connection() as c:
        c.execute(
            """
            INSERT INTO diary(date,f1,f2,f3,f4,entry_type,confidence,source_note,created_at,updated)
            VALUES(?,?,?,?,?,?,?,?,datetime('now','localtime'),datetime('now','localtime'))
            ON CONFLICT(date) DO UPDATE SET
              f1=excluded.f1, f2=excluded.f2,
              f3=excluded.f3, f4=excluded.f4,
              entry_type=excluded.entry_type,
              confidence=excluded.confidence,
              source_note=excluded.source_note,
              updated=excluded.updated
            """,
            (
                date,
                f1,
                f2,
                f3,
                f4,
                entry_type,
                confidence,
                source_note,
            ),
        )
    return jsonify({"ok": True})


@app.route("/api/diary/<date>", methods=["DELETE"])
def diary_delete(date):
    if not session.get("ok"):
        return error_response("unauthorized", 401)

    csrf_failure = require_csrf()
    if csrf_failure:
        return csrf_failure

    normalized_date = normalize_input_date(date)
    if not normalized_date:
        return error_response("invalid date", 400, code="invalid_date")

    with get_db_connection() as c:
        c.execute("DELETE FROM diary WHERE date=?", (normalized_date,))
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=False)
