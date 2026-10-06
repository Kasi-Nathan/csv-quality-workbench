import csv
import io

from fastapi import FastAPI, HTTPException, UploadFile

from checker import analyze_csv


app = FastAPI(title="CSV Quality Workbench")
MAX_FILE_SIZE = 5 * 1024 * 1024


@app.post("/api/analyze")
def analyze_upload(file: UploadFile):
    contents = file.file.read(MAX_FILE_SIZE + 1)

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 5 MiB limit.",
        )

    try:
        text = contents.decode("utf-8-sig")
        report = analyze_csv(io.StringIO(text, newline=""))
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV encoded as UTF-8.",
        )
    except (ValueError, csv.Error) as error:
        raise HTTPException(status_code=400, detail=str(error))

    return report