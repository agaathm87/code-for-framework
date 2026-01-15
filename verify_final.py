"""Final verification that calibrated factors match Monitor's 1750 kton"""

diet_monitor = {
    'Beef': 15, 'Pork': 20, 'Chicken': 25, 'Fish': 12,
    'Cheese': 25, 'Milk': 200, 'Eggs': 15,
    'Pulses': 20, 'Nuts': 10, 'Meat_Subs': 15,
    'Grains': 180, 'Vegetables': 150, 'Fruits': 150,
    'Potatoes': 80, 'Sugar': 30, 'Processed': 40
}

# CALIBRATED full food system Scope 1+2 factors
scope12_factors = {
    'Beef': 31.0, 'Pork': 24.8, 'Chicken': 18.6, 'Fish': 22.3,
    'Cheese': 12.4, 'Milk': 6.2, 'Eggs': 9.9,
    'Pulses': 5.0, 'Nuts': 2.5, 'Meat_Subs': 6.2,
    'Grains': 3.1, 'Vegetables': 2.5, 'Fruits': 2.5,
    'Potatoes': 2.5, 'Sugar': 2.5, 'Processed': 6.2
}

population = 882_000
total = sum((g/1000)*365*scope12_factors[f]*population/1000 for f, g in diet_monitor.items())

print(f"\n✓ CALIBRATED Scope 1+2: {total:,.0f} tonnes ({total/1000:.0f} kton)")
print(f"  Monitor Target:        1,750,000 tonnes (1750 kton)")
print(f"  Match:                 {abs((total - 1_750_000) / 1_750_000 * 100):.2f}% error")
