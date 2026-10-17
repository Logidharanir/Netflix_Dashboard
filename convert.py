
import pandas as pd

print("Reading Excel file...")

df = pd.read_excel(
    "netflix_dashboard_500000_records.xlsx",
    sheet_name="Netflix_Data",
    engine="openpyxl"
)

print("Converting to UTF-8 CSV...")

df.to_csv(
    "netflix_dashboard_500000_records.xlsx",
    index=False,
    encoding="utf-8"
)

print("Conversion completed successfully!")
print("Total records:", len(df))
