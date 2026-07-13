from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import re
import unicodedata

import pandas as pd


DEFAULT_OUTPUT_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "email",
    "country",
    "state",
    "city",
    "product_sku",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "discount_rate",
    "gross_sales",
    "discount_amount",
    "net_sales",
    "payment_method",
    "payment_status",
    "shipping_status",
    "delivery_date",
    "is_returned",
    "source_file",
    "record_quality_status",
    "quality_issues",
]

COUNTRY_MAP = {
    "usa": "United States",
    "u s": "United States",
    "united states": "United States",
    "hn": "Honduras",
    "honduras": "Honduras",
    "mexico": "Mexico",
}

STATE_MAP = {
    "california": "CA",
    "ca": "CA",
    "texas": "TX",
    "tx": "TX",
    "new york": "NY",
    "ny": "NY",
    "washington": "WA",
    "wa": "WA",
    "massachusetts": "MA",
    "ma": "MA",
    "cortes": "Cortes",
    "francisco morazan": "Francisco Morazan",
    "fm": "Francisco Morazan",
    "atlantida": "Atlantida",
    "nuevo leon": "Nuevo Leon",
    "jal": "Jalisco",
}

CATEGORY_MAP = {
    "home kitchen": "Home & Kitchen",
    "home and kitchen": "Home & Kitchen",
    "home": "Home & Kitchen",
    "electronics": "Electronics",
    "apparel": "Apparel",
    "fitness": "Fitness",
    "office": "Office Supplies",
    "office supplies": "Office Supplies",
    "furniture": "Furniture",
}

PAYMENT_METHOD_MAP = {
    "credit card": "Credit Card",
    "creditcard": "Credit Card",
    "tarjeta": "Credit Card",
    "tarjeta de credito": "Credit Card",
    "debit": "Debit Card",
    "debit card": "Debit Card",
    "paypal": "PayPal",
    "cash": "Cash",
    "cash on delivery": "Cash on Delivery",
}

STATUS_MAP = {
    "paid": "Paid",
    "pending": "Pending",
    "refunded": "Refunded",
    "delivered": "Delivered",
    "in transit": "In Transit",
    "returned": "Returned",
}

RETURN_FLAG_MAP = {
    "y": True,
    "yes": True,
    "true": True,
    "1": True,
    "n": False,
    "no": False,
    "false": False,
    "0": False,
}


def resolve_project_dir(project_folder: str = "04-data-cleaning-before-after") -> Path:
    """Locate the project from the project folder, repository root, or notebook folder."""
    candidates = [Path.cwd(), Path.cwd() / project_folder, Path.cwd().parent]
    for candidate in candidates:
        if (candidate / "raw" / "dirty_retail_orders.csv").exists():
            return candidate.resolve()
    raise FileNotFoundError("raw/dirty_retail_orders.csv was not found from the current path.")


def normalize_key(value: object) -> str:
    """Normalize accents, case, punctuation, and whitespace for mapping keys."""
    text = "" if pd.isna(value) else str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_mixed_date(value: object) -> pd.Timestamp:
    """Parse known source formats; impossible or unknown dates remain missing for audit."""
    text = "" if pd.isna(value) else str(value).strip()
    if not text:
        return pd.NaT
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%d/%m/%Y", "%m-%d-%Y"]
    for fmt in formats:
        try:
            return pd.Timestamp(datetime.strptime(text, fmt))
        except ValueError:
            continue
    return pd.NaT


def clean_money(value: object) -> object:
    """Remove currency labels and thousands separators before numeric conversion."""
    text = "" if pd.isna(value) else str(value).strip()
    if not text:
        return pd.NA
    cleaned = re.sub(r"[^0-9.\-]", "", text.replace(",", ""))
    return float(cleaned) if cleaned not in {"", "-"} else pd.NA


def clean_discount(value: object) -> object:
    """Convert percent or decimal discount text into a decimal rate."""
    text = "" if pd.isna(value) else str(value).strip()
    if not text:
        return 0.0
    has_percent = "%" in text
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    if cleaned in {"", "-"}:
        return pd.NA
    number = float(cleaned)
    return number / 100 if has_percent or abs(number) > 1 else number


def clean_quantity(value: object) -> object:
    """Convert numeric text and common written quantities to numbers."""
    text = "" if pd.isna(value) else str(value).strip().lower()
    if not text:
        return pd.NA
    text_numbers = {"one": 1, "two": 2, "three": 3}
    if text in text_numbers:
        return float(text_numbers[text])
    try:
        return float(text)
    except ValueError:
        return pd.NA


def map_value(value: object, mapping: dict[str, str], fallback: object = pd.NA) -> object:
    """Map source variants to canonical values while preserving unknown nonblank values."""
    key = normalize_key(value)
    if not key:
        return fallback
    return mapping.get(key, str(value).strip())


def load_raw_orders(path: Path) -> pd.DataFrame:
    """Read all source fields as text so malformed values remain visible for audit."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def standardize_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize headers, source priority, dates, categories, geography, and statuses."""
    standardized = df.copy()
    standardized.columns = [normalize_key(column).replace(" ", "_") for column in standardized.columns]
    standardized["source_priority"] = standardized["source_file"].map(
        lambda value: 2 if normalize_key(value) == "manual adjustment csv" else 1
    )
    standardized["order_date_clean"] = standardized["order_date"].map(parse_mixed_date)
    standardized["delivery_date_clean"] = standardized["delivery_date"].map(parse_mixed_date)
    standardized["country_clean"] = standardized["country"].map(lambda value: map_value(value, COUNTRY_MAP))
    standardized["state_clean"] = standardized["state"].map(lambda value: map_value(value, STATE_MAP))
    standardized["city_clean"] = standardized["city"].str.strip().str.title()
    standardized["category_clean"] = standardized["category"].map(lambda value: map_value(value, CATEGORY_MAP))
    standardized["payment_method_clean"] = standardized["payment_method"].map(
        lambda value: map_value(value, PAYMENT_METHOD_MAP)
    )
    standardized["payment_status_clean"] = standardized["payment_status"].map(
        lambda value: map_value(value, STATUS_MAP)
    )
    standardized["shipping_status_clean"] = standardized["shipping_status"].map(
        lambda value: map_value(value, STATUS_MAP)
    )
    standardized["is_returned"] = standardized["return_flag"].map(
        lambda value: RETURN_FLAG_MAP.get(normalize_key(value), pd.NA)
    )
    return standardized


def calculate_order_values(df: pd.DataFrame) -> pd.DataFrame:
    """Clean numeric fields and derive gross, discount, and net sales."""
    enriched = df.copy()
    enriched["quantity_clean"] = enriched["quantity"].map(clean_quantity)
    enriched["unit_price_clean"] = enriched["unit_price"].map(clean_money)
    enriched["discount_rate"] = enriched["discount"].map(clean_discount)
    enriched["gross_sales"] = enriched["quantity_clean"] * enriched["unit_price_clean"]
    enriched["discount_amount"] = enriched["gross_sales"] * enriched["discount_rate"]
    enriched["net_sales"] = enriched["gross_sales"] - enriched["discount_amount"]
    return enriched


def build_quality_issues(row: pd.Series) -> list[str]:
    """Return all audit issues detected for one staged record."""
    issues: list[str] = []
    if not str(row.get("order_id", "")).strip():
        issues.append("missing_order_id")
    if pd.isna(row.get("order_date_clean")):
        issues.append("invalid_order_date")
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", str(row.get("order_date", "")).strip()):
        issues.append("ambiguous_order_date_format")
    if not str(row.get("customer_id", "")).strip():
        issues.append("missing_customer_id")
    email = str(row.get("email", "")).strip()
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        issues.append("invalid_email")
    if not email:
        issues.append("missing_email")
    if not str(row.get("product_sku", "")).strip():
        issues.append("missing_product_sku")
    if pd.isna(row.get("category_clean")):
        issues.append("missing_category")
    if pd.isna(row.get("quantity_clean")):
        issues.append("invalid_quantity")
    elif row.get("quantity_clean") <= 0:
        issues.append("non_positive_quantity")
    if pd.isna(row.get("unit_price_clean")):
        issues.append("invalid_unit_price")
    elif row.get("unit_price_clean") < 0:
        issues.append("negative_unit_price")
    if pd.isna(row.get("discount_rate")):
        issues.append("invalid_discount")
    elif row.get("discount_rate") < 0:
        issues.append("negative_discount")
    if row.get("shipping_status_clean") == "Delivered" and pd.isna(row.get("delivery_date_clean")):
        issues.append("missing_delivery_date_for_delivered_order")
    return issues


def apply_quality_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Add issue list, count, text, and valid/review status to staged records."""
    checked = df.copy()
    checked["quality_issue_list"] = checked.apply(build_quality_issues, axis=1)
    checked["quality_issue_count"] = checked["quality_issue_list"].map(len)
    checked["quality_issues"] = checked["quality_issue_list"].map(lambda issues: " | ".join(issues))
    checked["record_quality_status"] = checked["quality_issue_count"].map(
        lambda count: "valid" if count == 0 else "review"
    )
    return checked


def resolve_duplicate_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Keep one row per order using source priority, then lowest issue count."""
    sorted_df = df.sort_values(
        by=["order_id", "source_priority", "quality_issue_count"],
        ascending=[True, False, True],
        kind="stable",
    )
    deduped = sorted_df.drop_duplicates(subset=["order_id"], keep="first").copy()
    return deduped.sort_values("order_id", kind="stable").reset_index(drop=True)


def build_clean_orders(
    df: pd.DataFrame,
    output_columns: list[str] = DEFAULT_OUTPUT_COLUMNS,
    should_resolve_duplicates: bool = True,
) -> pd.DataFrame:
    """Create the final typed and ordered clean dataset with audit columns."""
    base = resolve_duplicate_orders(df) if should_resolve_duplicates else df.copy()
    clean = pd.DataFrame(
        {
            "order_id": base["order_id"].str.strip(),
            "order_date": base["order_date_clean"].dt.strftime("%Y-%m-%d"),
            "customer_id": base["customer_id"].replace("", pd.NA),
            "customer_name": base["customer_name"].str.strip(),
            "email": base["email"].replace("", pd.NA),
            "country": base["country_clean"],
            "state": base["state_clean"],
            "city": base["city_clean"],
            "product_sku": base["product_sku"].replace("", pd.NA),
            "product_name": base["product_name"].str.strip(),
            "category": base["category_clean"],
            "quantity": base["quantity_clean"],
            "unit_price": base["unit_price_clean"],
            "discount_rate": base["discount_rate"],
            "gross_sales": base["gross_sales"],
            "discount_amount": base["discount_amount"],
            "net_sales": base["net_sales"],
            "payment_method": base["payment_method_clean"],
            "payment_status": base["payment_status_clean"],
            "shipping_status": base["shipping_status_clean"],
            "delivery_date": base["delivery_date_clean"].dt.strftime("%Y-%m-%d"),
            "is_returned": base["is_returned"],
            "source_file": base["source_file"],
            "record_quality_status": base["record_quality_status"],
            "quality_issues": base["quality_issues"],
        }
    )
    return clean[output_columns]


def build_quality_outputs(
    raw_df: pd.DataFrame,
    staged_df: pd.DataFrame,
    clean_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create before/after KPI and issue-frequency outputs."""
    valid_count = int((clean_df["record_quality_status"] == "valid").sum())
    review_count = int((clean_df["record_quality_status"] == "review").sum())
    clean_count = len(clean_df)
    quality_summary = pd.DataFrame(
        [
            {"metric": "raw_rows", "value": len(raw_df)},
            {"metric": "clean_rows", "value": clean_count},
            {"metric": "removed_duplicate_order_ids", "value": len(staged_df) - clean_count},
            {"metric": "valid_records", "value": valid_count},
            {"metric": "records_requiring_review", "value": review_count},
            {"metric": "valid_rate_pct", "value": round(100 * valid_count / clean_count, 2)},
            {"metric": "review_rate_pct", "value": round(100 * review_count / clean_count, 2)},
            {
                "metric": "valid_record_net_sales",
                "value": round(clean_df.loc[clean_df["record_quality_status"] == "valid", "net_sales"].sum(), 2),
            },
        ]
    )
    exploded = (
        staged_df[["order_id", "quality_issue_list"]]
        .explode("quality_issue_list")
        .dropna(subset=["quality_issue_list"])
        .rename(columns={"quality_issue_list": "quality_issue"})
    )
    issue_summary = (
        exploded.groupby("quality_issue", as_index=False)
        .agg(records=("order_id", "count"))
        .sort_values(["records", "quality_issue"], ascending=[False, True])
        .reset_index(drop=True)
    )
    return quality_summary, issue_summary


def validate_pipeline(raw_df: pd.DataFrame, staged_df: pd.DataFrame, clean_df: pd.DataFrame) -> None:
    """Raise an actionable error when schema, uniqueness, or row-count contracts fail."""
    required_columns = {
        "order_id",
        "order_date",
        "customer_id",
        "email",
        "country",
        "state",
        "city",
        "product_sku",
        "category",
        "quantity",
        "unit_price",
        "discount",
        "payment_method",
        "payment_status",
        "shipping_status",
        "delivery_date",
        "return_flag",
        "source_file",
    }
    missing = required_columns - set(staged_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if clean_df["order_id"].duplicated().any():
        raise ValueError("The clean dataset still contains duplicated order_id values.")
    if len(clean_df) > len(raw_df):
        raise ValueError("Clean row count cannot exceed raw row count.")
    if not set(clean_df["record_quality_status"].unique()) <= {"valid", "review"}:
        raise ValueError("Unexpected record_quality_status value found.")


def write_outputs(
    project_dir: Path,
    clean_df: pd.DataFrame,
    quality_summary: pd.DataFrame,
    issue_summary: pd.DataFrame,
    run_date: date | None = None,
) -> dict[str, Path]:
    """Write the full clean output, publishable subset, review queue, summaries, and log."""
    cleaned_dir = project_dir / "cleaned"
    docs_dir = project_dir / "docs"
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "clean": cleaned_dir / "retail_orders_clean.csv",
        "publishable": cleaned_dir / "retail_orders_publishable.csv",
        "review": cleaned_dir / "retail_orders_review.csv",
        "quality_summary": cleaned_dir / "data_quality_summary.csv",
        "quality_issues": cleaned_dir / "data_quality_issues.csv",
        "cleaning_log": docs_dir / "cleaning-log.md",
    }
    clean_df.to_csv(paths["clean"], index=False)
    clean_df.loc[clean_df["record_quality_status"] == "valid"].to_csv(paths["publishable"], index=False)
    clean_df.loc[clean_df["record_quality_status"] == "review"].to_csv(paths["review"], index=False)
    quality_summary.to_csv(paths["quality_summary"], index=False)
    issue_summary.to_csv(paths["quality_issues"], index=False)
    paths["cleaning_log"].write_text(
        "# Cleaning Log\n\n"
        f"Generated on: {run_date or date.today()}\n\n"
        "## Outputs\n\n"
        "- Full cleaned dataset with audit status: `cleaned/retail_orders_clean.csv`\n"
        "- Publishable valid records: `cleaned/retail_orders_publishable.csv`\n"
        "- Review queue: `cleaned/retail_orders_review.csv`\n"
        "- Data-quality KPI summary: `cleaned/data_quality_summary.csv`\n"
        "- Issue-frequency summary: `cleaned/data_quality_issues.csv`\n\n"
        "## Decisions\n\n"
        "- Manual adjustment rows outrank monthly export rows when an order ID conflicts.\n"
        "- Unknown or impossible dates remain blank and are flagged instead of guessed.\n"
        "- Negative quantities, prices, and discounts are retained in the review queue, not published silently.\n"
        "- Revenue is calculated from cleaned quantity, unit price, and discount rate.\n"
        "- Every output row retains source, quality status, and issue text for traceability.\n",
        encoding="utf-8",
    )
    return paths


def run_pipeline(
    project_dir: Path | None = None,
    *,
    write_output_files: bool = True,
    resolve_duplicates: bool = True,
    run_date: date | None = None,
) -> dict[str, object]:
    """Execute the complete raw-to-clean pipeline and return all analytical stages."""
    project_dir = (project_dir or resolve_project_dir()).resolve()
    raw = load_raw_orders(project_dir / "raw" / "dirty_retail_orders.csv")
    standardized = standardize_orders(raw)
    enriched = calculate_order_values(standardized)
    staged = apply_quality_rules(enriched)
    clean = build_clean_orders(staged, should_resolve_duplicates=resolve_duplicates)
    validate_pipeline(raw, staged, clean)
    quality_summary, issue_summary = build_quality_outputs(raw, staged, clean)
    paths = write_outputs(project_dir, clean, quality_summary, issue_summary, run_date) if write_output_files else {}
    return {
        "raw": raw,
        "standardized": standardized,
        "staged": staged,
        "clean": clean,
        "publishable": clean.loc[clean["record_quality_status"] == "valid"].copy(),
        "review": clean.loc[clean["record_quality_status"] == "review"].copy(),
        "quality_summary": quality_summary,
        "issue_summary": issue_summary,
        "output_paths": paths,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and audit the retail order extract.")
    parser.add_argument("--project-dir", type=Path, default=None, help="Path to 04-data-cleaning-before-after.")
    parser.add_argument("--no-write", action="store_true", help="Run validations without writing output files.")
    parser.add_argument("--keep-duplicates", action="store_true", help="Do not resolve duplicated order IDs.")
    args = parser.parse_args()
    result = run_pipeline(
        args.project_dir,
        write_output_files=not args.no_write,
        resolve_duplicates=not args.keep_duplicates,
    )
    summary = result["quality_summary"]
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
