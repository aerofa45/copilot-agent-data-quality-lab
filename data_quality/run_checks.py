from pathlib import Path
import json
import pandas as pd
from .quality import normalize_customers, quality_report

BASE = Path(__file__).resolve().parents[1]
raw_path = BASE / "data" / "customers_dirty.csv"
clean_path = BASE / "data" / "customers_clean.csv"
report_path = BASE / "reports" / "data_quality_report.json"

df = pd.read_csv(raw_path)
clean = normalize_customers(df)
report = quality_report(df)

valid_email = clean["email"].str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
usable = clean[valid_email].drop_duplicates(
    subset=["name", "email", "device_id"], keep="first"
)

usable.to_csv(clean_path, index=False)
report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("Data quality checks complete.")
print(json.dumps(report, indent=2))
print(f"Clean file: {clean_path}")
print(f"Report: {report_path}")
