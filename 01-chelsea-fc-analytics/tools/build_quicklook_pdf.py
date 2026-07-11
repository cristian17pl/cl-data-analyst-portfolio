from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas


PAGE_SIZE = landscape((1280, 720))
NAVY = colors.HexColor("#081827")
GOLD = colors.HexColor("#C8A84B")
MUTED_BLUE = colors.HexColor("#5E87B2")
WHITE = colors.HexColor("#FFFFFF")


def parse_slide(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Slides must use the format Title=path/to/image.png")
    title, raw_path = value.split("=", 1)
    path = Path(raw_path.strip().strip('"'))
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Image not found: {path}")
    return title.strip(), path


def draw_slide(pdf: canvas.Canvas, title: str, image_path: Path, index: int, total: int) -> None:
    page_w, page_h = PAGE_SIZE
    pdf.setPageSize(PAGE_SIZE)
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    img = Image.open(image_path)
    img_w, img_h = img.size

    margin_x = 18
    margin_top = 18
    footer_h = 32
    box_w = page_w - margin_x * 2
    box_h = page_h - margin_top * 2 - footer_h
    scale = min(box_w / img_w, box_h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    x = (page_w - draw_w) / 2
    y = footer_h + margin_top + (box_h - draw_h) / 2

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)
    pdf.rect(x - 1, y - 1, draw_w + 2, draw_h + 2, fill=0, stroke=1)
    pdf.drawImage(str(image_path), x, y, draw_w, draw_h, preserveAspectRatio=True, mask="auto")

    pdf.setFillColor(MUTED_BLUE)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(margin_x, 12, "Chelsea FC Analytics Report - Quick Look")
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(page_w / 2, 12, title)
    pdf.setFillColor(MUTED_BLUE)
    pdf.drawRightString(page_w - margin_x, 12, f"{index}/{total}")
    pdf.showPage()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a quick-look PDF from Power BI screenshots.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--slide", action="append", required=True, type=parse_slide)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(str(args.output), pagesize=PAGE_SIZE)
    total = len(args.slide)
    for idx, (title, image_path) in enumerate(args.slide, start=1):
        draw_slide(pdf, title, image_path, idx, total)
    pdf.save()


if __name__ == "__main__":
    main()
