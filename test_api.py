import unittest

from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


class TestCsvUpload(unittest.TestCase):
    def upload(self, contents, delimiter=None):
        data = {}
        if delimiter is not None:
            data["delimiter"] = delimiter

        return client.post(
            "/api/analyze",
            files={"file": ("test.csv", contents, "text/csv")},
            data=data,
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
            "duplicate_rows": [],
        })

    def test_blanks_and_duplicates(self):
        response = self.upload(b"name,age\nAsha,\nAsha,\nBen,31\n")

        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertEqual(report["row_count"], 3)
        self.assertEqual(report["blank_counts"], {"name": 0, "age": 2})
        self.assertEqual(report["duplicate_count"], 1)
        self.assertEqual(
            report["duplicate_rows"],
            [{"row": 2, "matches_row": 1}],
        )

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

    def test_repeated_rows_match_first_occurrence(self):
        response = self.upload(
            b"name,age\nAsha,24\nBen,31\nAsha,24\nAsha,24\n"
        )

        self.assertEqual(response.status_code, 200)
        report = response.json()

        self.assertEqual(report["duplicate_count"], 2)
        self.assertEqual(
            report["duplicate_rows"],
            [
                {"row": 3, "matches_row": 1},
                {"row": 4, "matches_row": 1},
            ],
        )

    def test_semicolon_delimiter(self):
        response = self.upload(
            b"name;age\nAsha;24\nBen;\nAsha;24\n",
            delimiter=";",
        )

        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertEqual(report["columns"], ["name", "age"])
        self.assertEqual(report["row_count"], 3)
        self.assertEqual(report["blank_counts"], {"name": 0, "age": 1})
        self.assertEqual(
            report["duplicate_rows"],
            [{"row": 3, "matches_row": 1}],
        )

    def test_tab_delimiter(self):
        response = self.upload(
            b"name\tage\nAsha\t24\nBen\t31\n",
            delimiter="\t",
        )

        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertEqual(report["columns"], ["name", "age"])
        self.assertEqual(report["row_count"], 2)

    def test_invalid_delimiter(self):
        response = self.upload(
            b"name|age\nAsha|24\n",
            delimiter="|",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Delimiter must be a comma, semicolon, or tab.",
        )