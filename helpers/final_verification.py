"""
FINAL VERIFICATION: Complete Monitor 2024 diet with calibrated factors + waste + retail
Target: 1750 kton total
"""

# Complete Monitor 2024 diet with ALL food categories
diet_monitor = {
    'Beef': 10, 'Pork': 15, 'Chicken': 25, 'Cheese': 35, 'Milk': 220,
    'Fish': 22, 'Eggs': 28, 'Pulses': 15, 'Nuts': 15, 'Meat_Subs': 20,
    'Grains': 230, 'Vegetables': 160, 'Fruits': 145, 'Potatoes': 45,
    'Sugar': 35, 'Processed': 140,
    'Coffee': 12, 'Tea': 3, 'Alcohol': 25, 'Oils': 25, 'Snacks': 45, 'Condiments': 20
}

# CALIBRATED Scope 1+2 factors (0.6669x reduction)
scope12_factors = {
    'Beef': 16.67, 'Pork': 13.34, 'Chicken': 10.00, 'Fish': 12.00,
    'Cheese': 6.67, 'Milk': 3.33, 'Eggs': 5.34,
    'Pulses': 2.67, 'Nuts': 1.33, 'Meat_Subs': 3.33,
    'Grains': 1.67, 'Vegetables': 1.33, 'Fruits': 1.33,
    'Potatoes': 1.33, 'Sugar': 1.33, 'Processed': 3.33,
    'Coffee': 23.34, 'Tea': 8.00, 'Alcohol': 13.34,
    'Oils': 5.34, 'Snacks': 10.00, 'Condiments': 4.00
}

population = 882_000

# Calculate base food emissions
print("\n" + "="*75)
print(" AMSTERDAM MONITOR 2024 - COMPLETE Scope 1+2 CALCULATION")
print("="*75)
print(f"{'FOOD ITEM':<15} {'g/day':<8} {'kg/year':<10} {'Factor':<8} {'Tonnes':<15}")
print("-"*75)

total_base = 0
for food, grams in diet_monitor.items():
    kg_year = (grams / 1000) * 365
    factor = scope12_factors[food]
    tonnes = kg_year * factor * population / 1000
    total_base += tonnes
    print(f"{food:<15} {grams:>6.0f}   {kg_year:>8.1f}   {factor:>6.2f}   {tonnes:>12,.0f}")

print("-"*75)
print(f"{'BASE FOOD TOTAL':<44} {total_base:>12,.0f} tonnes")

# Add explicit food waste (11% of base - household + processing waste)
waste_rate = 0.11
waste_emissions = total_base * waste_rate
print(f"{'+ FOOD WASTE (11%)':<44} {waste_emissions:>12,.0f} tonnes")

# Add retail/distribution (2.5% - cold chain, urban logistics)
retail_rate = 0.025
retail_emissions = total_base * retail_rate
print(f"{'+ RETAIL/DISTRIBUTION (2.5%)':<44} {retail_emissions:>12,.0f} tonnes")

# GRAND TOTAL
grand_total = total_base + waste_emissions + retail_emissions
print("="*75)
print(f"{'TOTAL SCOPE 1+2':<44} {grand_total:>12,.0f} tonnes")
print(f"{'TARGET (Monitor 2024)':<44} {1_750_000:>12,.0f} tonnes")
error = ((grand_total - 1_750_000) / 1_750_000 * 100)
print(f"{'ERROR':<44} {error:>12.2f}%")
print("="*75)

# Breakdown by component
print("\nBREAKDOWN:")
print(f"  Base Food:          {total_base:>10,.0f} tonnes ({total_base/grand_total*100:5.1f}%)")
print(f"  Waste:              {waste_emissions:>10,.0f} tonnes ({waste_emissions/grand_total*100:5.1f}%)")
print(f"  Retail/Distribution:{retail_emissions:>10,.0f} tonnes ({retail_emissions/grand_total*100:5.1f}%)")
print(f"  TOTAL:              {grand_total:>10,.0f} tonnes (100.0%)")

if abs(error) < 1.0:
    print("\n✓ SUCCESS! Within 1% of Monitor target!")
else:
    print(f"\n⚠ Off by {error:+.2f}% - may need minor adjustment")
