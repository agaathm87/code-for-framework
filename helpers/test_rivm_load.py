#!/usr/bin/env python3
"""Quick test of RIVM database loading for specific items."""

import pandas as pd
import os
import unicodedata

# Test loading detailed database
detailed_db_path = 'Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv'

print("Attempting to load detailed RIVM database...")
try:
    # CSV uses semicolon separators; skip first 2 rows (metadata), use row 2 as header
    df = pd.read_csv(detailed_db_path, sep=';', skiprows=2, encoding='utf-8', on_bad_lines='skip')
    print(f"✓ Loaded {len(df)} rows")
    print(f"Columns: {df.columns.tolist()[:10]}...")
    print()
    
    # Show first few products
    print("First 2 products:")
    for col in ['Naam', 'Global warming', 'Land use', 'Water consumption']:
        print(f"  {col}: {df.iloc[0][col]} | {df.iloc[1][col]}")
    print()
    
    # Search for butter, chicken, rice
    test_keywords = ['butter', 'chicken', 'rice']
    for kw in test_keywords:
        matches = df[df['Naam'].str.lower().str.contains(kw, na=False)]
        if not matches.empty:
            print(f"\n{kw.upper()} matches found: {len(matches)}")
            for idx, row in matches.head(2).iterrows():
                co2_val = str(row['Global warming']).replace(',', '.')
                land_val = str(row['Land use']).replace(',', '.')
                water_val = str(row['Water consumption']).replace(',', '.')
                print(f"  {row['Naam'][:50]}")
                print(f"    CO2: {co2_val} kg CO2e/kg")
                print(f"    Land: {land_val} m2a/kg")
                print(f"    Water: {water_val} m3/kg")
        else:
            print(f"\n{kw.upper()}: No matches found")
            
except FileNotFoundError:
    print(f"✗ File not found: {detailed_db_path}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")

# Test aggregated database
print("\n" + "="*60)
agg_db_path = 'rivm_nevo_groups_aggregated.csv'
print(f"Loading aggregated NEVO database from {agg_db_path}...")
try:
    df_agg = pd.read_csv(agg_db_path)
    print(f"✓ Loaded {len(df_agg)} groups")
    print(df_agg[['NEVO_Product_Group', 'CO2_Mean_kg', 'Land_Mean_m2', 'Water_Mean_m3']].head(5))
except FileNotFoundError:
    print(f"✗ File not found: {agg_db_path}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
