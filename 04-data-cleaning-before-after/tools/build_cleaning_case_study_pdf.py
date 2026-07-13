from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.clean_retail_orders import run_pipeline


OUTPUT = ROOT / "reports" / "data-cleaning-before-after-case-study.pdf"
PAGE_W, PAGE_H = 1600, 900
PAGE_SIZE = (PAGE_W, PAGE_H)

NAVY = colors.HexColor("#0A1628")
PANEL = colors.HexColor("#0E2841")
PANEL_ALT = colors.HexColor("#102D48")
BORDER = colors.HexColor("#29445F")
GOLD = colors.HexColor("#C8A84B")
BLUE = colors.HexColor("#1E90FF")
TEAL = colors.HexColor("#3DBA7E")
RED = colors.HexColor("#F04444")
WHITE = colors.white
MUTED = colors.HexColor("#B3C7D9")
INK = colors.HexColor("#091A2C")


def wrap_lines(text: str, width: float, font: str, size: float) -> list[str]:
    words = str(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    size: float = 13,
    leading: float = 17,
    color=MUTED,
    bold: bool = False,
) -> float:
    font = "Helvetica-Bold" if bold else "Helvetica"
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for line in wrap_lines(text, width, font, size):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def shell(pdf: canvas.Canvas, title: str, subtitle: str, page: int, total: int) -> None:
    pdf.setPageSize(PAGE_SIZE)
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(PANEL)
    pdf.rect(0, PAGE_H - 82, PAGE_W, 82, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(0, PAGE_H - 7, PAGE_W, 7, fill=1, stroke=0)
    pdf.rect(0, 0, PAGE_W, 7, fill=1, stroke=0)
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(30, PAGE_H - 43, title)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(30, PAGE_H - 64, subtitle)
    pdf.setFillColor(colors.HexColor("#76A8D5"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(30, 27, "DATA CLEANING: BEFORE & AFTER")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_W / 2, 27, "Reproducible pipeline - audit controls - publishable and review outputs")
    pdf.setFillColor(colors.HexColor("#76A8D5"))
    pdf.drawRightString(PAGE_W - 30, 27, f"{page}/{total}")


def panel(pdf: canvas.Canvas, x: float, y: float, w: float, h: float, fill=PANEL) -> None:
    pdf.setFillColor(fill)
    pdf.roundRect(x, y, w, h, 10, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, h, 10, fill=0, stroke=1)


def metric(pdf: canvas.Canvas, x: float, y: float, w: float, label: str, value: str, note: str, color=GOLD) -> None:
    panel(pdf, x, y, w, 105, PANEL)
    pdf.setFillColor(color)
    pdf.rect(x, y, 6, 105, fill=1, stroke=0)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(x + 18, y + 78, label.upper())
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(x + 18, y + 43, value)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(x + 18, y + 19, note)


def bullet(pdf: canvas.Canvas, text: str, x: float, y: float, width: float, color=GOLD) -> float:
    pdf.setFillColor(color)
    pdf.circle(x + 4, y + 4, 3, fill=1, stroke=0)
    return draw_text(pdf, text, x + 16, y, width - 16, 12.5, 16.5, MUTED)


def data_table(
    pdf: canvas.Canvas,
    df: pd.DataFrame,
    x: float,
    y_top: float,
    widths: list[float],
    row_h: float = 31,
    font_size: float = 9.5,
    max_rows: int = 10,
) -> float:
    columns = list(df.columns)
    pdf.setFillColor(PANEL_ALT)
    pdf.rect(x, y_top - row_h, sum(widths), row_h, fill=1, stroke=0)
    cursor = x
    for column, width in zip(columns, widths):
        pdf.setFillColor(WHITE)
        pdf.setFont("Helvetica-Bold", font_size)
        pdf.drawString(cursor + 8, y_top - 20, str(column)[:28])
        cursor += width
    y = y_top - row_h
    for index, (_, row) in enumerate(df.head(max_rows).iterrows()):
        pdf.setFillColor(PANEL if index % 2 == 0 else PANEL_ALT)
        pdf.rect(x, y - row_h, sum(widths), row_h, fill=1, stroke=0)
        cursor = x
        for value, width in zip(row.tolist(), widths):
            text = "" if pd.isna(value) else str(value)
            if len(text) > 34:
                text = text[:31] + "..."
            pdf.setFillColor(MUTED)
            pdf.setFont("Helvetica", font_size)
            pdf.drawString(cursor + 8, y - 20, text)
            cursor += width
        y -= row_h
    return y


def cover(pdf: canvas.Canvas, result: dict[str, object], page: int, total: int) -> None:
    pdf.setPageSize(PAGE_SIZE)
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(0, 0, 8, PAGE_H, fill=1, stroke=0)
    pdf.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(65, 745, "PYTHON / PANDAS - DATA QUALITY CASE STUDY")
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 58)
    pdf.drawString(65, 665, "Data Cleaning")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 52)
    pdf.drawString(65, 605, "Before & After")
    pdf.setStrokeColor(BORDER)
    pdf.line(65, 570, 770, 570)
    draw_text(
        pdf,
        "A reproducible retail-order pipeline that standardizes messy operational data, resolves duplicated business keys, calculates trusted sales fields, and separates publishable records from an auditable review queue.",
        65,
        530,
        720,
        16,
        22,
        MUTED,
    )

    clean = result["clean"]
    metrics = [
        ("RAW", str(len(result["raw"])), "source rows"),
        ("CLEAN", str(len(clean)), "unique order IDs"),
        ("VALID", str(len(result["publishable"])), "publishable rows"),
        ("REVIEW", str(len(result["review"])), "auditable exceptions"),
    ]
    for i, (label, value, note) in enumerate(metrics):
        metric(pdf, 65 + i * 250, 280, 225, label, value, note, TEAL if label == "VALID" else RED if label == "REVIEW" else GOLD)

    panel(pdf, 1100, 250, 430, 430, PANEL)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(1130, 640, "PIPELINE CONTRACT")
    y = 605
    for text in (
        "Read malformed values as text so the evidence is preserved.",
        "Apply explicit mappings and parsing rules.",
        "Prioritize trusted manual adjustments for key conflicts.",
        "Retain exceptions with row-level issue text.",
        "Write full, publishable, and review datasets separately.",
        "Validate uniqueness, schema, counts, and output artifacts.",
    ):
        y = bullet(pdf, text, 1130, y, 370)
        y -= 13
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(65, 45, "Cristian Perez Lagos - Data Analyst Portfolio - Project 04")
    pdf.drawRightString(PAGE_W - 35, 45, f"{page}/{total}")
    pdf.showPage()


def profile_page(pdf: canvas.Canvas, result: dict[str, object], page: int, total: int) -> None:
    shell(pdf, "Dirty Data Profile", "The source preserves operational messiness so every cleaning decision can be demonstrated", page, total)
    raw = result["raw"]
    issues = result["issue_summary"]
    left_x, right_x = 30, 855
    panel(pdf, left_x, 105, 795, 680)
    panel(pdf, right_x, 105, 715, 680)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(55, 748, "SOURCE PROFILE")
    profile = pd.DataFrame(
        [
            ["Rows", len(raw)],
            ["Columns", len(raw.columns)],
            ["Logical source files", raw["source_file"].nunique()],
            ["Duplicated order IDs", raw.loc[raw["order_id"].duplicated(False), "order_id"].nunique()],
            ["Blank source cells", int(raw.eq("").sum().sum())],
        ],
        columns=["Metric", "Value"],
    )
    data_table(pdf, profile, 55, 720, [520, 210], row_h=36, font_size=11, max_rows=8)
    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(55, 495, "EXAMPLES PRESERVED FOR CLEANING")
    y = 465
    for text in (
        "Dates arrive as ISO, slash-separated, and ambiguous dash-separated text.",
        "Money includes symbols, currency labels, commas, blanks, and negative values.",
        "Country, state, category, payment, shipping, and boolean labels use inconsistent variants.",
        "Business keys repeat across monthly exports and manual adjustments.",
        "Missing and invalid records remain visible rather than disappearing during import.",
    ):
        y = bullet(pdf, text, 55, y, 730)
        y -= 12

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(880, 748, "QUALITY CONTROLS TRIGGERED")
    max_records = max(issues["records"].max(), 1)
    y = 706
    for _, row in issues.head(12).iterrows():
        label = row["quality_issue"].replace("_", " ")
        value = int(row["records"])
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(880, y + 5, label)
        pdf.setFillColor(PANEL_ALT)
        pdf.roundRect(1115, y, 365, 16, 4, fill=1, stroke=0)
        pdf.setFillColor(RED)
        pdf.roundRect(1115, y, max(18, 365 * value / max_records), 16, 4, fill=1, stroke=0)
        pdf.setFillColor(WHITE)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawRightString(1525, y + 4, str(value))
        y -= 42
    pdf.showPage()


def pipeline_page(pdf: canvas.Canvas, page: int, total: int) -> None:
    shell(pdf, "Cleaning Pipeline", "Notebook for explanation; reusable script for execution; tests for contracts", page, total)
    stages = [
        ("01", "INGEST", "Read every field as text to preserve malformed source evidence."),
        ("02", "STANDARDIZE", "Normalize headers, dates, geography, categories, statuses, and booleans."),
        ("03", "ENRICH", "Parse quantity, price, and discount; calculate gross, discount, and net sales."),
        ("04", "CONTROL", "Assign all row-level issues and valid/review status."),
        ("05", "DEDUPLICATE", "Use source priority, then issue count, to keep one order record."),
        ("06", "DELIVER", "Write full, publishable, review, KPI, issue, and log outputs."),
    ]
    x, y = 55, 650
    box_w, box_h, gap = 460, 135, 35
    for i, (number, name, text) in enumerate(stages):
        col, row = i % 3, i // 3
        bx = x + col * (box_w + gap)
        by = y - row * 205
        panel(pdf, bx, by, box_w, box_h, PANEL)
        pdf.setFillColor(GOLD)
        pdf.setFont("Helvetica-Bold", 30)
        pdf.drawString(bx + 20, by + 83, number)
        pdf.setFillColor(BLUE)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(bx + 88, by + 92, name)
        draw_text(pdf, text, bx + 88, by + 67, box_w - 110, 11.5, 15, MUTED)
        if col < 2:
            pdf.setStrokeColor(BORDER)
            pdf.setLineWidth(3)
            pdf.line(bx + box_w + 8, by + box_h / 2, bx + box_w + gap - 8, by + box_h / 2)

    panel(pdf, 55, 135, 1450, 190, PANEL_ALT)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(80, 288, "ENGINEERING DECISIONS")
    decisions = (
        "Manual adjustments outrank monthly exports for conflicting order IDs.",
        "Impossible dates stay blank and flagged; the pipeline does not invent a correction.",
        "Review-worthy rows remain traceable but are excluded from the publishable output.",
        "Every transformation can be run from the CLI or demonstrated in the notebook.",
        "Built-in unit tests cover parsers, mappings, duplicate priority, status counts, and audit retention.",
    )
    for i, text in enumerate(decisions):
        col = i % 2
        row = i // 2
        bullet(pdf, text, 80 + col * 700, 248 - row * 48, 650, TEAL)
    pdf.showPage()


def before_after_page(pdf: canvas.Canvas, result: dict[str, object], page: int, total: int) -> None:
    shell(pdf, "Before and After", "The output is smaller, typed, standardized, and still auditable", page, total)
    raw = result["raw"]
    clean = result["clean"]
    metric(pdf, 30, 660, 350, "Raw rows", "63", "22 text-heavy source columns", GOLD)
    metric(pdf, 400, 660, 350, "Clean rows", "61", "one row per order ID", BLUE)
    metric(pdf, 770, 660, 350, "Publishable", "50", "81.97% valid rate", TEAL)
    metric(pdf, 1140, 660, 350, "Review queue", "11", "18.03% retained for review", RED)

    panel(pdf, 30, 105, 750, 525)
    panel(pdf, 805, 105, 765, 525)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(55, 595, "BEFORE - SOURCE VALUES")
    raw_sample = raw.loc[raw["order_id"].isin(["ORD-1002", "ORD-1007", "ORD-1018", "ORD-1023"]), [
        "order_id", "order_date", "country", "category", "quantity", "unit_price", "discount"
    ]].head(6)
    data_table(pdf, raw_sample, 55, 565, [100, 105, 105, 135, 75, 105, 80], row_h=43, font_size=9, max_rows=6)
    draw_text(
        pdf,
        "Source values retain conflicting duplicates, mixed date syntax, written quantities, currency labels, and inconsistent category or country names.",
        55,
        265,
        690,
        12,
        16,
        MUTED,
    )

    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(830, 595, "AFTER - CANONICAL VALUES")
    clean_sample = clean.loc[clean["order_id"].isin(["ORD-1002", "ORD-1007", "ORD-1018", "ORD-1023"]), [
        "order_id", "order_date", "country", "category", "quantity", "unit_price", "discount_rate", "record_quality_status"
    ]].rename(columns={"record_quality_status": "quality_status"})
    data_table(pdf, clean_sample, 830, 565, [75, 90, 85, 105, 55, 75, 85, 120], row_h=43, font_size=8.5, max_rows=6)
    draw_text(
        pdf,
        "The clean layer provides canonical labels, typed numeric fields, stable dates, one business-key record, and an explicit quality decision for downstream consumers.",
        830,
        265,
        690,
        12,
        16,
        MUTED,
    )
    pdf.showPage()


def delivery_page(pdf: canvas.Canvas, result: dict[str, object], page: int, total: int) -> None:
    shell(pdf, "Auditability and Delivery", "Cleaning is complete only when outputs, exceptions, and contracts are explicit", page, total)
    paths = result["output_paths"]
    panel(pdf, 30, 105, 735, 680)
    panel(pdf, 795, 105, 775, 680)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(55, 748, "DELIVERABLES")
    inventory = pd.DataFrame(
        [
            [name, path.relative_to(ROOT).as_posix(), path.stat().st_size]
            for name, path in paths.items()
        ],
        columns=["Artifact", "Path", "Bytes"],
    )
    data_table(pdf, inventory, 55, 720, [135, 430, 120], row_h=43, font_size=9.5, max_rows=8)
    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(55, 400, "SAFE CONSUMPTION")
    y = 370
    for text in (
        "Use retail_orders_publishable.csv for analysis that requires valid records only.",
        "Use retail_orders_review.csv as the remediation queue for data owners.",
        "Use retail_orders_clean.csv when lineage and all retained business events matter.",
        "Use quality summaries for monitoring and release evidence.",
    ):
        y = bullet(pdf, text, 55, y, 670)
        y -= 10

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(820, 748, "QUALITY GATES")
    gates = [
        ("Schema", "Required source columns must exist before transformation."),
        ("Uniqueness", "The final full output must contain one row per order ID."),
        ("Row counts", "Clean rows cannot exceed raw rows."),
        ("Statuses", "Only valid and review are permitted quality outcomes."),
        ("Separation", "Publishable and review outputs must be mutually exclusive."),
        ("Artifacts", "Every declared output must exist after a write-enabled run."),
    ]
    y = 700
    for label, text in gates:
        pdf.setFillColor(PANEL_ALT)
        pdf.roundRect(820, y - 44, 700, 58, 7, fill=1, stroke=0)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(835, y - 9, label.upper())
        draw_text(pdf, text, 950, y - 9, 540, 10.5, 14, MUTED)
        y -= 78
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(820, 190, "PORTFOLIO SIGNAL")
    draw_text(
        pdf,
        "The project demonstrates more than cleanup syntax: it shows source preservation, deterministic rules, exception management, release outputs, and automated contracts - the same controls expected in production analytics pipelines.",
        820,
        163,
        700,
        13,
        17,
        WHITE,
        True,
    )
    pdf.showPage()


def main() -> None:
    result = run_pipeline(ROOT, write_output_files=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    total = 5
    pdf = canvas.Canvas(str(OUTPUT), pagesize=PAGE_SIZE, pageCompression=1)
    pdf.setTitle("Data Cleaning: Before & After - Case Study")
    pdf.setAuthor("Cristian Perez Lagos")
    pdf.setSubject("Reproducible Python data-cleaning and data-quality case study")
    cover(pdf, result, 1, total)
    profile_page(pdf, result, 2, total)
    pipeline_page(pdf, 3, total)
    before_after_page(pdf, result, 4, total)
    delivery_page(pdf, result, 5, total)
    pdf.save()


if __name__ == "__main__":
    main()
