"""
Verify that explicit food groups reach Monitor's 1750 kton target
"""

# Monitor 2024 diet with ALL food groups
diet_complete = {
    'Beef': 10, 'Pork': 15, 'Chicken': 25, 'Cheese': 35, 'Milk': 220,
    'Fish': 22, 'Eggs': 28, 'Pulses': 15, 'Nuts': 15, 'Meat_Subs': 20,
    'Grains': 230, 'Vegetables': 160, 'Fruits': 145, 'Potatoes': 45,
    'Sugar': 35, 'Processed': 140,
    'Coffee': 12, 'Tea': 3, 'Alcohol': 25, 'Oils': 25, 'Snacks': 45, 'Condiments': 20
}

# Full system Scope 1+2 factors (includes retail, food service, household, waste)
scope12_factors = {
    'Beef': 25.0, 'Pork': 20.0, 'Chicken': 15.0, 'Fish': 18.0,
    'Cheese': 10.0, 'Milk': 5.0, 'Eggs': 8.0,
    'Pulses': 4.0, 'Nuts': 2.0, 'Meat_Subs': 5.0,
    'Grains': 2.5, 'Vegetables': 2.0, 'Fruits': 2.0,
    'Potatoes': 2.0, 'Sugar': 2.0, 'Processed': 5.0,
    'Coffee': 35.0, 'Tea': 12.0, 'Alcohol': 20.0,
    'Oils': 8.0, 'Snacks': 15.0, 'Condiments': 6.0
}

population = 882_000

# Calculate base food consumption
total_base = 0
print("\n" + "="*70)
print("COMPLETE MONITOR 2024 DIET - Scope 1+2 Breakdown")
print("="*70)
for food, grams in diet_complete.items():
    kg_year = (grams / 1000) * 365
    factor = scope12_factors[food]
    tonnes = kg_year * factor * population / 1000
    total_base += tonnes
    print(f"{food:12s}: {grams:3.0f}g/day → {kg_year:5.1f}kg/yr × {factor:5.1f} = {tonnes:8,.0f} tonnes")

print("="*70)
print(f"TOTAL BASE FOOD:       {total_base:10,.0f} tonnes ({total_base/1000:5.0f} kton)")

# Add explicit food waste (household + processing waste ~10-12% of total)
waste_rate = 0.11  # 11% food waste
waste_emissions = total_base * waste_rate
print(f"FOOD WASTE (11%):      {waste_emissions:10,.0f} tonnes ({waste_emissions/1000:5.0f} kton)")

# Add retail/distribution (cold chain, urban logistics)
# ~2.5% of total for refrigerated distribution
retail_dist_rate = 0.025
retail_emissions = total_base * retail_dist_rate
print(f"RETAIL/DISTRIBUTION:   {retail_emissions:10,.0f} tonnes ({retail_emissions/1000:5.0f} kton)")

# TOTAL
grand_total = total_base + waste_emissions + retail_emissions
print("="*70)
print(f"GRAND TOTAL S1+2:      {grand_total:10,.0f} tonnes ({grand_total/1000:5.0f} kton)")
print(f"Monitor Target:        {1_750_000:10,.0f} tonnes (1750 kton)")
print(f"Difference:            {((grand_total - 1_750_000) / 1_750_000 * 100):+5.1f}%")
print("="*70)
