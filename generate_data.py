"""
generate_data.py
Generates a realistic synthetic e-commerce sales dataset for portfolio purposes.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# --- Config ---
N_ROWS = 2400
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

categories = {
    "Electronics": ["Wireless Earbuds", "Smart Watch", "Bluetooth Speaker", "Power Bank", "Phone Case"],
    "Home & Living": ["Aroma Diffuser", "LED Desk Lamp", "Storage Box Set", "Throw Blanket", "Candle Set"],
    "Apparel": ["Basic T-Shirt", "Sweatshirt", "Sports Shorts", "Sock Set", "Cap"],
    "Beauty": ["Face Serum", "Moisturizing Cream", "Sunscreen", "Lipstick", "Shampoo"],
    "Sports & Outdoor": ["Yoga Mat", "Water Bottle", "Fitness Band", "Backpack", "Bike Lock"],
}

regions = ["Marmara", "Aegean", "Central Anatolia", "Mediterranean", "Black Sea", "Southeastern Anatolia", "Eastern Anatolia"]
region_weights = [0.32, 0.15, 0.18, 0.12, 0.09, 0.08, 0.06]

channels = ["Mobile App", "Website", "Desktop"]
channel_weights = [0.55, 0.35, 0.10]

price_ranges = {
    "Electronics": (150, 1200),
    "Home & Living": (80, 450),
    "Apparel": (60, 350),
    "Beauty": (70, 400),
    "Sports & Outdoor": (90, 600),
}

rows = []
date_range_days = (END_DATE - START_DATE).days

for i in range(N_ROWS):
    category = np.random.choice(list(categories.keys()), p=[0.28, 0.18, 0.22, 0.20, 0.12])
    product = np.random.choice(categories[category])

    # seasonal effect: more sales in Nov (indirim sezonu) and Dec (yılbaşı)
    day_offset = np.random.randint(0, date_range_days)
    order_date = START_DATE + timedelta(days=day_offset)
    month = order_date.month
    seasonal_boost = 1.0
    if month in (11, 12):
        seasonal_boost = 1.6
    elif month in (6, 7):
        seasonal_boost = 1.2

    if np.random.random() > (0.55 * seasonal_boost / 1.6):
        continue  # thin out to create realistic seasonal density

    low, high = price_ranges[category]
    unit_price = round(np.random.uniform(low, high), 2)
    quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.45, 0.2, 0.15, 0.1, 0.06, 0.04])
    discount_pct = np.random.choice([0, 0, 0, 10, 15, 20, 30], p=[0.5, 0.15, 0.1, 0.1, 0.07, 0.05, 0.03])
    revenue = round(unit_price * quantity * (1 - discount_pct / 100), 2)

    region = np.random.choice(regions, p=region_weights)
    channel = np.random.choice(channels, p=channel_weights)
    rating = np.random.choice([5, 4, 3, 2, 1], p=[0.42, 0.30, 0.15, 0.08, 0.05])

    rows.append({
        "order_id": f"ORD-{10000+i}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "category": category,
        "product": product,
        "unit_price_try": unit_price,
        "quantity": quantity,
        "discount_pct": discount_pct,
        "revenue_try": revenue,
        "region": region,
        "channel": channel,
        "customer_rating": rating,
    })

df = pd.DataFrame(rows)
df = df.sort_values("order_date").reset_index(drop=True)
df.to_csv("/home/claude/sales_project/sales_data.csv", index=False)
print(f"Generated {len(df)} rows")
print(df.head())
