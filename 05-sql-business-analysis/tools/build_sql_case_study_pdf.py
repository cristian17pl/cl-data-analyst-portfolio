from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUTPUT = ROOT / "reports" / "olist-sql-business-analysis.pdf"
PAGE_W, PAGE_H = 1600, 900

NAVY = colors.HexColor("#0A1628")
PANEL = colors.HexColor("#0E2841")
PANEL_ALT = colors.HexColor("#143451")
BORDER = colors.HexColor("#29445F")
GOLD = colors.HexColor("#C8A84B")
BLUE = colors.HexColor("#1E90FF")
TEAL = colors.HexColor("#3DBA7E")
RED = colors.HexColor("#F04444")
WHITE = colors.white
MUTED = colors.HexColor("#B3C7D9")


def wrap(text: str, width: float, font: str, size: float) -> list[str]:
    lines, current = [], ""
    for word in str(text).split():
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


def text(pdf, value, x, y, width, size=12, leading=16, color=MUTED, bold=False):
    font = "Helvetica-Bold" if bold else "Helvetica"
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for line in wrap(value, width, font, size):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def panel(pdf, x, y, w, h, fill=PANEL):
    pdf.setFillColor(fill)
    pdf.roundRect(x, y, w, h, 10, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, h, 10, fill=0, stroke=1)


def shell(pdf, title, subtitle, page, total):
    pdf.setPageSize((PAGE_W, PAGE_H))
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
    pdf.drawString(30, 27, "OLIST E-COMMERCE - SQL BUSINESS ANALYSIS")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_W / 2, 27, "PostgreSQL-compatible analysis - validated results - business recommendations")
    pdf.drawRightString(PAGE_W - 30, 27, f"{page}/{total}")


def metric(pdf, x, y, w, label, value, note, accent=GOLD):
    panel(pdf, x, y, w, 105)
    pdf.setFillColor(accent)
    pdf.rect(x, y, 6, 105, fill=1, stroke=0)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(x + 18, y + 78, label.upper())
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(x + 18, y + 43, value)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(x + 18, y + 18, note)


def bullet(pdf, value, x, y, width, accent=GOLD):
    pdf.setFillColor(accent)
    pdf.circle(x + 4, y + 4, 3, fill=1, stroke=0)
    return text(pdf, value, x + 16, y, width - 16, 12, 16, MUTED)


def table(pdf, df, x, y_top, widths, max_rows=8, row_h=34, font_size=9):
    pdf.setFillColor(PANEL_ALT)
    pdf.rect(x, y_top - row_h, sum(widths), row_h, fill=1, stroke=0)
    cursor = x
    for col, width in zip(df.columns, widths):
        pdf.setFillColor(WHITE)
        pdf.setFont("Helvetica-Bold", font_size)
        pdf.drawString(cursor + 7, y_top - 22, str(col))
        cursor += width
    y = y_top - row_h
    for idx, (_, row) in enumerate(df.head(max_rows).iterrows()):
        pdf.setFillColor(PANEL if idx % 2 == 0 else PANEL_ALT)
        pdf.rect(x, y - row_h, sum(widths), row_h, fill=1, stroke=0)
        cursor = x
        for value, width in zip(row, widths):
            shown = "" if pd.isna(value) else str(value)
            if len(shown) > 28:
                shown = shown[:25] + "..."
            pdf.setFillColor(MUTED)
            pdf.setFont("Helvetica", font_size)
            pdf.drawString(cursor + 7, y - 22, shown)
            cursor += width
        y -= row_h
    return y


def bars(pdf, labels, values, x, y_top, width, row_h=42, accent=BLUE, value_fmt=lambda v: str(v)):
    max_value = max(values) if values else 1
    label_w = 150
    for idx, (label, value) in enumerate(zip(labels, values)):
        y = y_top - idx * row_h
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica", 10)
        pdf.drawRightString(x + label_w - 12, y + 4, str(label))
        pdf.setFillColor(PANEL_ALT)
        pdf.roundRect(x + label_w, y, width - label_w - 85, 18, 3, fill=1, stroke=0)
        pdf.setFillColor(GOLD if idx == 0 else accent)
        pdf.roundRect(x + label_w, y, max(8, (width - label_w - 85) * value / max_value), 18, 3, fill=1, stroke=0)
        pdf.setFillColor(WHITE)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x + width - 76, y + 4, value_fmt(value))


def cover(pdf, total):
    pdf.setPageSize((PAGE_W, PAGE_H))
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(0, 0, 8, PAGE_H, fill=1, stroke=0)
    pdf.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(65, 745, "POSTGRESQL / RELATIONAL ANALYTICS - PORTFOLIO PROJECT 05")
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 58)
    pdf.drawString(65, 665, "Olist E-Commerce")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 52)
    pdf.drawString(65, 605, "SQL Business Analysis")
    pdf.setStrokeColor(BORDER)
    pdf.line(65, 570, 850, 570)
    text(pdf, "Ten business questions answered across revenue, geography, products, customers, payments, delivery, reviews, sellers, retention, and basket behavior - with explicit controls for fact grain and join multiplication.", 65, 530, 780, 16, 22)
    metric(pdf, 65, 280, 300, "Delivered revenue", "R$15.42M", "item price plus freight", GOLD)
    metric(pdf, 385, 280, 300, "Orders analyzed", "96.5K", "delivered marketplace orders", BLUE)
    metric(pdf, 705, 280, 300, "SQL questions", "10", "validated result extracts", TEAL)
    panel(pdf, 1080, 250, 450, 430)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(1110, 640, "CASE-STUDY PROMISE")
    y = 600
    for value in (
        "Keep item revenue, payments, reviews, and delivery events at their correct grains.",
        "Use CTEs and window functions to make transformations reviewable.",
        "Validate nine source tables before interpreting results.",
        "Translate result tables into decisions, not just query output.",
        "Provide PostgreSQL scripts and a server-free local execution path.",
    ):
        y = bullet(pdf, value, 1110, y, 380)
        y -= 16
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(65, 45, "Cristian Perez Lagos - Data Analyst Portfolio - Project 05")
    pdf.drawRightString(PAGE_W - 35, 45, f"1/{total}")
    pdf.showPage()


def model_page(pdf, total):
    shell(pdf, "Model and Grain Controls", "The analytical model is normalized; the SQL chooses the correct fact path for each question", 2, total)
    panel(pdf, 30, 115, 930, 665)
    panel(pdf, 990, 115, 580, 665)
    nodes = {
        "CUSTOMERS": (80, 620), "ORDERS": (355, 620), "ORDER ITEMS": (650, 620),
        "PRODUCTS": (650, 410), "SELLERS": (650, 240), "PAYMENTS": (355, 410), "REVIEWS": (355, 240),
    }
    links = [("CUSTOMERS","ORDERS"),("ORDERS","ORDER ITEMS"),("ORDER ITEMS","PRODUCTS"),("ORDER ITEMS","SELLERS"),("ORDERS","PAYMENTS"),("ORDERS","REVIEWS")]
    for a,b in links:
        ax, ay = nodes[a]; bx, by = nodes[b]
        pdf.setStrokeColor(BORDER); pdf.setLineWidth(3)
        pdf.line(ax + 180, ay + 35, bx, by + 35)
    for name,(x,y) in nodes.items():
        pdf.setFillColor(PANEL_ALT); pdf.roundRect(x,y,180,70,8,fill=1,stroke=0)
        pdf.setFillColor(GOLD if name in {"ORDER ITEMS","PAYMENTS","REVIEWS"} else BLUE)
        pdf.rect(x,y,5,70,fill=1,stroke=0)
        pdf.setFillColor(WHITE); pdf.setFont("Helvetica-Bold",10); pdf.drawString(x+18,y+42,name)
        grain = {"CUSTOMERS":"customer_id","ORDERS":"order_id","ORDER ITEMS":"order + item","PRODUCTS":"product_id","SELLERS":"seller_id","PAYMENTS":"order + payment","REVIEWS":"review + order"}[name]
        pdf.setFillColor(MUTED); pdf.setFont("Helvetica",8); pdf.drawString(x+18,y+20,grain)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(1018,742,"WHY GRAIN MATTERS")
    y=700
    for value in (
        "Joining payments directly to items can multiply both revenue facts.",
        "The source contains 547 orders with multiple review rows.",
        "Seller delivery rates must be order-weighted, not item-weighted.",
        "Repeat behavior requires customer_unique_id, not order-level customer_id.",
        "Geolocation repeats ZIP prefixes and is not joined without aggregation.",
    ):
        y=bullet(pdf,value,1018,y,515); y-=18
    pdf.setFillColor(TEAL); pdf.setFont("Helvetica-Bold",12); pdf.drawString(1018,390,"VALIDATION RESULT")
    text(pdf,"1,550,922 rows loaded across nine tables. Every expected row count matched and all six tested orphan counts were zero.",1018,360,500,15,20,WHITE,True)
    pdf.showPage()


def geography_page(pdf, total):
    df = pd.read_csv(RESULTS / "01_revenue_by_state.csv")
    shell(pdf, "Revenue Concentration", "A large market with a concentrated geographic core", 3, total)
    metric(pdf,30,660,350,"Delivered revenue","R$15.42M","item revenue plus freight",GOLD)
    metric(pdf,400,660,350,"Sao Paulo share","37.4%","R$5.77M delivered revenue",BLUE)
    metric(pdf,770,660,350,"Top-five states","73.2%","share of delivered revenue",TEAL)
    metric(pdf,1140,660,350,"Top AOV","R$242.31","highest state-level AOV",GOLD)
    panel(pdf,30,115,920,510); panel(pdf,980,115,590,510)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(55,585,"TOP STATES BY DELIVERED REVENUE")
    top=df.head(8)
    bars(pdf,top.customer_state.tolist(),top.total_revenue.tolist(),60,535,840,48,BLUE,lambda v:f"R${v/1e6:.2f}M")
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(1008,585,"BUSINESS READ")
    y=545
    for value in (
        "Sao Paulo alone produces more than one-third of delivered revenue.",
        "The top five states form the natural first market for retention and service tests.",
        "Revenue concentration raises the impact of operational issues in the Southeast.",
        "Average order value varies by state, so order count and value should be managed separately.",
    ):
        y=bullet(pdf,value,1008,y,520); y-=20
    pdf.showPage()


def product_page(pdf, total):
    cats=pd.read_csv(RESULTS/"02_top_product_categories.csv").head(8)
    monthly=pd.read_csv(RESULTS/"03_monthly_revenue_by_category.csv")
    peaks=monthly.groupby("order_month",as_index=False).product_revenue.sum().sort_values("product_revenue",ascending=False).head(5)
    shell(pdf,"Product Mix and Revenue Timing","Category breadth with a visible year-end promotional peak",4,total)
    panel(pdf,30,115,900,665); panel(pdf,960,115,610,665)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(55,742,"TOP CATEGORIES BY PRODUCT REVENUE")
    bars(pdf,cats.product_category.tolist(),cats.product_revenue.tolist(),55,690,820,48,BLUE,lambda v:f"R${v/1e6:.2f}M")
    text(pdf,"The top five categories contribute 39.8% of product revenue. Health and beauty leads total revenue, while watches and gifts achieves high value with fewer units and a R$199 average item price.",55,275,820,13,18,WHITE,True)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(990,742,"STRONGEST MONTHS - TOP TEN CATEGORIES")
    peak=peaks.copy(); peak["order_month"]=peak.order_month.astype(str).str[:7]; peak["product_revenue"]=peak.product_revenue.map(lambda v:f"R${v/1000:.1f}K")
    peak.columns=["Month","Revenue"]
    table(pdf,peak,990,710,[250,280],5,46,11)
    pdf.setFillColor(TEAL); pdf.setFont("Helvetica-Bold",12); pdf.drawString(990,400,"INTERPRETATION")
    y=365
    for value in (
        "November 2017 is the strongest observed month at R$642.9K.",
        "March through May 2018 forms a sustained high-revenue period.",
        "Boundary months are partial, so the analysis avoids treating them as comparable full periods.",
        "Category mix supports differentiated pricing, inventory, and campaign strategies.",
    ):
        y=bullet(pdf,value,990,y,525); y-=18
    pdf.showPage()


def experience_page(pdf,total):
    delivery=pd.read_csv(RESULTS/"05_delivery_performance_by_state.csv")
    shell(pdf,"Delivery Reliability Drives Experience","Late orders show a severe shift toward low review scores",5,total)
    metric(pdf,30,660,350,"Late-order rating","2.57","average review score",RED)
    metric(pdf,400,660,350,"On-time rating","4.29","average review score",TEAL)
    metric(pdf,770,660,350,"Late one-star share","46.1%","versus 6.6% on time",RED)
    metric(pdf,1140,660,350,"Worst state late rate","23.9%","Alagoas; 397 orders",GOLD)
    panel(pdf,30,115,760,510); panel(pdf,820,115,750,510)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(55,585,"HIGHEST LATE-DELIVERY RATES")
    worst=delivery.head(8)
    bars(pdf,worst.customer_state.tolist(),worst.late_delivery_rate_pct.tolist(),55,535,680,47,RED,lambda v:f"{v:.1f}%")
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(850,585,"DECISION")
    text(pdf,"Prioritize carrier, route, and promise-date diagnostics in AL, MA, PI, CE, and SE. Use PR, MG, and SP as higher-scale operating benchmarks, where observed late rates remain near 5-6%.",850,545,660,15,21,WHITE,True)
    y=400
    for value in (
        "The relationship is associative, not a causal experiment.",
        "The magnitude still makes delivery reliability a high-confidence experience lever.",
        "Review analysis first collapses multiple review rows to the order grain.",
        "Track both late rate and total delivery days; they answer different operational questions.",
    ):
        y=bullet(pdf,value,850,y,660); y-=18
    pdf.showPage()


def commercial_page(pdf,total):
    payment=pd.read_csv(RESULTS/"06_payment_method_mix.csv")
    repeat=pd.read_csv(RESULTS/"09_repeat_customer_revenue.csv")
    shell(pdf,"Commercial Levers","Payment dependence and a large second-purchase opportunity",6,total)
    panel(pdf,30,115,750,665); panel(pdf,810,115,760,665)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(55,742,"PAYMENT VALUE MIX")
    bars(pdf,payment.payment_type.tolist(),payment.payment_value_share_pct.tolist(),55,680,680,70,BLUE,lambda v:f"{v:.2f}%")
    text(pdf,"Credit cards contribute 78.46% of delivered-order payment value and average 3.5 installments. Authorization, installment cost, and credit-card conversion are material commercial dependencies.",55,345,670,14,20,WHITE,True)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(838,742,"CUSTOMER REVENUE MIX")
    metric(pdf,838,585,330,"One-time revenue","94.4%","R$14.56M",GOLD)
    metric(pdf,1188,585,330,"Repeat revenue","5.6%","R$864.2K",BLUE)
    metric(pdf,838,450,330,"One-time avg LTV","R$160.73","90,557 customers",GOLD)
    metric(pdf,1188,450,330,"Repeat avg LTV","R$308.53","2,801 customers",TEAL)
    pdf.setFillColor(TEAL); pdf.setFont("Helvetica-Bold",12); pdf.drawString(838,390,"RECOMMENDED TEST")
    text(pdf,"Build a second-purchase lifecycle test after delivery: category-aware recommendations, timed incentive, and service recovery for delayed first orders. Measure incremental second-order conversion and contribution margin.",838,355,670,15,21,WHITE,True)
    pdf.showPage()


def architecture_page(pdf,total):
    shell(pdf,"SQL Architecture and Delivery","The project demonstrates controlled analysis, not isolated syntax exercises",7,total)
    panel(pdf,30,115,760,665); panel(pdf,820,115,750,665)
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(55,742,"PATTERNS USED")
    patterns=(
        ("CTEs","Reusable category, review, seller-order, customer, and basket layers."),
        ("Window functions","Running category revenue and payment/revenue shares."),
        ("Filtered aggregates","Late-delivery rates with explicit eligible denominators."),
        ("Grain bridges","Order-level review and seller-order metrics before aggregation."),
        ("Self-joins","Distinct order-category pairs without symmetric duplicates."),
        ("Identity design","customer_unique_id for person-level repeat behavior."),
    )
    y=690
    for label,desc in patterns:
        pdf.setFillColor(PANEL_ALT); pdf.roundRect(55,y-48,690,62,7,fill=1,stroke=0)
        pdf.setFillColor(BLUE); pdf.setFont("Helvetica-Bold",10); pdf.drawString(72,y-13,label.upper())
        text(pdf,desc,200,y-13,520,10.5,14,MUTED)
        y-=82
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(848,742,"DELIVERY CONTRACT")
    y=700
    for value in (
        "PostgreSQL DDL, indexes, CSV load commands, and validation SQL.",
        "Ten numbered business queries with matching result extracts.",
        "DuckDB runner for server-free reproduction and automated row checks.",
        "Findings document with exact metrics, implications, and limitations.",
        "ERD and modeling notes explaining fact paths and cardinality risks.",
        "Executive PDF that communicates the analysis without requiring database access.",
    ):
        y=bullet(pdf,value,848,y,650,TEAL); y-=20
    pdf.setFillColor(GOLD); pdf.setFont("Helvetica-Bold",12); pdf.drawString(848,340,"PORTFOLIO SIGNAL")
    text(pdf,"A reviewer can inspect the SQL, rerun the project, reconcile every headline number to a CSV, and understand why each join is safe. That combination is the core analytics-engineering value of the case study.",848,305,650,15,21,WHITE,True)
    pdf.showPage()


def main():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    total=7
    pdf=canvas.Canvas(str(OUTPUT),pagesize=(PAGE_W,PAGE_H),pageCompression=1)
    pdf.setTitle("Olist E-Commerce SQL Business Analysis")
    pdf.setAuthor("Cristian Perez Lagos")
    pdf.setSubject("PostgreSQL-compatible e-commerce business analysis")
    cover(pdf,total)
    model_page(pdf,total)
    geography_page(pdf,total)
    product_page(pdf,total)
    experience_page(pdf,total)
    commercial_page(pdf,total)
    architecture_page(pdf,total)
    pdf.save()


if __name__ == "__main__":
    main()
