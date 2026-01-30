"""Quick test to verify Scope 1+2 calculations match Monitor's 1750 kton"""

# Sample Monitor 2024 diet from the model
diet_monitor = {
    'Beef': 15, 'Pork': 20, 'Chicken': 25, 'Fish': 12,
    'Cheese': 25, 'Milk': 200, 'Eggs': 15,
    'Pulses': 20, 'Nuts': 10, 'Meat_Subs': 15,
    'Grains': 180, 'Vegetables': 150, 'Fruits': 150,
    'Potatoes': 80, 'Sugar': 30, 'Processed': 40
}

# Full food system Scope 1+2 factors (updated)
scope12_factors = {
    'Beef': 25.0, 'Pork': 20.0, 'Chicken': 15.0, 'Fish': 18.0,
    'Cheese': 10.0, 'Milk': 5.0, 'Eggs': 8.0,
    'Pulses': 4.0, 'Nuts': 2.0, 'Meat_Subs': 5.0,
    'Grains': 2.5, 'Vegetables': 2.0, 'Fruits': 2.0,
    'Potatoes': 2.0, 'Sugar': 2.0, 'Processed': 5.0
}

population = 882_000

total_scope12 = 0
print("\nMonitor 2024 Diet - Scope 1+2 Calculation:")
print("=" * 60)
for food, grams_day in diet_monitor.items():
    kg_year_person = (grams_day / 1000) * 365
    factor = scope12_factors[food]
    tonnes_total = kg_year_person * factor * population / 1000
    total_scope12 += tonnes_total
    print(f"{food:12s}: {grams_day:3.0f}g/day → {kg_year_person:5.1f}kg/yr/person × {factor:4.1f} × 882k = {tonnes_total:8,.0f} tonnes")

print("=" * 60)
print(f"TOTAL SCOPE 1+2: {total_scope12:,.0f} tonnes ({total_scope12/1000:.0f} kton)")
print(f"Monitor Target:  1,750,000 tonnes (1750 kton)")
print(f"Difference:      {((total_scope12 - 1_750_000) / 1_750_000 * 100):+.1f}%")
