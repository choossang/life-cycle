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
        self._load_app()

    def tearDown(self):
        for module_name in list(sys.modules):
            if module_name == "app" or module_name.endswith(".app"):
                if module_name in sys.modules:
                    del sys.modules[module_name]

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
