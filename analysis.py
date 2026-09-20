"""
analysis.py
E-ticaret satış verisi analizi.

Bu script, ham satış verisini temizler, aylık/kategori/bölge bazında
analiz eder ve görselleştirmeler üretir. Çıktılar 'charts/' klasörüne
PNG olarak kaydedilir ve rapor oluşturma script'i (build_report.py)
tarafından kullanılır.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

plt.rcParams["font.size"] = 11
os.makedirs("/home/claude/sales_project/charts", exist_ok=True)

# --- 1. Veriyi yükle ve temizle ---
df = pd.read_csv("/home/claude/sales_project/sales_data.csv", parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# Temizlik kontrolleri (gerçek projelerde bu adım kritik)
assert df["revenue_try"].min() >= 0, "Negatif gelir bulundu!"
df = df.drop_duplicates(subset="order_id")
df = df.dropna(subset=["revenue_try", "category", "order_date"])

# --- 2. Genel özet metrikler ---
total_revenue = df["revenue_try"].sum()
total_orders = df["order_id"].nunique()
avg_order_value = df["revenue_try"].mean()
avg_rating = df["customer_rating"].mean()

summary = {
    "total_revenue": round(total_revenue, 2),
    "total_orders": total_orders,
    "avg_order_value": round(avg_order_value, 2),
    "avg_rating": round(avg_rating, 2),
}
print("Özet:", summary)

# --- 3. Aylık gelir trendi ---
monthly = df.groupby("month")["revenue_try"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["revenue_try"], marker="o", color="#2563eb", linewidth=2)
ax.set_title("Monthly Revenue Trend (2025)")
ax.set_ylabel("Revenue (TRY)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/claude/sales_project/charts/monthly_revenue.png", dpi=150)
plt.close()

# --- 4. Kategoriye göre gelir ---
by_category = df.groupby("category")["revenue_try"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(by_category.index, by_category.values, color="#059669")
ax.set_title("Total Revenue by Category")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig("/home/claude/sales_project/charts/revenue_by_category.png", dpi=150)
plt.close()

# --- 5. En çok satan 5 ürün ---
top_products = df.groupby("product")["revenue_try"].sum().sort_values(ascending=False).head(5)

fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(top_products.index[::-1], top_products.values[::-1], color="#d97706")
ax.set_title("Top 5 Products by Revenue")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig("/home/claude/sales_project/charts/top_products.png", dpi=150)
plt.close()

# --- 6. Bölgeye göre dağılım ---
by_region = df.groupby("region")["revenue_try"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(7, 5))
colors = plt.cm.Blues([0.9 - i * 0.11 for i in range(len(by_region))])
ax.pie(by_region.values, labels=by_region.index, autopct="%1.0f%%", colors=colors,
       textprops={"fontsize": 9}, startangle=90)
ax.set_title("Revenue Distribution by Region")
plt.tight_layout()
plt.savefig("/home/claude/sales_project/charts/revenue_by_region.png", dpi=150)
plt.close()

# --- 7. Kanala göre ortalama sipariş değeri ---
by_channel = df.groupby("channel")["revenue_try"].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(by_channel.index, by_channel.values, color="#7c3aed")
ax.set_title("Average Order Value by Channel")
ax.set_ylabel("Average Revenue (TRY)")
plt.tight_layout()
plt.savefig("/home/claude/sales_project/charts/avg_order_by_channel.png", dpi=150)
plt.close()

# --- 8. Sonuçları JSON'a yaz (rapor script'i okuyacak) ---
import json
insights = {
    "summary": summary,
    "best_month": monthly.loc[monthly["revenue_try"].idxmax(), "month"],
    "best_category": by_category.idxmax(),
    "top_product": top_products.idxmax(),
    "top_region": by_region.idxmax(),
    "best_channel": by_channel.idxmax(),
    "discount_orders_pct": round((df["discount_pct"] > 0).mean() * 100, 1),
}
with open("/home/claude/sales_project/insights.json", "w", encoding="utf-8") as f:
    json.dump(insights, f, ensure_ascii=False, indent=2)

print("Analiz tamamlandı. Grafikler 'charts/' klasörüne kaydedildi.")
print("İçgörüler:", insights)
