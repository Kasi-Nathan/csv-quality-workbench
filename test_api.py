import unittest

from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


class TestCsvUpload(unittest.TestCase):
    def upload(self, contents):
        return client.post(
            "/api/analyze",
            files={"file": ("test.csv", contents, "text/csv")},
        )

    def test_clean_csv(self):
        response = self.upload(b"name,age\nAsha,24\nBen,31\n")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "row_count": 2,
            "column_count": 2,
            "columns": ["name", "age"],
            "blank_counts": {"name": 0, "age": 0},
            "duplicate_count": 0,
        })

    def test_blanks_and_duplicates(self):
        response = self.upload(b"name,age\nAsha,\nAsha,\nBen,31\n")

        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertEqual(report["row_count"], 3)
        self.assertEqual(report["blank_counts"], {"name": 0, "age": 2})
        self.assertEqual(report["duplicate_count"], 1)

    def test_empty_csv(self):
        response = self.upload(b"")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "CSV file is empty; no header found.",
        )

    def test_extra_cells(self):
        response = self.upload(b"name,age\nAsha,24,unexpected\n")

        self.assertEqual(response.status_code, 400)
        self.assertIn("more values than the header", response.json()["detail"])

    def test_invalid_encoding(self):
        response = self.upload(b"name\n\xff\n")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Please upload a CSV encoded as UTF-8.",
        )