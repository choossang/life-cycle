import importlib
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("APP_PASSWORD", "test-password")


class DiarySchemaMigrationTests(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.remove(self.db_path)
        os.environ["DB_PATH"] = self.db_path

        self.saju_data_path = APP_DIR / "saju_data.json"
        self._saju_data_backup = None
        if self.saju_data_path.exists():
            self._saju_data_backup = self.saju_data_path.read_text(encoding="utf-8")
        self.saju_data_path.write_text(
            json.dumps(
                [
                    {
                        "date": "1979년 02월",
                        "job": 72,
                        "gui": 64,
                        "hlt": 58,
                    }
                ],
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        self._load_app()

    def tearDown(self):
        for module_name in list(sys.modules):
            if module_name == "app" or module_name.endswith(".app"):
                if module_name in sys.modules:
                    del sys.modules[module_name]

        if self._saju_data_backup is None:
            if self.saju_data_path.exists():
                self.saju_data_path.unlink()
        else:
            self.saju_data_path.write_text(self._saju_data_backup, encoding="utf-8")

        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    def _load_app(self):
        if "app" in sys.modules:
            self.app_module = importlib.reload(sys.modules["app"])
        else:
            self.app_module = importlib.import_module("app")
        self.app_module.init_db()
        self.app = self.app_module.app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def _login(self):
        return self.client.post("/login", data={"pw": "test-password"}, follow_redirects=True)

    def _csrf_header(self):
        with self.client.session_transaction() as sess:
            token = sess.get("csrf_token")
        return {"X-CSRF-Token": token} if token else {}

    def _setup_legacy_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DROP TABLE IF EXISTS diary")
            conn.execute(
                """
                CREATE TABLE diary (
                    date TEXT PRIMARY KEY,
                    f1 TEXT DEFAULT '',
                    f2 TEXT DEFAULT '',
                    f3 TEXT DEFAULT '',
                    f4 TEXT DEFAULT '',
                    updated TEXT
                )
                """
            )
            conn.execute(
                "INSERT INTO diary (date, f1, f2, f3, f4, updated) VALUES (?,?,?,?,?,?)",
                (
                    "1979년 02월",
                    "legacy",
                    "legacy2",
                    "legacy3",
                    "legacy4",
                    "2026-01-01T00:00:00",
                ),
            )

    def _setup_legacy_db_with_collision(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DROP TABLE IF EXISTS diary")
            conn.execute(
                """
                CREATE TABLE diary (
                    date TEXT PRIMARY KEY,
                    f1 TEXT DEFAULT '',
                    f2 TEXT DEFAULT '',
                    f3 TEXT DEFAULT '',
                    f4 TEXT DEFAULT '',
                    updated TEXT
                )
                """
            )
            conn.execute(
                "INSERT INTO diary (date, f1, f2, f3, f4, updated) VALUES (?,?,?,?,?,?)",
                (
                    "1979-02",
                    "normalized",
                    None,
                    "normalized3",
                    None,
                    "2026-01-01T00:00:00",
                ),
            )
            conn.execute(
                "INSERT INTO diary (date, f1, f2, f3, f4, updated) VALUES (?,?,?,?,?,?)",
                (
                    "1979년 02월",
                    None,
                    "legacy2",
                    None,
                    "legacy4",
                    "2026-01-01T00:00:00",
                ),
            )

    def test_schema_has_new_columns(self):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("PRAGMA table_info(diary)").fetchall()

        required = {
            "date",
            "f1",
            "f2",
            "f3",
            "f4",
            "entry_type",
            "confidence",
            "source_note",
            "created_at",
            "updated",
        }
        self.assertTrue(required.issubset({row[1] for row in rows}))

    def test_reject_invalid_korean_year_month_date(self):
        self._login()
        response = self.client.post(
            "/api/diary",
            json={"date": "1979년 02월", "f1": "text"},
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_date")
        self.assertIn("error", body)

    def test_reject_non_string_date(self):
        self._login()
        response = self.client.post(
            "/api/diary",
            json={"date": 202601, "f1": "text"},
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_date")
        self.assertIn("error", body)

    def test_legacy_dates_are_normalized_on_init(self):
        self._setup_legacy_db()
        self._load_app()
        self._login()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT date, entry_type, confidence, source_note, created_at FROM diary"
            ).fetchall()

        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["date"], "1979-02")
        self.assertEqual(row["entry_type"], "manual")
        self.assertEqual(row["confidence"], 1.0)
        self.assertEqual(row["source_note"], "")

        normalized_rows = self.app_module.normalize_existing_diary_dates()
        self.assertEqual(len(normalized_rows), 1)
        self.assertEqual(normalized_rows[0]["date"], "1979-02")

    def test_normalized_and_legacy_rows_merge_without_data_loss(self):
        self._setup_legacy_db_with_collision()
        self._load_app()
        self._login()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        rows = self.app_module.normalize_existing_diary_dates()
        self.assertEqual(len(rows), 1)

        row = rows[0]
        self.assertEqual(row["date"], "1979-02")
        self.assertEqual(row["f1"], "normalized")
        self.assertEqual(row["f2"], "legacy2")
        self.assertEqual(row["f3"], "normalized3")
        self.assertEqual(row["f4"], "legacy4")

    def test_diary_post_requires_csrf(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            json={"date": "2026-01", "f1": "text"},
        )

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body.get("code"), "csrf_failed")
        self.assertIn("error", body)

    def test_diary_post_persists_metadata_fields(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            json={
                "date": "2026-01",
                "f1": "a",
                "f2": "b",
                "f3": "c",
                "f4": "d",
                "entry_type": "retro",
                "confidence": 0.4,
                "source_note": "imported from notes",
            },
            headers=self._csrf_header(),
        )
        self.assertEqual(response.status_code, 200)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT entry_type, confidence, source_note FROM diary WHERE date = ?",
                ("2026-01",),
            ).fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["entry_type"], "retro")
        self.assertAlmostEqual(row["confidence"], 0.4)
        self.assertEqual(row["source_note"], "imported from notes")

    def test_diary_delete_requires_csrf(self):
        self._login()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO diary (date, f1, f2, f3, f4, entry_type, confidence, source_note, created_at, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'), datetime('now','localtime'))",
                ("2026-01", "a", "b", "c", "d", "manual", 1.0, ""),
            )

        response = self.client.delete("/api/diary/2026-01")

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body.get("code"), "csrf_failed")
        self.assertIn("error", body)

    def test_diary_delete_with_valid_csrf_removes_row(self):
        self._login()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO diary (date, f1, f2, f3, f4, entry_type, confidence, source_note, created_at, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'), datetime('now','localtime'))",
                ("2026-01", "a", "b", "c", "d", "manual", 1.0, ""),
            )

        response = self.client.delete(
            "/api/diary/2026-01",
            headers=self._csrf_header(),
        )

        self.assertEqual(response.status_code, 200)

        with sqlite3.connect(self.db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM diary WHERE date = ?", ("2026-01",)).fetchone()[0]

        self.assertEqual(count, 0)

    def test_diary_post_rejects_invalid_payload_shape(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            data=json.dumps([1, 2, 3]),
            content_type="application/json",
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_payload")
        self.assertIn("error", body)

    def test_diary_post_rejects_non_string_f1(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            json={"date": "2026-01", "f1": 123},
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_f1")
        self.assertIn("error", body)

    def test_diary_post_rejects_invalid_confidence(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            json={"date": "2026-01", "f1": "text", "confidence": 3},
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_confidence")
        self.assertIn("error", body)

    def test_diary_post_rejects_invalid_confidence_non_finite(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            json={"date": "2026-01", "f1": "text", "confidence": float('nan')},
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_confidence")
        self.assertIn("error", body)

    def test_diary_post_rejects_invalid_confidence_inf(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            json={"date": "2026-01", "f1": "text", "confidence": float('inf')},
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_confidence")
        self.assertIn("error", body)

    def test_diary_post_rejects_invalid_entry_type(self):
        self._login()

        response = self.client.post(
            "/api/diary",
            json={"date": "2026-01", "f1": "text", "entry_type": "invalid"},
            headers=self._csrf_header(),
        )

        body = response.get_json() or {}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body.get("code"), "invalid_entry_type")
        self.assertIn("error", body)

    def test_diary_get_includes_interpretation_with_evidence_text(self):
        self._login()

        save_response = self.client.post(
            "/api/diary",
            json={
                "date": "1979-02",
                "f1": "새로운 역할 제안을 받았다",
                "f2": "협업이 안정적이었다",
                "f3": "체력 관리를 시작했다",
                "f4": "감정 기복이 줄었다",
            },
            headers=self._csrf_header(),
        )
        self.assertEqual(save_response.status_code, 200)

        response = self.client.get("/api/diary")
        self.assertEqual(response.status_code, 200)

        rows = response.get_json() or []
        self.assertEqual(len(rows), 1)

        interpretation = rows[0].get("interpretation")
        self.assertIsInstance(interpretation, dict)
        self.assertIn("job", interpretation)
        self.assertIn("gui", interpretation)
        self.assertIn("hlt", interpretation)
        self.assertIn("새로운 역할 제안을 받았다", interpretation["job"])

    def test_saju_api_remains_raw_scores_without_interpretation(self):
        self._login()

        response = self.client.get("/api/saju")
        self.assertEqual(response.status_code, 200)

        rows = response.get_json() or []
        self.assertGreater(len(rows), 0)
        self.assertIn("job", rows[0])
        self.assertIn("gui", rows[0])
        self.assertIn("hlt", rows[0])
        self.assertNotIn("interpretation", rows[0])

    def test_diary_get_returns_fallback_interpretation_when_saju_row_missing(self):
        self._login()

        save_response = self.client.post(
            "/api/diary",
            json={
                "date": "2026-01",
                "f1": "실험 메모",
                "f2": "협업 관련 기록",
                "f3": "운동을 늘렸다",
                "f4": "메모",
            },
            headers=self._csrf_header(),
        )
        self.assertEqual(save_response.status_code, 200)

        response = self.client.get("/api/diary")
        self.assertEqual(response.status_code, 200)

        rows = response.get_json() or []
        self.assertEqual(len(rows), 1)
        interpretation = rows[0].get("interpretation")
        self.assertIsInstance(interpretation, dict)
        for key in ("job", "gui", "hlt"):
            self.assertIn("해석 정보 없음", interpretation[key])

    def test_diary_get_blank_evidence_fields_fallback_to_missing_record(self):
        self._login()

        save_response = self.client.post(
            "/api/diary",
            json={
                "date": "1979-02",
                "f1": "",
                "f2": "   ",
                "f3": "\t",
                "f4": "",
            },
            headers=self._csrf_header(),
        )
        self.assertEqual(save_response.status_code, 200)

        response = self.client.get("/api/diary")
        self.assertEqual(response.status_code, 200)

        rows = response.get_json() or []
        self.assertEqual(len(rows), 1)
        interpretation = rows[0].get("interpretation")
        self.assertIn("근거: 기록 없음", interpretation["job"])
        self.assertIn("근거: 기록 없음", interpretation["gui"])
        self.assertIn("근거: 기록 없음", interpretation["hlt"])
        self.assertTrue(interpretation["job"].startswith("일/역할:"))
        self.assertTrue(interpretation["gui"].startswith("관계:"))
        self.assertTrue(interpretation["hlt"].startswith("건강:"))

    def test_diary_get_handles_malformed_saju_json_by_fallback(self):
        self.saju_data_path.write_text("{bad json", encoding="utf-8")

        self._login()

        save_response = self.client.post(
            "/api/diary",
            json={
                "date": "1979-02",
                "f1": "새로운 프로젝트를 시작했다",
                "f2": "팀원들과 합의했다",
                "f3": "컨디션이 좋다",
                "f4": "긍정적",
            },
            headers=self._csrf_header(),
        )
        self.assertEqual(save_response.status_code, 200)

        response = self.client.get("/api/diary")
        self.assertEqual(response.status_code, 200)

        rows = response.get_json() or []
        self.assertEqual(len(rows), 1)
        interpretation = rows[0].get("interpretation")
        self.assertIsInstance(interpretation, dict)
        for key in ("job", "gui", "hlt"):
            self.assertIn("해석 정보 없음", interpretation[key])
            self.assertIn("근거:", interpretation[key])

    def test_index_template_bootstraps_csrf_month_key_and_fetch_headers(self):
        self._login()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn("const csrfToken = \"", html)
        self.assertIn("function toMonthKey", html)
        self.assertIn("X-CSRF-Token", html)
        self.assertIn("/api/saju", html)
        self.assertIn("/api/diary", html)
