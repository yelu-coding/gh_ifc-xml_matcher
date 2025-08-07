import os
import csv
import json
import shutil

# === Input CSV file path (the one you manually edited) ===
INPUT_CSV_PATH = '/Users/georgylu/03_master_yelu/output/matched_results_1.csv'

# === Final output folder ===
OUTPUT_FOLDER = '/Users/georgylu/03_master_yelu/output_final'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Step 1: Copy the CSV file into the output_final folder ===
csv_filename = os.path.basename(INPUT_CSV_PATH)
final_csv_path = os.path.join(OUTPUT_FOLDER, csv_filename)
shutil.copy(INPUT_CSV_PATH, final_csv_path)
print(f"✅ CSV file copied to: {final_csv_path}")

# === Step 2: Read the CSV and generate the corresponding JSON file ===
with open(INPUT_CSV_PATH, mode='r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

# === JSON output path (same name as CSV, but with .json extension) ===
json_filename = os.path.splitext(csv_filename)[0] + '.json'
json_path = os.path.join(OUTPUT_FOLDER, json_filename)

# === Write data to JSON file ===
with open(json_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"✅ JSON file generated at: {json_path}")
