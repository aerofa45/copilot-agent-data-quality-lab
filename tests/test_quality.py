import pandas as pd
from pathlib import Path
from data_quality.quality import normalize_customers, quality_report

BASE = Path(__file__).resolve().parents[1]

def test_quality_report_finds_expected_issues():
    df = pd.read_csv(BASE / "data" / "customers_dirty.csv")
    report = quality_report(df)
    assert 103 in report["missing_email_customer_ids"]
    assert 105 in report["invalid_email_customer_ids"]
    assert 101 in report["possible_duplicate_customer_ids"]
    assert 104 in report["possible_duplicate_customer_ids"]

def test_normalization():
    df = pd.read_csv(BASE / "data" / "customers_dirty.csv")
    clean = normalize_customers(df)
    sarah = clean[clean["customer_id"] == 102].iloc[0]
    assert sarah["email"] == "sarah@example.com"
    assert sarah["state"] == "MO"
