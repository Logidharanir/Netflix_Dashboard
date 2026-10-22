
import pandas as pd
import numpy as np

# =====================================
# NETFLIX ANALYTICS DATASET
# 150,000 RECORDS - INTERMEDIATE LEVEL
# =====================================

rng = np.random.default_rng(42)
N = 150_000

genres = [
    "Action", "Comedy", "Drama", "Thriller", "Romance",
    "Documentary", "Horror", "Sci-Fi", "Animation",
    "Crime", "Fantasy", "Adventure", "Mystery", "Family"
]

countries = [
    "United States", "India", "United Kingdom", "Canada",
    "South Korea", "Japan", "Spain", "France", "Germany",
    "Australia", "Mexico", "Brazil", "Turkey", "Italy"
]

ratings = ["TV-MA", "TV-14", "TV-PG", "R", "PG-13",
           "PG", "TV-Y7", "TV-Y", "G", "NR"]

content_types = ["Movie", "TV Show"]

# Generate realistic-looking synthetic data
release_year = rng.integers(1980, 2027, N)

date_added = (
    pd.Timestamp("2015-01-01")
    + pd.to_timedelta(
        rng.integers(
            0,
            (pd.Timestamp("2026-10-22") -
             pd.Timestamp("2015-01-01")).days + 1,
            N
        ),
        unit="D"
    )
)

views = rng.lognormal(mean=10.2, sigma=1.0, size=N).astype(int)
views = np.clip(views, 500, 50_000_000)

watch_hours = (
    views * rng.uniform(1.2, 2.8, N)
).astype(int)

estimated_revenue_usd = np.round(
    views * rng.uniform(0.015, 0.12, N), 2
)

df = pd.DataFrame({
    "content_id": [
        f"NF{i:06d}" for i in range(1, N + 1)
    ],
    "title": [
        f"{rng.choice(['The', 'Dark', 'Final', 'Hidden', 'Lost', 'New', 'Secret'])} "
        f"{rng.choice(['Story', 'Journey', 'World', 'Kingdom', 'Promise', 'Truth', 'Adventure'])} "
        f"{i}"
        for i in range(1, N + 1)
    ],
    "content_type": rng.choice(
        content_types, N, p=[0.70, 0.30]
    ),
    "genre": rng.choice(genres, N),
    "country": rng.choice(countries, N),
    "release_year": release_year,
    "rating": rng.choice(ratings, N),
    "date_added": date_added,
    "views": views,
    "watch_hours": watch_hours,
    "estimated_revenue_usd": estimated_revenue_usd
})

# Sort for easier date-based analysis
df = df.sort_values("date_added").reset_index(drop=True)

# Write directly to a genuine Excel workbook
output_file = "netflix_dashboard_dataset.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl",
    datetime_format="yyyy-mm-dd"
) as writer:
    df.to_excel(
        writer,
        sheet_name="Netflix_Data",
        index=False
    )

# Verify the generated Excel workbook
check = pd.read_excel(
    output_file,
    sheet_name="Netflix_Data",
    nrows=5,
    engine="openpyxl"
)

print("\nDataset created successfully!")
print("File:", output_file)
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("Excel sheet: Netflix_Data")
print("\nColumns:")
print(df.columns.tolist())
print("\nPreview:")
print(check.to_string(index=False))
print("\nData types:")
print(df.dtypes)
