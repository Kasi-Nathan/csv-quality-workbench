import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python checker.py <filename.csv>")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        if reader.fieldnames is None:
            print("Error: CSV file is empty; no header found.")
            sys.exit(1)

        blank_counts = {column: 0 for column in reader.fieldnames}
        seen_rows = set()
        duplicate_count = 0

        for row in reader:
            row_values = tuple(row.values())

            if row_values in seen_rows:
                duplicate_count += 1
            else:
                seen_rows.add(row_values)

            for column in reader.fieldnames:
                value = row[column]
                if value is None or value.strip() == "":
                    blank_counts[column] += 1

except FileNotFoundError:
    print(f"Error: File not found: {filename}")
    sys.exit(1)

for column, count in blank_counts.items():
    print(f"{column}: {count}")

print(f"Duplicate rows: {duplicate_count}")