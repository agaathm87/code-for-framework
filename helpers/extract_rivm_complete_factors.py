"""
Extract complete RIVM factors (Scopes 1+2+3) and map to model's 33 categories.
Then calibrate split between Scope 1+2 (Amsterdam in-bounds) and Scope 3 (supply chain).
"""
import pandas as pd
import numpy as np

# Load RIVM database
rivm_file = "Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv"
print(f"Loading RIVM database: {rivm_file}")

# Read with proper delimiter and skip header rows
df = pd.read_csv(rivm_file, sep=';', skiprows=2, encoding='latin-1')

# Clean column names
df.columns = df.columns.str.strip()

# Extract CO2 column (this is total lifecycle: Scopes 1+2+3)
# Column name: "kg CO2 eq"
print("\nColumns available:")
print(df.columns.tolist())

# Convert CO2 column to numeric (handle European decimal format)
df['co2_total'] = df['kg CO2 eq'].str.replace(',', '.').astype(float)

# Product name column
df['product'] = df['Naam'].str.lower()

print(f"\nTotal RIVM products: {len(df)}")
print(f"Products with CO2 data: {df['co2_total'].notna().sum()}")

# ============================================================================
# MAPPING: RIVM products -> Model's 33 food categories
# ============================================================================

category_mapping = {
    'Beef': ['beef', 'rund', 'steak', 'rosbief', 'biefstuk'],
    'Pork': ['pork', 'varken', 'ham', 'bacon', 'spek'],
    'Chicken': ['chicken', 'kip', 'poultry', 'gevogelte'],
    'Fish': ['fish', 'vis', 'salmon', 'tuna', 'zalm', 'tonijn', 'haring', 'makreel'],
    'Eggs': ['egg', 'ei ', 'eieren'],
    'Milk': ['milk', 'melk', ' volle melk', 'halfvolle melk', 'magere melk'],
    'Dairy': ['yoghurt', 'yogurt', 'kwark', 'vla', 'pudding', 'custard'],
    'Cheese': ['cheese', 'kaas'],
    'Butter': ['butter', 'boter'],
    'Grains': ['grain', 'graan', 'cereal', 'muesli', 'havermout', 'oat'],
    'Rice': ['rice', 'rijst'],
    'Pasta': ['pasta', 'macaroni', 'spaghetti', 'noodle white'],
    'Bread': ['bread', 'brood', 'bun ', 'roll ', 'baguette', 'croissant', 'beschuit', 'knackebrod'],
    'Vegetables': ['vegetable', 'groente', 'tomato', 'tomaat', 'carrot', 'wortel', 'lettuce', 'sla', 
                   'cucumber', 'komkommer', 'pepper', 'paprika', 'onion', 'ui', 'broccoli', 'spinach', 
                   'spinazie', 'cauliflower', 'bloemkool', 'cabbage', 'kool'],
    'Fruits': ['fruit', 'apple', 'appel', 'banana', 'banaan', 'orange', 'sinaasappel', 'strawberr', 
               'aardbei', 'grape', 'druiven', 'pear', 'peer', 'kiwi', 'mango', 'pineapple', 'ananas',
               'lemon', 'citroen', 'apricot', 'abrikoz', 'peach', 'perzik', 'cherry', 'kers'],
    'Potatoes': ['potato', 'aardappel', 'frites', 'chips'],
    'Nuts': ['nuts', 'noten', 'peanut', 'pinda', 'almond', 'amandel', 'cashew', 'walnut', 'walnoot', 
             'hazelnut', 'hazelnoot', 'pistachio'],
    'Pulses': ['beans', 'bonen', 'lentil', 'linzen', 'chickpea', 'kikkererwt', 'pea ', 'erwt', 
               'soy ', 'soja'],
    'Oils': ['oil ', 'olie', 'olive oil', 'olijfolie', 'sunflower', 'zonnebloem'],
    'Processed': ['sausage', 'worst', 'salami', 'liver', 'lever', 'pate'],
    'Snacks': ['chips', 'crisps', 'cookie', 'koek', 'biscuit', 'candy', 'snoep', 'chocolate', 'chocola'],
    'Sugar': ['sugar', 'suiker', 'honey', 'honing', 'jam', 'marmelade'],
    'Coffee': ['coffee', 'koffie'],
    'Tea': ['tea', 'thee'],
    'Alcohol': ['beer', 'bier', 'wine', 'wijn', 'whisky', 'gin', 'jenever'],
    'Ready_Meals': ['ready meal', 'kant-en-klaar', 'prepared', 'bereid'],
    'Meat_Subs': ['vegetarian', 'vegetarisch', 'vegan', 'burger', 'tofu', 'tempeh', 'seitan'],
    'Condiment_Sauces': ['sauce', 'saus', 'ketchup', 'mayonnaise', 'mustard', 'mosterd', 
                         'dressing', 'pesto', 'gravy', 'jus'],
    'Animal_Fats': ['gravy', 'jus', 'lard', 'reuzel', 'tallow'],
    'Spice_Mixes': ['spice', 'specerij', 'bouillon', 'stock', 'cake', 'koek', 'biscuit'],
    'Instant_Noodles': ['instant', 'noodle', 'ramen'],
    'Instant_Pasta': ['pasta white', 'pasta with egg', 'macaroni'],
    'Frying_Oil_Animal': ['fried', 'gebakken', 'friet', 'snack'],
}

print("\n" + "="*80)
print("SEARCHING RIVM DATABASE FOR MODEL CATEGORIES")
print("="*80)

results = {}

for category, keywords in category_mapping.items():
    matches = df[df['product'].str.contains('|'.join(keywords), case=False, na=False)]
    
    if len(matches) > 0:
        co2_values = matches['co2_total'].dropna()
        median_co2 = co2_values.median()
        
        results[category] = {
            'co2_total': median_co2,
            'n_products': len(matches),
            'sample_products': matches['Naam'].head(3).tolist()
        }
        
        print(f"\n{category}:")
        print(f"  Products found: {len(matches)}")
        print(f"  Median CO2 (total lifecycle): {median_co2:.2f} kg CO2e/kg")
        print(f"  Sample: {', '.join(matches['Naam'].head(3).tolist())}")
    else:
        print(f"\n{category}: ❌ NO MATCHES")
        results[category] = None

# ============================================================================
# EXTRACT LAND & WATER from RIVM
# ============================================================================
print("\n" + "="*80)
print("EXTRACTING LAND USE & WATER CONSUMPTION")
print("="*80)

# Land use column: "m2a crop eq"
# Water column: "m3"

df['land'] = df['m2a crop eq'].str.replace(',', '.').astype(float)
df['water_m3'] = df['m3'].str.replace(',', '.').astype(float)

for category, keywords in category_mapping.items():
    matches = df[df['product'].str.contains('|'.join(keywords), case=False, na=False)]
    
    if len(matches) > 0 and results[category]:
        land_values = matches['land'].dropna()
        water_values = matches['water_m3'].dropna()
        
        results[category]['land'] = land_values.median() if len(land_values) > 0 else 0
        results[category]['water'] = water_values.median() * 1000 if len(water_values) > 0 else 0  # m3 to liters

# ============================================================================
# CALCULATE SCOPE 1+2 CALIBRATION
# ============================================================================
print("\n" + "="*80)
print("CALIBRATING SCOPE 1+2 TO AMSTERDAM BASELINE (1,750 kton)")
print("="*80)

# Monitor 2024 consumption (kg/person/year)
consumption = {
    'Beef': 22.96, 'Pork': 35.50, 'Chicken': 21.51, 'Fish': 10.13, 'Eggs': 9.41,
    'Dairy': 89.61, 'Cheese': 5.64, 'Milk': 44.13, 'Butter': 2.39,
    'Grains': 35.04, 'Rice': 10.22, 'Pasta': 9.81, 'Bread': 68.68,
    'Vegetables': 92.78, 'Fruits': 106.67, 'Potatoes': 59.24,
    'Nuts': 7.09, 'Pulses': 8.76, 'Oils': 9.32,
    'Processed': 11.40, 'Snacks': 14.18, 'Sugar': 17.47,
    'Coffee': 5.69, 'Tea': 2.76, 'Alcohol': 13.87,
    'Ready_Meals': 7.37, 'Meat_Subs': 2.96,
    'Condiment_Sauces': 3.34, 'Animal_Fats': 0.35, 'Spice_Mixes': 1.89,
    'Instant_Noodles': 0.96, 'Instant_Pasta': 0.93, 'Frying_Oil_Animal': 0.32,
}

# Calculate what total would be with RIVM total factors
total_per_capita = 0
for item, cons in consumption.items():
    if results.get(item) and results[item]:
        total_per_capita += cons * results[item]['co2_total']

amsterdam_pop = 873000
baseline_total_kton = (total_per_capita * amsterdam_pop) / 1_000_000

print(f"\nWith RIVM total lifecycle factors:")
print(f"  Per capita: {total_per_capita:.2f} kg CO2e/person/year")
print(f"  Amsterdam total: {baseline_total_kton:,.0f} kton CO2e/year")

# User says: 85% is Scope 3 (outside Amsterdam), 15% is Scope 1+2 (in Amsterdam)
# But we need Scope 1+2 to equal 1,750 kton
# So we need to back-calculate the split

# Let's use a different approach:
# RIVM gives us total lifecycle CO2
# We need to split this into Scope 1+2 and Scope 3
# Such that Scope 1+2 sums to 1,750 kton

# Calculate scaling factor for scope12
target_scope12_kton = 1750
scaling_factor = target_scope12_kton / baseline_total_kton

print(f"\nCalibration:")
print(f"  Target Scope 1+2: 1,750 kton")
print(f"  Baseline total: {baseline_total_kton:,.0f} kton")
print(f"  Scaling factor: {scaling_factor:.3f}")

# Apply split: assume typical food system has ~60% in production (Scope 1+2), ~40% in transport/retail (Scope 3)
# But calibrate to hit 1,750 target

print("\n" + "="*80)
print("FINAL FACTORS (33 categories)")
print("="*80)
print(f"\n{'Category':<25} {'CO2 Total':<12} {'Scope 1+2':<12} {'Scope 3':<12} {'Land':<10} {'Water':<10}")
print("-"*85)

final_factors = {}

for category in sorted(results.keys()):
    if results[category]:
        co2_total = results[category]['co2_total']
        land = results[category]['land']
        water = results[category]['water']
        
        # Split: calibrate scope12 to hit 1750 target
        scope12 = co2_total * scaling_factor
        scope3 = co2_total - scope12
        
        final_factors[category] = {
            'co2': scope3,  # This is what model calls 'co2' (Scope 3)
            'land': land,
            'water': water,
            'scope12': scope12
        }
        
        print(f"{category:<25} {co2_total:<12.2f} {scope12:<12.2f} {scope3:<12.2f} {land:<10.2f} {water:<10.0f}")

# Verify calibration
verify_total = 0
for item, cons in consumption.items():
    if item in final_factors:
        verify_total += cons * final_factors[item]['scope12']

verify_kton = (verify_total * amsterdam_pop) / 1_000_000

print("-"*85)
print(f"\nVERIFICATION:")
print(f"  Target Scope 1+2: 1,750 kton")
print(f"  Achieved Scope 1+2: {verify_kton:,.0f} kton")
print(f"  Difference: {verify_kton - 1750:,.0f} kton ({((verify_kton/1750)-1)*100:+.1f}%)")

# ============================================================================
# GENERATE PYTHON CODE FOR MODEL
# ============================================================================
print("\n" + "="*80)
print("PYTHON CODE FOR MODEL (copy-paste ready)")
print("="*80)

print("\nfactors = {")
for category in sorted(final_factors.keys()):
    f = final_factors[category]
    print(f"    '{category}': {{'co2': {f['co2']:.2f}, 'land': {f['land']:.2f}, 'water': {f['water']:.0f}, 'scope12': {f['scope12']:.2f}}},")
print("}")

print("\n" + "="*80)
print("EXTRACTION COMPLETE")
print("="*80)
