import pandas as pd
import os
import re
import calendar

# File paths
output_file = os.path.join(os.path.dirname(__file__), "gas.csv")
bord_gais_file = os.path.join(os.path.dirname(__file__), "Bord Gais Daily Data.csv")

# Read existing gas.csv
if os.path.exists(output_file):
    existing_gas = pd.read_csv(output_file, dtype=str)
    existing_dates = set(existing_gas["Date"])
else:
    existing_gas = pd.DataFrame(columns=["Year", "Month", "Date", "Hdd", "Gas (kWh)"])
    existing_dates = set()

# Read and clean Bord Gais Daily Data.csv
new_data = pd.read_csv(bord_gais_file, dtype=str)
cleaned_rows = []
for idx, row in new_data.iterrows():
    date_str = row["Date"]
    hdd = row["HDD"]
    gas = row["Gas (kWh)"]
    if isinstance(date_str, str) and re.match(r"\d{2}/\d{2}/\d{4}", date_str):
        try:
            date = pd.to_datetime(date_str, dayfirst=True)
            date_fmt = date.strftime("%d/%m/%Y")
            if date_fmt not in existing_dates:
                cleaned_rows.append({
                    "Year": date.year,
                    "Month": calendar.month_abbr[date.month],
                    "Date": date_fmt,
                    "Hdd": float(hdd) if pd.notna(hdd) else None,
                    "Gas (kWh)": float(str(gas).replace(",", "")) if pd.notna(gas) and gas not in ["", "nan"] else None
                })
        except Exception:
            continue

# Append new unique rows to gas.csv
if cleaned_rows:
    cleaned_df = pd.DataFrame(cleaned_rows, columns=["Year", "Month", "Date", "Hdd", "Gas (kWh)"])
    updated_gas = pd.concat([existing_gas, cleaned_df], ignore_index=True)
    updated_gas.to_csv(output_file, index=False)
    print(f"Appended {len(cleaned_rows)} new rows to {output_file}")
else:
    print("No new unique rows to append.")