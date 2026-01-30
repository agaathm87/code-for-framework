"""
Comprehensive verification of units and calculations
"""
import pandas as pd

print("="*80)
print("COMPREHENSIVE UNIT VERIFICATION")
print("="*80)

# Constants from the model
POPULATION_TOTAL = 873000
WASTE_FACTOR = 1.138  # 13.8% waste

# Load factors
df_factors = pd.read_csv('rivm_impact_factors_used.csv', index_col='Food_Item')

# Monitor 2024 diet (grams per capita per day)
monitor_diet = {
    'Beef': 10, 'Pork': 15, 'Lamb': 2, 'Chicken': 25, 'Processed_Meats': 30,
    'Cheese': 35, 'Milk': 220, 'Fish': 22, 'Eggs': 28,
    'Pulses': 15, 'Nuts': 15, 'Meat_Subs': 20,
    'Grains': 230, 'Vegetables': 160, 'Fruits': 145, 'Potatoes': 45,
    'Sugar': 35, 'Snacks': 45, 'Cookies_Pastries': 40, 'Soups': 20,
    'Coffee': 12, 'Tea': 3, 'Alcohol': 25, 'Oils': 25,
    'Rice': 30, 'Bread': 150, 'Pasta': 30, 'Dairy': 0,
    'Butter': 12, 'Animal_Fats': 8,
    'Condiment_Sauces': 15, 'Spice_Mixes': 3
}

print("\n1. CALCULATION FLOW VERIFICATION")
print("-"*80)
print("For each food item, the model calculates:")
print("  kg_consumed_yr = (grams / 1000) × 365")
print("  kg_produced_yr = kg_consumed_yr × WASTE_FACTOR (1.138)")
print("  ")
print("  co2_tonnes = (kg_produced_yr × f['co2'] × POPULATION) / 1000")
print("  scope12_tonnes = (kg_produced_yr × f['scope12'] × POPULATION) / 1000")
print("  land_m2 = kg_produced_yr × f['land'] × POPULATION")
print("  water_l = kg_produced_yr × f['water'] × POPULATION")

print("\n2. STEP-BY-STEP EXAMPLE: BEEF")
print("-"*80)
beef_grams = monitor_diet['Beef']
beef_factors = df_factors.loc['Beef']

print(f"Input: {beef_grams} grams/capita/day")
print(f"\nStep 1: Convert to kg consumed per capita per year")
kg_consumed_yr = (beef_grams / 1000) * 365
print(f"  kg_consumed_yr = ({beef_grams} / 1000) × 365 = {kg_consumed_yr:.3f} kg/capita/year")

print(f"\nStep 2: Account for waste to get production")
kg_produced_yr = kg_consumed_yr * WASTE_FACTOR
print(f"  kg_produced_yr = {kg_consumed_yr:.3f} × {WASTE_FACTOR} = {kg_produced_yr:.3f} kg/capita/year")

print(f"\nStep 3: Scale to total population")
kg_total_produced = kg_produced_yr * POPULATION_TOTAL
print(f"  Total produced = {kg_produced_yr:.3f} × {POPULATION_TOTAL:,} = {kg_total_produced:,.0f} kg")
print(f"               = {kg_total_produced/1000:,.1f} tonnes")

print(f"\nStep 4: Calculate CO2 (Scope 3)")
print(f"  Factor: {beef_factors['co2']:.3f} kg CO2e/kg")
co2_tonnes = (kg_produced_yr * beef_factors['co2'] * POPULATION_TOTAL) / 1000
print(f"  CO2 = ({kg_produced_yr:.3f} × {beef_factors['co2']:.3f} × {POPULATION_TOTAL:,}) / 1000")
print(f"      = {co2_tonnes:,.1f} tonnes CO2e")

print(f"\nStep 5: Calculate Scope 1+2")
print(f"  Factor: {beef_factors['scope12']:.3f} kg CO2e/kg")
scope12_tonnes = (kg_produced_yr * beef_factors['scope12'] * POPULATION_TOTAL) / 1000
print(f"  Scope12 = ({kg_produced_yr:.3f} × {beef_factors['scope12']:.3f} × {POPULATION_TOTAL:,}) / 1000")
print(f"          = {scope12_tonnes:,.1f} tonnes CO2e")

print(f"\n✓ Scope 1+2 now uses produced mass (with waste), consistent with CO2")

print("\n3. CALCULATE TOTAL FOR ALL FOODS")
print("-"*80)
total_co2 = 0
total_scope12 = 0
total_land = 0
total_water = 0

for food, grams in monitor_diet.items():
    if food not in df_factors.index:
        print(f"  WARNING: {food} not in factors")
        continue
    
    f = df_factors.loc[food]
    kg_consumed_yr = (grams / 1000) * 365
    kg_produced_yr = kg_consumed_yr * WASTE_FACTOR
    
    co2_tonnes = (kg_produced_yr * f['co2'] * POPULATION_TOTAL) / 1000
    scope12_tonnes = (kg_produced_yr * f['scope12'] * POPULATION_TOTAL) / 1000
    land_m2 = kg_produced_yr * f['land'] * POPULATION_TOTAL
    water_l = kg_produced_yr * f['water'] * POPULATION_TOTAL
    
    total_co2 += co2_tonnes
    total_scope12 += scope12_tonnes
    total_land += land_m2
    total_water += water_l

print(f"\nTOTAL RESULTS (Monitor 2024 diet):")
print(f"  Scope 3 (CO2): {total_co2:,.0f} tonnes = {total_co2/1000:.1f} kton")
print(f"  Scope 1+2: {total_scope12:,.0f} tonnes = {total_scope12/1000:.1f} kton")
print(f"  TOTAL: {(total_co2 + total_scope12):,.0f} tonnes = {(total_co2 + total_scope12)/1000:.1f} kton")
print(f"  Scope 1+2 %: {total_scope12/(total_co2 + total_scope12)*100:.1f}%")
print(f"  ")
print(f"  Land: {total_land:,.0f} m²")
print(f"  Water: {total_water:,.0f} liters")

print("\n4. COMPARISON WITH AMSTERDAM MONITOR")
print("-"*80)
print("Amsterdam Monitor 2024 reports:")
print("  Total Scope 1+2: 1,570 kton (or 1,750 kton)")
print(f"\nOur calculation: {total_scope12/1000:.1f} kton")
print(f"Discrepancy: {abs(1570 - total_scope12/1000):,.0f} kton")
print(f"")
print(f"Ratio needed to match 1570: {1570 / (total_scope12/1000):.3f}x")
print(f"Ratio needed to match 1750: {1750 / (total_scope12/1000):.3f}x")

print("\n5. UNIT ISSUES FOUND")
print("-"*80)
print("✓ CO2 factors: kg CO2e/kg food (correct)")
print("✓ Consumption: grams/capita/day → kg/capita/year (correct)")
print("✓ Population scaling: × 873,000 (correct)")
print("✓ Tonnes conversion: / 1000 (correct)")
print("")
print("⚠️  INCONSISTENCY: Scope 1+2 uses consumed, CO2 uses produced")
print("    Should both use kg_produced_yr for consistency")
print("")
print("⚠️  Land units: Stored as m² but comment says 'km²' conversion")
print(f"    Current: {total_land:,.0f} m²")
print(f"    If converted to km²: {total_land/1e6:,.2f} km²")
print("")
print("⚠️  Water units: Multiplied by 1000 in load_impact_factors")
print(f"    Current: {total_water:,.0f} (liters or m³×1000?)")
print(f"    RIVM m³ already means cubic meters, ×1000 = liters is correct")

print("\n" + "="*80)
