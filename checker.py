import csv
import sys
def analyze_csv(file):
    reader = csv.DictReader(file, strict=True)
    columns = reader.fieldnames

    if not columns:
        raise ValueError("CSV file is empty; no header found.")

    if any(not column.strip() for column in columns):
        raise ValueError("CSV column names cannot be blank.")

    if len(columns) != len(set(columns)):
        raise ValueError("CSV column names must be unique.")

    blank_counts = {column: 0 for column in columns}
    seen_rows = set()
    duplicate_count = 0
    row_count = 0

    for row in reader:
        if None in row:
            raise ValueError(
                f"CSV row ending at line {reader.line_num} "
                "has more values than the header."
            )

        row_count += 1
        row_values = tuple(row[column] for column in columns)

        if row_values in seen_rows:
            duplicate_count += 1
        else:
            seen_rows.add(row_values)

        for column in columns:
            value = row[column]
            if value is None or value.strip() == "":
                blank_counts[column] += 1

    return {
        "row_count": row_count,
        "column_count": len(columns),
        "columns": columns,
        "blank_counts": blank_counts,
        "duplicate_count": duplicate_count,
    }


def check_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as file:
        report = analyze_csv(file)

    return report["blank_counts"], report["duplicate_count"]
def main():
    if len(sys.argv) < 2:
        print("Usage: python checker.py <filename.csv>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        blank_counts, duplicate_count = check_csv(filename)

    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)

    except (ValueError, csv.Error) as error:
        print(f"Error: {error}")
        sys.exit(1)

    for column, count in blank_counts.items():
        print(f"{column}: {count}")

    print(f"Duplicate rows: {duplicate_count}")

if __name__ == "__main__":
    main()