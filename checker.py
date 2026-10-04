import csv
import sys

filename = sys.argv[1]

with open(filename, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    blank_counts = {column: 0 for column in reader.fieldnames}

    for row in reader:
        for column in reader.fieldnames:
            value = row[column]
            if value is None or value.strip() == "":
                blank_counts[column] += 1

for column, count in blank_counts.items():
    print(f"{column}: {count}")