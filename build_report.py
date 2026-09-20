"""
build_report.py
analysis.py çıktısındaki grafikleri ve içgörüleri kullanarak
profesyonel bir PDF rapor oluşturur.
"""
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Türkçe karakterleri destekleyen font kaydı
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFontFamily(
    "DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold",
    italic="DejaVuSans-Oblique", boldItalic="DejaVuSans-Bold"
)

with open("/home/claude/sales_project/insights.json", "r", encoding="utf-8") as f:
    insights = json.load(f)

s = insights["summary"]
CHART_DIR = "/home/claude/sales_project/charts"

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleCustom", parent=styles["Title"], fontName="DejaVuSans-Bold", textColor=colors.HexColor("#1e3a8a"))
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="DejaVuSans-Bold", textColor=colors.HexColor("#1e3a8a"), spaceBefore=14, spaceAfter=8)
body = ParagraphStyle("BodyCustom", parent=styles["Normal"], fontName="DejaVuSans", fontSize=10.5, leading=15, alignment=TA_LEFT)
caption = ParagraphStyle("Caption", parent=styles["Normal"], fontName="DejaVuSans-Oblique", fontSize=9, textColor=colors.grey, alignment=1, spaceAfter=14)

doc = SimpleDocTemplate(
    "/home/claude/sales_project/Satis_Analizi_Raporu.pdf",
    pagesize=A4,
    topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
)

story = []

# --- Başlık ---
story.append(Paragraph("2025 E-Commerce Sales Analysis", title_style))
story.append(Paragraph("Sample Portfolio Project — Data analysis with Python (pandas, matplotlib)", body))
story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", color=colors.HexColor("#1e3a8a"), thickness=1))
story.append(Spacer(1, 16))

# --- Özet metrik tablosu ---
story.append(Paragraph("Executive Summary", h2))
metrics_data = [
    ["Total Revenue", f"{s['total_revenue']:,.0f} TRY"],
    ["Total Orders", f"{s['total_orders']:,}"],
    ["Average Order Value", f"{s['avg_order_value']:,.0f} TRY"],
    ["Average Customer Rating", f"{s['avg_rating']} / 5"],
]
t = Table(metrics_data, colWidths=[8 * cm, 6 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eff6ff")),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1e3a8a")),
    ("FONTNAME", (0, 0), (0, -1), "DejaVuSans-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "DejaVuSans"),
    ("FONTSIZE", (0, 0), (-1, -1), 10.5),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dbeafe")),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
]))
story.append(t)
story.append(Spacer(1, 20))

# --- Aylık trend ---
story.append(Paragraph("Monthly Revenue Trend", h2))
story.append(Paragraph(
    f"The strongest month of the year was <b>{insights['best_month']}</b> — driven by the November "
    f"discount season and year-end holiday shopping. The dip seen in April-May points to a seasonal "
    f"slowdown, suggesting campaigns should be planned around that period.",
    body
))
story.append(Spacer(1, 8))
story.append(Image(f"{CHART_DIR}/monthly_revenue.png", width=16 * cm, height=8 * cm))
story.append(Paragraph("Figure 1: Total revenue by month (TRY)", caption))

story.append(PageBreak())

# --- Kategori ve ürün ---
story.append(Paragraph("Category & Product Performance", h2))
story.append(Paragraph(
    f"The <b>{insights['best_category']}</b> category accounts for the largest share of total revenue. "
    f"At the product level, <b>{insights['top_product']}</b> generated the highest revenue — a strong "
    f"candidate for stock and campaign prioritization.",
    body
))
story.append(Spacer(1, 8))
story.append(Image(f"{CHART_DIR}/revenue_by_category.png", width=16 * cm, height=8 * cm))
story.append(Paragraph("Figure 2: Total revenue by category", caption))
story.append(Image(f"{CHART_DIR}/top_products.png", width=16 * cm, height=8 * cm))
story.append(Paragraph("Figure 3: Top 5 products by revenue", caption))

story.append(PageBreak())

# --- Bölge ve kanal ---
story.append(Paragraph("Region & Sales Channel Analysis", h2))
story.append(Paragraph(
    f"<b>{insights['top_region']}</b> is the highest-performing region by revenue. On the channel side, "
    f"orders placed via <b>{insights['best_channel']}</b> have the highest average order value — "
    f"improvements to that channel's flow (e.g. checkout experience) could be prioritized. Roughly "
    f"{insights['discount_orders_pct']}% of orders were purchased at a discount, which may be worth "
    f"reviewing as part of the pricing strategy.",
    body
))
story.append(Spacer(1, 8))
story.append(Image(f"{CHART_DIR}/revenue_by_region.png", width=11 * cm, height=8 * cm))
story.append(Paragraph("Figure 4: Revenue distribution by region", caption))
story.append(Image(f"{CHART_DIR}/avg_order_by_channel.png", width=13 * cm, height=7.5 * cm))
story.append(Paragraph("Figure 5: Average order value by channel", caption))

story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", color=colors.HexColor("#dbeafe"), thickness=1))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<i>This report was built end-to-end on a sample (synthetic) dataset using Python (pandas, "
    "matplotlib, reportlab). The source code covering data cleaning, analysis, and report "
    "generation is included alongside this report in the portfolio.</i>",
    ParagraphStyle("Footer", parent=body, fontSize=9, textColor=colors.grey)
))

doc.build(story)
print("PDF oluşturuldu: Satis_Analizi_Raporu.pdf")
