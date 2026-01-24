"""Verify RIVM baseline against Monitor 1750 kton"""

# RIVM scope12 factors (from model)
factors = {
    'Alcohol': 0.22,
    'Animal_Fats': 22.0,
    'Beef': 13.99,
    'Bread': 0.6,
    'Butter': 1.78,
    'Cheese': 4.42,
    'Chicken': 1.96,
    'Coffee': 0.77,
    'Condiment_Sauces': 4.5,
    'Dairy': 1.78,
    'Eggs': 0.51,
    'Fish': 2.06,
    'Fruits': 0.19,
    'Frying_Oil_Animal': 22.0,
    'Grains': 0.43,
    'Instant_Noodles': 3.0,
    'Instant_Pasta': 0.65,
    'Meat_Subs': 3.33,
    'Milk': 0.77,
    'Nuts': 0.61,
    'Oils': 0.56,
    'Pasta': 0.65,
    'Pork': 6.91,
    'Potatoes': 0.38,
    'Processed': 0.9,
    'Pulses': 0.5,
    'Ready_Meals': 5.0,
    'Rice': 0.65,
    'Snacks': 1.2,
    'Spice_Mixes': 3.0,
    'Sugar': 0.24,
    'Tea': 1.16,
    'Vegetables': 0.26,
}

# Monitor 2024 consumption (from model)
consumption = {
    'Beef': 22.96,
    'Pork': 35.50,
    'Chicken': 21.51,
    'Fish': 10.13,
    'Eggs': 9.41,
    'Dairy': 89.61,
    'Cheese': 5.64,
    'Milk': 44.13,
    'Butter': 2.39,
    'Grains': 35.04,
    'Rice': 10.22,
    'Pasta': 9.81,
    'Bread': 68.68,
    'Vegetables': 92.78,
    'Fruits': 106.67,
    'Potatoes': 59.24,
    'Nuts': 7.09,
    'Pulses': 8.76,
    'Oils': 9.32,
    'Processed': 11.40,
    'Snacks': 14.18,
    'Sugar': 17.47,
    'Coffee': 5.69,
    'Tea': 2.76,
    'Alcohol': 13.87,
    'Ready_Meals': 7.37,
    'Meat_Subs': 2.96,
    'Condiment_Sauces': 3.34,
    'Animal_Fats': 0.35,
    'Spice_Mixes': 1.89,
    'Instant_Noodles': 0.96,
    'Instant_Pasta': 0.93,
    'Frying_Oil_Animal': 0.32,
}

print("=" * 80)
print("RIVM SCOPE 1+2 BASELINE VERIFICATION")
print("=" * 80)

total_scope12 = 0

for item, cons in consumption.items():
    if item in factors:
        factor = factors[item]
        contrib = cons * factor
        total_scope12 += contrib

print(f"\nTotal per capita Scope 1+2: {total_scope12:.2f} kg CO2e/person/year")

amsterdam_pop = 873000
total_scope12_kton = (total_scope12 * amsterdam_pop) / 1_000_000

print(f"\nScaled to Amsterdam ({amsterdam_pop:,} residents):")
print(f"Total Scope 1+2: {total_scope12_kton:,.0f} kton CO2e/year")
print()
print(f"TARGET from Monitor/RIVM: 1,750 kton")
print(f"DIFFERENCE: {total_scope12_kton - 1750:,.0f} kton ({((total_scope12_kton/1750)-1)*100:+.1f}%)")
print()
print("INTERPRETATION:")
print("- If ≈ 1,750: RIVM scope12 factors are correct as-is")
print("- If < 1,750: RIVM factors underestimate (need to check data extraction)")
print("- If > 1,750: RIVM factors overestimate")
print()
print("=" * 80)
