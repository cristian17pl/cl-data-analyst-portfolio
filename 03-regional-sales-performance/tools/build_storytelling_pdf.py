from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "Visuals" / "storytelling-screenshots"
OUTPUT = ROOT / "reports" / "regional-sales-performance-storytelling-quick-look.pdf"

PAGE_W = 1600
PAGE_H = 900
PAGE_SIZE = (PAGE_W, PAGE_H)

NAVY = colors.HexColor("#0A1628")
PANEL = colors.HexColor("#0E2841")
PANEL_ALT = colors.HexColor("#102D48")
BORDER = colors.HexColor("#29445F")
GOLD = colors.HexColor("#C8A84B")
BLUE = colors.HexColor("#1E90FF")
BLUE_2 = colors.HexColor("#76A8D5")
WHITE = colors.HexColor("#FFFFFF")
MUTED = colors.HexColor("#B3C7D9")
GREEN = colors.HexColor("#3DBA7E")
RED = colors.HexColor("#F04444")


@dataclass(frozen=True)
class StoryPage:
    title: str
    subtitle: str
    image: str
    signal: str
    reads: tuple[str, ...]
    design: str
    filter_context: str


STORY_PAGES = (
    StoryPage(
        title="Executive Summary",
        subtitle="One page from enterprise scale to accountable drivers",
        image="02-executive-summary.png",
        signal=(
            "2024 revenue reached $43.7M, up 38.2% versus prior year, while the page "
            "makes concentration explicit: Southwest and Bikes carry a disproportionate share."
        ),
        reads=(
            "The variance bridge decomposes the $12.1M increase by region instead of stopping at the headline change.",
            "The monthly line shows the shape behind the annual result, including mid-year and year-end peaks.",
            "The category ranking and leaders panel anchor the story in concrete names, values, and revenue shares.",
        ),
        design=(
            "Compact HTML KPI cards combine value, comparison, and status. Gold, blue, green, and red are reserved "
            "for hierarchy and decision signals rather than decoration."
        ),
        filter_context="Year 2024; all categories, regions, and channels.",
    ),
    StoryPage(
        title="Regional Performance",
        subtitle="Where revenue sits, who carries scale, and who beats plan",
        image="03-regional-performance.png",
        signal=(
            "Scale and accountability are different stories: Southwest leads revenue, Germany leads normalized "
            "attainment, and Southeast is the visible laggard at 87.0%."
        ),
        reads=(
            "The country map establishes geographic footprint without competing basemap labels.",
            "Actual versus target bars preserve absolute commercial scale and expose each regional gap.",
            "The attainment ranking normalizes performance; gold leads, red trails, and blue carries the middle ranks.",
            "The scorecard supplies exact values and the Region field needed for drillthrough.",
        ),
        design=(
            "Geography is used because location is the question. Exact numbers, absolute comparisons, and normalized "
            "rankings sit together so no single visual overclaims the story."
        ),
        filter_context="All years, categories, regions, and channels.",
    ),
    StoryPage(
        title="Product and Margin Drivers",
        subtitle="Self-service decomposition with a fixed profitability audit",
        image="07-product-margin.png",
        signal=(
            "Bikes produce $94.7M of revenue, led by Road Bikes at $43.9M, but bestseller status does not guarantee "
            "profitability: red margin values expose value-destructive SKUs."
        ),
        reads=(
            "The decomposition tree lets the reader choose the explanatory path across category, subcategory, region, product, and channel.",
            "The fixed subcategory ranking gives a fast read for viewers who do not interact with the tree.",
            "The product table closes the loop with revenue, units, and margin at SKU level.",
        ),
        design=(
            "Interactive root-cause exploration is paired with stable evidence. Rank-driven bar colors and red negative-margin "
            "font formatting direct attention without turning the whole table into a heatmap."
        ),
        filter_context="Category and Product Line filtered to Bikes; all other slicers open.",
    ),
    StoryPage(
        title="Revenue Trend and Seasonality",
        subtitle="One metric switch, three complementary time lenses",
        image="08-revenue-trend.png",
        signal=(
            "The selected units view reveals a strong mid-2024 peak and a sharp decline in the latest partial period; "
            "the supporting charts separate recurring seasonality from cumulative pace."
        ),
        reads=(
            "The field-parameter selector reuses one hero chart for revenue, margin, units, or orders.",
            "Month-by-year columns compare like months directly and disclose partial 2022 and 2025 coverage.",
            "The YTD race resets each January and shows how quickly each selected year accumulates revenue.",
        ),
        design=(
            "A disconnected field parameter resolves through a composite-key-safe bridge measure. Continuous MonthStart "
            "axes preserve chronology while the report-level en-US locale keeps month labels consistent."
        ),
        filter_context="Multiple years selected; metric set to Units Sold.",
    ),
    StoryPage(
        title="Channel Margin Story",
        subtitle="Revenue scale is separated from profit quality",
        image="09-channel-margin.png",
        signal=(
            "In 2024, Reseller generated $32.9M - 3.1 times Online revenue - but at a -2.9% margin, while Online delivered "
            "$10.8M at a 40.0% margin."
        ),
        reads=(
            "The combo chart puts revenue columns and margin-rate line in one declared volume-versus-quality decision.",
            "Category bars show exactly where reseller margin moves left of zero, led by Bikes.",
            "The normalized mix shows channel drift independently of total revenue growth.",
            "The two-row economics table makes the AOV and margin trade-off auditable.",
        ),
        design=(
            "The dual axis is deliberate because the units differ and serve one decision. Negative margin is never hidden, "
            "and the HTML cards summarize both channel engines plus their trade-off."
        ),
        filter_context="Year 2024; all products, territories, and channels.",
    ),
    StoryPage(
        title="Target Performance Scorecard",
        subtitle="Forty statuses become a prioritized action list",
        image="10-target-scorecard.png",
        signal=(
            "2025 attainment is 145.7% overall, but only 8 of 10 regions are on target. Northeast carries the largest miss, "
            "and category-level red cells reveal where intervention is needed."
        ),
        reads=(
            "The Region-by-Category matrix uses green, amber, and red as operational status, not decoration.",
            "The action table sorts dollar variance worst first so the reader moves from status to accountable gap.",
            "The top cards distinguish revenue scale, plan attainment, and breadth of regional coverage.",
        ),
        design=(
            "A virtual TREATAS relationship allows Category columns to filter target data even though fact_targets has no "
            "physical product relationship. Missing targets remain blank rather than implying zero performance."
        ),
        filter_context="Year 2025; all categories, regions, and channels.",
    ),
    StoryPage(
        title="Territory Detail - Canada",
        subtitle="The same visual grammar at a selected regional grain",
        image="06-territory-detail.png",
        signal=(
            "Canada contributes $16.4M, grows 17.1% year over year, and reaches 118.8% of target, but its 2.5% margin "
            "shows that growth and target attainment do not equal profit quality."
        ),
        reads=(
            "The monthly trajectory preserves continuity with the Executive Summary trend.",
            "Road Bikes dominate the selected territory's product mix.",
            "The Top-15 product table combines bestsellers, units, and margin for concrete follow-up.",
            "The normalized channel mix connects the territory back to the channel-margin story.",
        ),
        design=(
            "Drillthrough passes the exact dim_territory[Region] context. The destination combines scoped HTML cards, "
            "Top-N measures, a back action, and the same color semantics used across the report."
        ),
        filter_context="Drillthrough context: Canada; source filters preserved.",
    ),
)


def wrapped_lines(pdf: canvas.Canvas, text: str, width: float, font: str, size: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if pdf.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    size: float,
    leading: float,
    color=WHITE,
    bold: bool = False,
) -> float:
    font = "Helvetica-Bold" if bold else "Helvetica"
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for line in wrapped_lines(pdf, text, width, font, size):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_bullet(pdf: canvas.Canvas, text: str, x: float, y: float, width: float) -> float:
    pdf.setFillColor(GOLD)
    pdf.circle(x + 4, y + 4, 3, fill=1, stroke=0)
    return draw_wrapped(pdf, text, x + 16, y, width - 16, 12.5, 16.5, MUTED)


def draw_image_fit(
    pdf: canvas.Canvas,
    image_path: Path,
    x: float,
    y: float,
    width: float,
    height: float,
    border: bool = True,
    pad: float = 0,
) -> None:
    with Image.open(image_path) as img:
        img_w, img_h = img.size
    scale = min((width - 2 * pad) / img_w, (height - 2 * pad) / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    draw_x = x + (width - draw_w) / 2
    draw_y = y + (height - draw_h) / 2
    if border:
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.5)
        pdf.roundRect(draw_x - 3, draw_y - 3, draw_w + 6, draw_h + 6, 6, fill=0, stroke=1)
    pdf.drawImage(str(image_path), draw_x, draw_y, draw_w, draw_h, preserveAspectRatio=True, mask="auto")


def draw_shell(pdf: canvas.Canvas, title: str, subtitle: str, page_no: int, total: int) -> None:
    pdf.setPageSize(PAGE_SIZE)
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(PANEL)
    pdf.rect(0, PAGE_H - 82, PAGE_W, 82, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(0, PAGE_H - 7, PAGE_W, 7, fill=1, stroke=0)
    pdf.rect(0, 0, PAGE_W, 7, fill=1, stroke=0)

    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 23)
    pdf.drawString(28, PAGE_H - 43, title)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(28, PAGE_H - 63, subtitle)

    pdf.setFillColor(BLUE_2)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(28, 27, "REGIONAL SALES PERFORMANCE")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_W / 2, 27, "Storytelling quick look - report pages, interactions, and semantic model")
    pdf.setFillColor(BLUE_2)
    pdf.drawRightString(PAGE_W - 28, 27, f"{page_no}/{total}")


def draw_story_panel(pdf: canvas.Canvas, page: StoryPage) -> None:
    x = 1145
    y = 105
    width = 425
    height = 680
    pdf.setFillColor(PANEL)
    pdf.roundRect(x, y, width, height, 10, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x, y, width, height, 10, fill=0, stroke=1)

    tx = x + 22
    ty = y + height - 32
    tw = width - 44

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "STORY SIGNAL")
    ty -= 23
    ty = draw_wrapped(pdf, page.signal, tx, ty, tw, 15.5, 20, WHITE, True)
    ty -= 17

    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "READ")
    ty -= 22
    for item in page.reads:
        ty = draw_bullet(pdf, item, tx, ty, tw)
        ty -= 8

    ty -= 5
    pdf.setFillColor(GREEN)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "DESIGN DECISION")
    ty -= 22
    draw_wrapped(pdf, page.design, tx, ty, tw, 12, 16, MUTED)

    box_y = y + 18
    pdf.setFillColor(PANEL_ALT)
    pdf.roundRect(tx, box_y, tw, 48, 7, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(tx + 12, box_y + 31, "FILTER CONTEXT SHOWN")
    draw_wrapped(pdf, page.filter_context, tx + 12, box_y + 15, tw - 24, 9.5, 11, MUTED)


def draw_story_page(pdf: canvas.Canvas, page: StoryPage, page_no: int, total: int) -> None:
    draw_shell(pdf, page.title, page.subtitle, page_no, total)
    draw_image_fit(pdf, ASSETS / page.image, 28, 105, 1088, 680)
    draw_story_panel(pdf, page)
    pdf.showPage()


def draw_cover(pdf: canvas.Canvas, page_no: int, total: int) -> None:
    pdf.setPageSize(PAGE_SIZE)
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_image_fit(pdf, ASSETS / "01-cover.png", 0, 0, PAGE_W, PAGE_H, border=False)
    pdf.setFillColor(colors.Color(0.02, 0.06, 0.11, alpha=0.72))
    pdf.roundRect(1112, 36, 442, 82, 8, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(1134, 90, "STORYTELLING QUICK LOOK")
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(1134, 63, "Pages, interactions, and model")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9)
    pdf.drawRightString(1534, 47, f"{page_no}/{total}")
    pdf.showPage()


def draw_interactions_page(pdf: canvas.Canvas, page_no: int, total: int) -> None:
    draw_shell(
        pdf,
        "Context on Demand",
        "Report-page tooltip and Region drillthrough keep exploration inside the story",
        page_no,
        total,
    )
    pdf.setFillColor(PANEL)
    pdf.roundRect(28, 449, 1088, 336, 10, fill=1, stroke=0)
    pdf.roundRect(28, 105, 1088, 318, 10, fill=1, stroke=0)
    draw_image_fit(pdf, ASSETS / "04-tooltip-context.png", 42, 463, 1060, 306)
    draw_image_fit(pdf, ASSETS / "05-drillthrough-action.png", 42, 119, 1060, 290)

    x = 1145
    y = 105
    w = 425
    h = 680
    pdf.setFillColor(PANEL)
    pdf.roundRect(x, y, w, h, 10, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x, y, w, h, 10, fill=0, stroke=1)
    tx, ty, tw = x + 22, y + h - 32, w - 44

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "INTERACTION STORY")
    ty -= 24
    ty = draw_wrapped(
        pdf,
        "Hover answers the next question without leaving the map; drillthrough converts a selected Region into a scoped analytical page.",
        tx,
        ty,
        tw,
        15.5,
        20,
        WHITE,
        True,
    )
    ty -= 18
    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "TOOLTIP")
    ty -= 22
    for item in (
        "Canada hover context returns $16.4M revenue, 17.1% YoY growth, and a rolling 12-month mini-trend.",
        "The tooltip supplies context on demand without adding permanent chart ink to the map.",
    ):
        ty = draw_bullet(pdf, item, tx, ty, tw)
        ty -= 9
    ty -= 5
    pdf.setFillColor(GREEN)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "DRILLTHROUGH")
    ty -= 22
    for item in (
        "Select a Region data point, then use View Territory Detail.",
        "The target binding uses the exact dim_territory[Region] column and preserves compatible source filters.",
        "The destination provides a Back action to return to the analytical flow.",
    ):
        ty = draw_bullet(pdf, item, tx, ty, tw)
        ty -= 9
    pdf.showPage()


def draw_model_overview(pdf: canvas.Canvas, page_no: int, total: int) -> None:
    draw_shell(
        pdf,
        "Semantic Model Overview",
        "A dual-fact design supports sales behavior and comparable target accountability",
        page_no,
        total,
    )
    draw_image_fit(pdf, ASSETS / "12-model-overview.png", 28, 105, 1088, 680)
    x, y, w, h = 1145, 105, 425, 680
    pdf.setFillColor(PANEL)
    pdf.roundRect(x, y, w, h, 10, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x, y, w, h, 10, fill=0, stroke=1)
    tx, ty, tw = x + 22, y + h - 32, w - 44
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "MODEL STORY")
    ty -= 23
    ty = draw_wrapped(
        pdf,
        "The model separates transactional sales from monthly planning while keeping shared Date and Territory dimensions as the analytical spine.",
        tx,
        ty,
        tw,
        15.5,
        20,
        WHITE,
        True,
    )
    ty -= 18
    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "CONSTRUCTION")
    ty -= 22
    for item in (
        "fact_sales holds order-line revenue, cost, margin, quantity, customer, product, channel, territory, and date grain.",
        "fact_targets holds monthly Territory-by-Category targets and connects physically to Date and Territory.",
        "The Category target comparison uses TREATAS rather than an ambiguous physical relationship to dim_product.",
        "Metric selector is intentionally disconnected; the formulas table centralizes 81 reusable measures.",
        "Eight relationships are defined, including one inactive Customer-to-Territory path to avoid ambiguous filtering.",
    ):
        ty = draw_bullet(pdf, item, tx, ty, tw)
        ty -= 8
    pdf.showPage()


def draw_sales_star(pdf: canvas.Canvas, page_no: int, total: int) -> None:
    draw_shell(
        pdf,
        "Sales Star Schema",
        "Conformed dimensions keep business questions readable and filter propagation predictable",
        page_no,
        total,
    )
    draw_image_fit(pdf, ASSETS / "11-model-sales.png", 28, 105, 1088, 680)
    x, y, w, h = 1145, 105, 425, 680
    pdf.setFillColor(PANEL)
    pdf.roundRect(x, y, w, h, 10, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x, y, w, h, 10, fill=0, stroke=1)
    tx, ty, tw = x + 22, y + h - 32, w - 44
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(tx, ty, "WHY THIS MODEL WORKS")
    ty -= 24
    ty = draw_wrapped(
        pdf,
        "A conventional sales star makes the report easy to audit: each slicer belongs to a dimension, while calculations aggregate from one transaction fact.",
        tx,
        ty,
        tw,
        15.5,
        20,
        WHITE,
        True,
    )
    ty -= 18
    for label, body in (
        ("DATE", "Daily calendar plus MonthStart, YearMonth, English month labels, and explicit sort columns."),
        ("PRODUCT", "Category, product line, subcategory, product, price, cost, and color support mix and margin analysis."),
        ("TERRITORY", "Continent, country code, and Region support map, rankings, tooltip, and drillthrough."),
        ("CUSTOMER", "Customer and segment enable commercial-grain extension without embedding attributes in the fact."),
        ("CHANNEL", "A compact Online versus Reseller dimension powers the margin-quality narrative."),
    ):
        pdf.setFillColor(BLUE)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(tx, ty, label)
        ty -= 17
        ty = draw_wrapped(pdf, body, tx, ty, tw, 12, 16, MUTED)
        ty -= 11
    pdf.showPage()


def draw_measure_architecture(pdf: canvas.Canvas, page_no: int, total: int) -> None:
    draw_shell(
        pdf,
        "Measure Architecture",
        "Folders and prefixes turn 81 DAX measures into a maintainable analytical API",
        page_no,
        total,
    )

    pdf.setFillColor(PANEL)
    pdf.roundRect(28, 105, 420, 680, 10, fill=1, stroke=0)
    draw_image_fit(pdf, ASSETS / "13-measure-folders.png", 46, 125, 384, 640, border=False)

    pdf.setFillColor(PANEL)
    pdf.roundRect(476, 105, 1094, 680, 10, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(476, 105, 1094, 680, 10, fill=0, stroke=1)

    folders = (
        ("0_Custom_Visuals", "VIS HTML", "Rendered KPI cards, leaders, tooltip, and page-specific HTML components."),
        ("1_Sales", "$  %", "Revenue, cost, gross margin, average order value, discount, and mix."),
        ("2_Volume", "#", "Orders, order lines, units, active customers, and products sold."),
        ("3_Targets", "$  %  #", "Target revenue, comparable-period variance, attainment, and coverage."),
        ("4_Time Intelligence", "$  %  #  pp", "Prior year, YTD, YoY, rolling 12-month, and percentage-point change."),
        ("5_Channel", "$  %", "Online and Reseller revenue, margin, share, and AOV economics."),
        ("6_Rankings", "#  $  %", "Context-aware ranks and Top-N measures for readable visuals."),
        ("7_Selectors / Text Cards", "REF", "Field-parameter bridge, selected labels, leaders, and conditional colors."),
    )
    start_x = 502
    start_y = 744
    col_w = 505
    box_h = 104
    gap_x = 24
    gap_y = 14
    for i, (folder, prefix, body) in enumerate(folders):
        col = i % 2
        row = i // 2
        x = start_x + col * (col_w + gap_x)
        y = start_y - row * (box_h + gap_y) - box_h
        pdf.setFillColor(PANEL_ALT)
        pdf.roundRect(x, y, col_w, box_h, 8, fill=1, stroke=0)
        pdf.setStrokeColor(BORDER)
        pdf.roundRect(x, y, col_w, box_h, 8, fill=0, stroke=1)
        pdf.setFillColor(GOLD)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x + 16, y + box_h - 27, folder)
        pdf.setFillColor(BLUE)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawRightString(x + col_w - 16, y + box_h - 27, prefix)
        draw_wrapped(pdf, body, x + 16, y + box_h - 53, col_w - 32, 11.5, 15, MUTED)

    dax_y = 125
    dax_h = 140
    pdf.setFillColor(PANEL_ALT)
    pdf.roundRect(502, dax_y, 1035, dax_h, 8, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(502, dax_y, 1035, dax_h, 8, fill=0, stroke=1)
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(518, dax_y + dax_h - 24, "DAX PATTERNS USED")

    dax_patterns = (
        (
            "FILTER CONTEXT",
            "CALCULATE drives channel, prior-period, and scoped KPI logic; REMOVEFILTERS, KEEPFILTERS, ALL, and ALLSELECTED control comparison denominators and visible context.",
        ),
        (
            "TIME + VIRTUAL RELATIONSHIPS",
            "SAMEPERIODLASTYEAR, TOTALYTD, and EDATE create prior-year, cumulative, and rolling windows; TREATAS bridges Product Category to the disconnected target grain.",
        ),
        (
            "RANKING + DYNAMIC OUTPUT",
            "RANKX, TOPN, and ISINSCOPE power Top-N and leader/laggard colors; SELECTEDVALUE and SWITCH resolve selectors; FORMAT supports compact KPI and HTML text.",
        ),
    )
    dax_col_w = 323
    for i, (label, body) in enumerate(dax_patterns):
        x = 518 + i * (dax_col_w + 16)
        pdf.setFillColor(BLUE)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x, dax_y + dax_h - 45, label)
        draw_wrapped(pdf, body, x, dax_y + dax_h - 64, dax_col_w, 9.7, 12.5, MUTED)

    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(
        518,
        dax_y + 10,
        "Prefix contract: $ currency | % rate/share | # count/rank | pp percentage-point change | REF helper | VIS HTML rendered custom visual",
    )
    pdf.showPage()


def main() -> None:
    required = {
        "01-cover.png",
        "02-executive-summary.png",
        "03-regional-performance.png",
        "04-tooltip-context.png",
        "05-drillthrough-action.png",
        "06-territory-detail.png",
        "07-product-margin.png",
        "08-revenue-trend.png",
        "09-channel-margin.png",
        "10-target-scorecard.png",
        "11-model-sales.png",
        "12-model-overview.png",
        "13-measure-folders.png",
    }
    missing = [name for name in sorted(required) if not (ASSETS / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing storytelling assets: {missing}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ordered_story_pages = STORY_PAGES[:2] + STORY_PAGES[-1:] + STORY_PAGES[2:-1]
    total = 1 + len(ordered_story_pages) + 1 + 3
    pdf = canvas.Canvas(str(OUTPUT), pagesize=PAGE_SIZE, pageCompression=1)
    pdf.setTitle("Regional Sales Performance - Storytelling Quick Look")
    pdf.setAuthor("Cristian Lagos")
    pdf.setSubject("Power BI page storytelling, report interactions, and semantic model architecture")

    page_no = 1
    draw_cover(pdf, page_no, total)
    for index, page in enumerate(ordered_story_pages):
        page_no += 1
        draw_story_page(pdf, page, page_no, total)
        if index == 1:
            page_no += 1
            draw_interactions_page(pdf, page_no, total)

    page_no += 1
    draw_model_overview(pdf, page_no, total)
    page_no += 1
    draw_sales_star(pdf, page_no, total)
    page_no += 1
    draw_measure_architecture(pdf, page_no, total)
    pdf.save()


if __name__ == "__main__":
    main()
