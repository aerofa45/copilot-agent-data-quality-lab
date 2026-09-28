import re
import pandas as pd

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
STATE_MAP = {"missouri": "MO", "mo": "MO"}

def normalize_customers(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["name"] = out["name"].astype(str).str.strip()
    out["email"] = out["email"].fillna("").astype(str).str.strip().str.lower()
    out["state"] = (
        out["state"].fillna("").astype(str).str.strip().str.lower()
        .map(lambda x: STATE_MAP.get(x, x.upper()))
    )
    out["device_id"] = out["device_id"].fillna("").astype(str).str.strip().str.upper()
    return out

def quality_report(df: pd.DataFrame) -> dict:
    normalized = normalize_customers(df)

    missing_email = normalized[normalized["email"].eq("")]["customer_id"].tolist()
    invalid_email = normalized[
        ~normalized["email"].eq("") &
        ~normalized["email"].map(lambda x: bool(EMAIL_RE.match(x)))
    ]["customer_id"].tolist()

    dup_mask = normalized.duplicated(subset=["name", "email", "device_id"], keep=False)
    duplicate_records = normalized.loc[dup_mask, "customer_id"].tolist()

    invalid_state = normalized[~normalized["state"].isin({"MO"})]["customer_id"].tolist()

    return {
        "row_count": int(len(normalized)),
        "missing_email_customer_ids": [int(x) for x in missing_email],
        "invalid_email_customer_ids": [int(x) for x in invalid_email],
        "possible_duplicate_customer_ids": [int(x) for x in duplicate_records],
        "invalid_state_customer_ids": [int(x) for x in invalid_state],
    }
