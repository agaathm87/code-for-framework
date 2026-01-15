"""Calculate proper Scope 1+2 factors that reach 1750 kton with all components"""

# Target: 1750 kton total
# Current: 2624 kton (base: 2312, waste: 254, retail: 58)
# We need to reduce base by: 1750 / (1 + 0.11 + 0.025) = 1750 / 1.135 = 1542 kton

target_total = 1750  # kton
waste_rate = 0.11
retail_rate = 0.025
multiplier = 1 + waste_rate + retail_rate  # 1.135

target_base = target_total / multiplier  # Target for base food only
print(f"Target breakdown:")
print(f"  Base food:     {target_base:.0f} kton")
print(f"  Waste (11%):   {target_base * waste_rate:.0f} kton")
print(f"  Retail (2.5%): {target_base * retail_rate:.0f} kton")
print(f"  TOTAL:         {target_base * multiplier:.0f} kton\n")

# Current base is 2312 kton, need 1542 kton
# Reduction factor needed
current_base = 2312
reduction = target_base / current_base
print(f"Current base: {current_base} kton")
print(f"Reduction factor needed: {reduction:.4f}x ({(1-reduction)*100:.1f}% reduction)\n")

# Apply to all factors
factors_current = {
    'Beef': 25.0, 'Pork': 20.0, 'Chicken': 15.0, 'Fish': 18.0,
    'Cheese': 10.0, 'Milk': 5.0, 'Eggs': 8.0,
    'Pulses': 4.0, 'Nuts': 2.0, 'Meat_Subs': 5.0,
    'Grains': 2.5, 'Vegetables': 2.0, 'Fruits': 2.0,
    'Potatoes': 2.0, 'Sugar': 2.0, 'Processed': 5.0,
    'Coffee': 35.0, 'Tea': 12.0, 'Alcohol': 20.0,
    'Oils': 8.0, 'Snacks': 15.0, 'Condiments': 6.0
}

print("="*70)
print("CALIBRATED Scope 1+2 Factors (kgCO2e/kg):")
print("="*70)
for food, current in factors_current.items():
    adjusted = current * reduction
    print(f"'{food:12s}': {adjusted:5.2f},  # was {current:5.1f}")
