# CSV Quality Workbench

A Python CLI and FastAPI service that reports CSV row and column
counts, blank values per column, and exact duplicate rows.

## Setup

Requires Python 3.12. Create and activate a virtual environment, then:

```bash
python -m pip install -r requirements.txt
```

## Command-line usage

```bash
python checker.py sample.csv
```

## Run the API locally

```bash
python -m uvicorn api:app --reload
```

Open http://127.0.0.1:8000/docs and upload a file using
POST /api/analyze.

Uploads must use UTF-8 encoding and be at most 5 MiB.
Empty files, blank or duplicate column names, malformed CSV syntax,
and rows with excess cells are rejected.

## Run tests

```bash
python -m unittest -v
```