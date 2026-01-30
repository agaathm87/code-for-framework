"""
Verify units, conversions, and scaling in the model
"""
import pandas as pd

print("="*80)
print("UNIT AND CONVERSION VERIFICATION")
print("="*80)

# 1. Check RIVM database units
print("\n1. RIVM DATABASE UNITS")
print("-"*80)
df_rivm = pd.read_csv('Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv',
                       sep=';', skiprows=2, encoding='utf-8', nrows=5)
print("Column headers:")
print(f"  Column 0 (Name): {df_rivm.columns[0]}")
print(f"  Column 1 (Unit): {df_rivm.columns[1]}")
print(f"  Column 3 (CO2): {df_rivm.columns[3]}")
print(f"  Column 7 (Land): {df_rivm.columns[7]}")
print(f"  Column 8 (Water): {df_rivm.columns[8]}")

print("\nFirst row values:")
print(df_rivm.iloc[0, [0, 1, 3, 7, 8]].to_dict())

# 2. Check aggregated CSV
print("\n2. AGGREGATED CSV UNITS")
print("-"*80)
df_agg = pd.read_csv('rivm_nevo_groups_aggregated.csv', encoding='utf-8')
print("Columns:", df_agg.columns.tolist())
print("\nFirst row (Aardappelen):")
print(df_agg.iloc[0].to_dict())

# 3. Check what the model is doing
print("\n3. MODEL CONVERSIONS (from load_impact_factors)")
print("-"*80)
print("Current code:")
print("  'co2': float(co2_total) * SCOPE3_RATIO,")
print("  'scope12': float(co2_total) * SCOPE12_RATIO,")
print("  'land': float(land_m2),  # m² → km² per kg")
print("  'water': float(water_m3) * 1000.0  # m³ → liters per kg")
print("\nISSUE: Land conversion comment says 'm² → km²' but NO DIVISION by 1,000,000!")

# 4. Check impact factors file
print("\n4. SAVED IMPACT FACTORS")
print("-"*80)
df_factors = pd.read_csv('rivm_impact_factors_used.csv')
print("Sample (Beef):")
beef = df_factors[df_factors['Food_Item'] == 'Beef'].iloc[0]
print(f"  CO2 (Scope 3): {beef['co2']:.3f} kg CO2e/kg")
print(f"  Scope 1+2: {beef['scope12']:.3f} kg CO2e/kg")
print(f"  Land: {beef['land']:.3f} (units?)")
print(f"  Water: {beef['water']:.3f} (units?)")

print("\nSample (Potatoes):")
potato = df_factors[df_factors['Food_Item'] == 'Potatoes'].iloc[0]
print(f"  CO2 (Scope 3): {potato['co2']:.3f} kg CO2e/kg")
print(f"  Scope 1+2: {potato['scope12']:.3f} kg CO2e/kg")
print(f"  Land: {potato['land']:.3f} (units?)")
print(f"  Water: {potato['water']:.3f} (units?)")

# 5. Check population and consumption scaling
print("\n5. POPULATION AND CONSUMPTION")
print("-"*80)
print("Expected:")
print("  Amsterdam population: ~873,000")
print("  Days per year: 365")
print("  Total person-days: 873,000 × 365 = 318,645,000")

# 6. Check a manual calculation
print("\n6. MANUAL CALCULATION CHECK")
print("-"*80)
print("Example: If Monitor 2024 diet has 22g beef/capita/day:")
print("  Total beef consumption: 22g × 873,000 people × 365 days")
print("                        = 7,019,100,000 grams")
print("                        = 7,019,100 kg")
print("                        = 7,019.1 tonnes")
print("\nIf beef has 17.87 kg CO2/kg (total from RIVM):")
print("  Total beef CO2: 7,019.1 tonnes × 17.87 kg CO2/kg")
print("                = 125,411 tonnes CO2")
print("                = 125.4 kton CO2")
print("\nIf Monitor says meat is 25% of 1,750 kton = 437.5 kton:")
print("  Beef alone can't be 125 kton if ALL meat is only 437 kton")
print("  → Either consumption amounts are wrong, or factors are wrong")

print("\n" + "="*80)
print("ISSUES TO CHECK:")
print("="*80)
print("1. Land units: Code says 'm² → km²' but doesn't divide by 1,000,000")
print("2. Water units: Multiplies by 1000, but RIVM m³ already × 1000 = liters?")
print("3. Consumption amounts: Are Monitor diet grams correct?")
print("4. RIVM factors: Using 'per kg' but consumption in grams - need /1000?")
print("="*80)
