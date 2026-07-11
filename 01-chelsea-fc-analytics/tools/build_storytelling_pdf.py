from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas


PAGE_W = 1600
PAGE_H = 900
PAGE_SIZE = (PAGE_W, PAGE_H)

NAVY = colors.HexColor("#081827")
PANEL = colors.HexColor("#0E2841")
CARD = colors.HexColor("#141E30")
GOLD = colors.HexColor("#C8A84B")
BLUE = colors.HexColor("#5E87B2")
WHITE = colors.HexColor("#FFFFFF")
MUTED = colors.HexColor("#9AB8D6")
GREEN = colors.HexColor("#59A472")
RED = colors.HexColor("#E63535")


@dataclass(frozen=True)
class StorySlide:
    title: str
    image: Path
    message: str
    readout: tuple[str, ...]
    signal: str
    filter_context: str | None = None


SLIDES = [
    StorySlide(
        title="Report Home",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-fcbd9d48-a439-4b0f-b623-b28c59c00cf7.png"),
        message="A portfolio-grade football analytics report built around performance, finance, transfers, squad cost, and player value.",
        readout=(
            "The landing page frames the project scope before the audience enters the analytical pages.",
            "Navigation is organized by the same pillars used in the storytelling: performance, finances, transfers, and squad.",
            "The headline KPIs give scale: 6 seasons, 354 matches, 38 tracked players, and GBP 1.31bn transfer spend.",
        ),
        signal="This page works as the executive entry point: clear scope, clear navigation, and immediate domain context.",
    ),
    StorySlide(
        title="Season Overview - 2024-25",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-fbf8ac1b-4761-4ffe-98b8-a2936a944a1b.png"),
        message="The 2024-25 season is the strongest BlueCo performance checkpoint: 90 PL points, a top-4 finish, and positive net P/L.",
        readout=(
            "BlueCo's 2024-25 bounce is visible across points, win rate, and goal difference.",
            "The top-right summary table turns the season filter into an executive scorecard.",
            "The competition W/D/L chart adds texture: not just how many results, but where those results came from.",
        ),
        signal="Combines KPI cards, trend comparison, and detail tables to explain a season in one scan.",
        filter_context="Filter context: BlueCo Era, Season 2024-25.",
    ),
    StorySlide(
        title="Match Performance - 2024-25",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-edd3fc57-3024-413b-ad7c-fef95217536c.png"),
        message="The headline story is not only results improved, but where the ceiling remains: Top-6 win rate still lags the bottom-half dominance.",
        readout=(
            "Goals for vs against shows the attacking jump in 2024-25.",
            "Opponent-tier segmentation exposes hidden performance quality behind the headline win rate.",
            "Venue W/D/L helps separate home, away, and neutral performance patterns.",
        ),
        signal="This page moves beyond raw win rate by stratifying opposition difficulty.",
        filter_context="Filter context: BlueCo Era, Season 2024-25.",
    ),
    StorySlide(
        title="Financial Sustainability - BlueCo Era",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-2974afa9-c047-41af-a211-a558fd02ddd7.png"),
        message="BlueCo revenue growth is real, but cost growth still pressures net profitability and wage sustainability.",
        readout=(
            "Revenue vs cost makes the profitability gap visible season by season.",
            "Revenue mix shows the structural dependence on broadcast and commercial income.",
            "Wage-to-revenue ratio creates a sustainability lens that raw wage totals cannot provide.",
        ),
        signal="Financial pages connect football operations with business performance, a key analytics portfolio differentiator.",
        filter_context="Filter context: BlueCo Era, Sustainability view.",
    ),
    StorySlide(
        title="Financial Money Flow - BlueCo Era",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-2e8f47c9-fbf6-4fbf-96fb-39dc5dbe405b.png"),
        message="The Sankey-style flow translates finance into a story: revenue enters, direct and operating costs absorb it, and the final result remains a loss.",
        readout=(
            "Revenue streams are staged into total revenue before splitting into gross profit and direct cost.",
            "The red cost flows make the largest leakage points immediately visible.",
            "The final net loss is understandable as a flow outcome, not just a card value.",
        ),
        signal="Custom HTML/DAX visual adds signature storytelling that standard Power BI visuals rarely deliver.",
        filter_context="Filter context: BlueCo Era, Money Flow view.",
    ),
    StorySlide(
        title="Transfer Activity - 2022-23",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-5385a805-dd61-4602-a28b-80a607233b4c.png"),
        message="The 2022-23 transfer cohort shows the portfolio problem clearly: high fees do not automatically become current market value.",
        readout=(
            "The scatter uses fee paid vs market value to separate creators from destroyers.",
            "Median reference lines make the quadrant reading immediate.",
            "The fee ranking ties individual names back to the portfolio risk story.",
        ),
        signal="Quadrant analysis converts a transfer list into an investment-performance map.",
        filter_context="Filter context: BlueCo Era, Season 2022-23.",
    ),
    StorySlide(
        title="Squad and Wages - 2023-24",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-fbc70fd3-8269-4f55-9085-f44ea96bdb47.png"),
        message="Wage efficiency is the warning layer: high cost per appearance identifies contracts that hurt operational flexibility.",
        readout=(
            "The wage bill trend shows payroll pressure across seasons.",
            "Cost per appearance highlights players where cost and availability are out of balance.",
            "The efficiency trend benchmark quickly shows which seasons sit above or below the 6-season average.",
        ),
        signal="Uses derived efficiency metrics instead of simply ranking wages, which makes the analysis more decision-oriented.",
        filter_context="Filter context: BlueCo Era, Season 2023-24.",
    ),
    StorySlide(
        title="Player Market Value - 2025-26",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-bd7d9931-aa5e-43a3-8425-866f1e146391.png"),
        message="Squad value is rising into 2025-26, and Palmer's climb to the No. 1 asset is the clearest individual story.",
        readout=(
            "The trajectory chart shows value momentum within the selected season.",
            "The asset ranking identifies where value is concentrated today.",
            "The ribbon visual shows player hierarchy movement over time, not only the current snapshot.",
        ),
        signal="Combines time series, ranking, and rank movement to tell both portfolio and player-level value stories.",
        filter_context="Filter context: BlueCo Era, Season 2025-26.",
    ),
    StorySlide(
        title="Player Performance - 2025-26",
        image=Path(r"C:\Users\CRISTI~1.PER\AppData\Local\Temp\codex-clipboard-54da1309-f21c-43cc-ab6a-c4c32206d9bd.png"),
        message="Palmer leads goal contributions, while the rating trend shows team quality recovering from the 2022-23 low point.",
        readout=(
            "Goals plus assists ranks attacking contribution without hiding the part-of-whole split.",
            "The rating trend gives a simple quality benchmark across seasons.",
            "The detail table keeps the page audit-friendly for player-level follow-up.",
        ),
        signal="Balances executive insight with analyst detail: chart first, evidence table second.",
        filter_context="Filter context: BlueCo Era, Season 2025-26.",
    ),
]


def draw_wrapped(pdf: canvas.Canvas, text: str, x: float, y: float, width: float, size: int, leading: int, color=WHITE, bold=False) -> float:
    font = "Helvetica-Bold" if bold else "Helvetica"
    words = text.split()
    lines: list[str] = []
    current = ""
    pdf.setFont(font, size)
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

    pdf.setFillColor(color)
    pdf.setFont(font, size)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_bullet(pdf: canvas.Canvas, text: str, x: float, y: float, width: float) -> float:
    pdf.setFillColor(GOLD)
    pdf.circle(x + 4, y + 4, 3, fill=1, stroke=0)
    return draw_wrapped(pdf, text, x + 16, y, width - 16, 13, 17, MUTED)


def draw_screenshot(pdf: canvas.Canvas, image_path: Path) -> None:
    img = Image.open(image_path)
    img_w, img_h = img.size
    x = 26
    y = 88
    box_w = 1114
    box_h = 700
    scale = min(box_w / img_w, box_h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    draw_x = x + (box_w - draw_w) / 2
    draw_y = y + (box_h - draw_h) / 2

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)
    pdf.rect(draw_x - 2, draw_y - 2, draw_w + 4, draw_h + 4, fill=0, stroke=1)
    pdf.drawImage(str(image_path), draw_x, draw_y, draw_w, draw_h, preserveAspectRatio=True, mask="auto")


def draw_story_panel(pdf: canvas.Canvas, slide: StorySlide) -> None:
    panel_x = 1168
    panel_y = 88
    panel_w = 398
    panel_h = 700

    pdf.setFillColor(PANEL)
    pdf.roundRect(panel_x, panel_y, panel_w, panel_h, 10, fill=1, stroke=0)
    pdf.setStrokeColor(colors.HexColor("#2C3B54"))
    pdf.setLineWidth(1)
    pdf.roundRect(panel_x, panel_y, panel_w, panel_h, 10, fill=0, stroke=1)

    x = panel_x + 24
    y = panel_y + panel_h - 38
    width = panel_w - 48

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "CORE MESSAGE")
    y -= 24
    y = draw_wrapped(pdf, slide.message, x, y, width, 17, 22, WHITE, bold=True)
    y -= 18

    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "WHAT TO READ")
    y -= 22
    for item in slide.readout:
        y = draw_bullet(pdf, item, x, y, width)
        y -= 11

    y -= 4
    pdf.setFillColor(GREEN)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "PORTFOLIO SIGNAL")
    y -= 22
    y = draw_wrapped(pdf, slide.signal, x, y, width, 13, 17, MUTED)

    if slide.filter_context:
        y = max(y - 26, panel_y + 56)
        pdf.setFillColor(CARD)
        pdf.roundRect(x, panel_y + 18, width, 44, 8, fill=1, stroke=0)
        pdf.setFillColor(GOLD)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x + 12, panel_y + 45, "FILTERS SHOWN")
        draw_wrapped(pdf, slide.filter_context, x + 12, panel_y + 28, width - 24, 10, 12, MUTED)


def draw_page(pdf: canvas.Canvas, slide: StorySlide, index: int, total: int) -> None:
    pdf.setPageSize(PAGE_SIZE)
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    pdf.setFillColor(PANEL)
    pdf.rect(0, PAGE_H - 74, PAGE_W, 74, fill=1, stroke=0)
    pdf.setFillColor(GOLD)
    pdf.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)
    pdf.rect(0, 0, PAGE_W, 8, fill=1, stroke=0)

    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 23)
    pdf.drawString(26, PAGE_H - 48, slide.title)

    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica", 11)
    pdf.drawRightString(PAGE_W - 28, PAGE_H - 45, "Chelsea FC Analytics Report - Storytelling Quick Look")

    draw_screenshot(pdf, slide.image)
    draw_story_panel(pdf, slide)

    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(26, 28, "Chelsea FC Analytics Report")
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_W / 2, 28, "Performance - Finances - Transfers - Squad")
    pdf.setFillColor(BLUE)
    pdf.drawRightString(PAGE_W - 28, 28, f"{index}/{total}")
    pdf.showPage()


def main() -> None:
    output = Path("01-chelsea-fc-analytics/reports/chelsea-fc-analytics-storytelling-quick-look.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    for slide in SLIDES:
        if not slide.image.exists():
            raise FileNotFoundError(slide.image)

    pdf = canvas.Canvas(str(output), pagesize=PAGE_SIZE)
    pdf.setTitle("Chelsea FC Analytics Report - Storytelling Quick Look")
    pdf.setAuthor("Cristian Perez Lagos")
    for idx, slide in enumerate(SLIDES, start=1):
        draw_page(pdf, slide, idx, len(SLIDES))
    pdf.save()


if __name__ == "__main__":
    main()
