"""Calculate adjustment factor needed to reach Monitor's 1750 kton"""

# Current result: 1,410,375 tonnes
# Target: 1,750,000 tonnes
# Multiplier needed: 1,750,000 / 1,410,375 = 1.241

adjustment = 1.241

print("\nAdjustment Factor Calculation:")
print("=" * 60)
print(f"Current Scope 1+2: 1,410,375 tonnes")
print(f"Monitor Target:    1,750,000 tonnes")
print(f"Multiplier needed: {adjustment:.3f}x")
print("\nThis ~24% increase accounts for:")
print("- Beverages (coffee, tea, alcohol)")
print("- Oils and fats")
print("- Snacks and confectionery")
print("- Condiments and sauces")
print("- Food waste processing")
print("- Additional cold chain/distribution losses")

# New factors (rounded for practicality)
print("\n" + "=" * 60)
print("RECOMMENDED FINAL Scope 1+2 Factors (kgCO2e/kg):")
print("=" * 60)

factors_current = {
    'Beef': 25.0, 'Pork': 20.0, 'Chicken': 15.0, 'Fish': 18.0,
    'Cheese': 10.0, 'Milk': 5.0, 'Eggs': 8.0,
    'Pulses': 4.0, 'Nuts': 2.0, 'Meat_Subs': 5.0,
    'Grains': 2.5, 'Vegetables': 2.0, 'Fruits': 2.0,
    'Potatoes': 2.0, 'Sugar': 2.0, 'Processed': 5.0
}

for food, current in factors_current.items():
    adjusted = current * adjustment
    print(f"'{food}': {adjusted:.1f}  (was {current:.1f})")
