# CSV Quality Workbench

A CSV quality checker with a React dashboard, FastAPI backend,
and Python command-line tool.

Upload a CSV to view row and column counts, blank values per
column, and exact duplicate rows.

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

## Run the web app locally

Requires Node.js and npm, plus the Python setup described above.

Keep two terminals running.

### Terminal 1: Backend

From the project root, with your Python virtual environment activated:

```bash
python -m uvicorn api:app --reload
```

Starts the API at http://127.0.0.1:8000.
The `--reload` option restarts it when Python files change.

### Terminal 2: Frontend

From the project root:

```bash
cd frontend
npm install
npm run dev
```

- `cd frontend` enters the frontend folder.
- `npm install` installs its dependencies.
- `npm run dev` starts the Vite development server.

Open the local URL printed by Vite, usually http://localhost:5173.

Choose a CSV file and click **Analyze**.
The dashboard displays the results or an error message.

During local development, Vite forwards `/api` requests to the backend.
Both servers must remain running.

## Frontend checks

Run these from the `frontend` folder:

```bash
npm run lint
npm run build
```

- `npm run lint` checks JavaScript and React code for common mistakes.
- `npm run build` generates production files in `dist`; it does not deploy the app.

## Run tests

```bash
python -m unittest -v
```