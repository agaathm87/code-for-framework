"""
Extract complete RIVM factors (Scopes 1+2+3) and map to model's 33 categories.
No external dependencies version.
"""
import csv
import statistics

# Load RIVM database
rivm_file = "Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv"
print(f"Loading RIVM database: {rivm_file}")

# Read CSV manually
with open(rivm_file, 'r', encoding='latin-1') as f:
    lines = f.readlines()

# Skip first 2 header rows, get column names from row 3
header = lines[2].strip().split(';')
print(f"\nColumns: {header[:15]}")  # First 15 columns

# Find column indices
col_name_idx = header.index('Naam')
col_co2_idx = header.index('kg CO2 eq')
col_land_idx = header.index('m2a crop eq')
col_water_idx = header.index('m3')

# Parse data rows (skip first 3 header rows)
products = []
for line in lines[3:]:
    row = line.strip().split(';')
    if len(row) > max(col_co2_idx, col_land_idx, col_water_idx):
        try:
            name = row[col_name_idx]
            co2_str = row[col_co2_idx].replace(',', '.')
            land_str = row[col_land_idx].replace(',', '.')
            water_str = row[col_water_idx].replace(',', '.')
            
            co2 = float(co2_str) if co2_str else None
            land = float(land_str) if land_str else None
            water = float(water_str) if water_str else None
            
            products.append({
                'name': name.lower(),
                'name_display': name,
                'co2_total': co2,
                'land': land,
                'water_m3': water
            })
        except:
            continue

print(f"Loaded {len(products)} products from RIVM database")

# ============================================================================
# MAPPING: RIVM products -> Model's 33 food categories
# ============================================================================

category_mapping = {
    'Beef': ['beef', 'rund', 'steak', 'rosbief', 'biefstuk'],
    'Pork': ['pork', 'varken', 'ham', 'bacon', 'spek'],
    'Chicken': ['chicken', 'kip', 'poultry', 'gevogelte'],
    'Fish': ['fish', 'vis', 'salmon', 'tuna', 'zalm', 'tonijn', 'haring', 'makreel'],
    'Eggs': ['egg', 'ei ', 'eieren'],
    'Milk': ['milk', 'melk'],
    'Dairy': ['yoghurt', 'yogurt', 'kwark', 'vla', 'pudding', 'custard'],
    'Cheese': ['cheese', 'kaas'],
    'Butter': ['butter', 'boter'],
    'Grains': ['grain', 'graan', 'cereal', 'muesli', 'havermout', 'oat'],
    'Rice': ['rice', 'rijst'],
    'Pasta': ['pasta', 'macaroni', 'spaghetti'],
    'Bread': ['bread', 'brood', 'bun ', 'roll ', 'baguette', 'croissant', 'beschuit'],
    'Vegetables': ['vegetable', 'groente', 'tomato', 'tomaat', 'carrot', 'wortel', 'lettuce', 
                   'cucumber', 'pepper', 'paprika', 'onion', 'ui', 'broccoli', 'spinach', 
                   'cauliflower', 'cabbage'],
    'Fruits': ['fruit', 'apple', 'appel', 'banana', 'banaan', 'orange', 'strawberr', 
               'aardbei', 'grape', 'druiven', 'pear', 'kiwi', 'mango', 'pineapple', 'ananas'],
    'Potatoes': ['potato', 'aardappel', 'frites', 'chips frozen'],
    'Nuts': ['nuts', 'noten', 'peanut', 'pinda', 'almond', 'cashew', 'walnut', 'hazelnut'],
    'Pulses': ['beans', 'bonen', 'lentil', 'chickpea', 'pea ', 'erwt', 'soy ', 'soja'],
    'Oils': ['oil sunflower', 'oil olive', 'olie zonnebloem', 'olie olijf'],
    'Processed': ['sausage', 'worst', 'salami', 'liver', 'lever'],
    'Snacks': ['chips', 'crisps', 'cookie', 'koek', 'biscuit', 'candy', 'chocolate'],
    'Sugar': ['sugar', 'suiker', 'honey', 'honing', 'jam'],
    'Coffee': ['coffee', 'koffie'],
    'Tea': ['tea', 'thee'],
    'Alcohol': ['beer', 'bier', 'wine', 'wijn', 'whisky', 'gin', 'jenever'],
    'Ready_Meals': ['ready', 'prepared', 'wrap', 'tortilla'],
    'Meat_Subs': ['vegetarian', 'vegetarisch', 'burger', 'tofu', 'tempeh'],
    'Condiment_Sauces': ['sauce', 'saus', 'ketchup', 'mayonnaise', 'mustard', 'pesto', 'gravy'],
    'Animal_Fats': ['gravy', 'jus', 'lard', 'mayonnaise'],
    'Spice_Mixes': ['spice', 'bouillon', 'stock', 'cake', 'biscuit'],
    'Instant_Noodles': ['instant', 'noodle', 'ramen'],
    'Instant_Pasta': ['pasta white', 'pasta with egg'],
    'Frying_Oil_Animal': ['fried', 'deep frying', 'friet'],
}

print("\n" + "="*80)
print("SEARCHING RIVM DATABASE FOR MODEL CATEGORIES")
print("="*80)

results = {}

for category, keywords in category_mapping.items():
    matches = []
    
    for product in products:
        if any(keyword in product['name'] for keyword in keywords):
            if product['co2_total'] is not None:
                matches.append(product)
    
    if len(matches) > 0:
        co2_values = [p['co2_total'] for p in matches]
        land_values = [p['land'] for p in matches if p['land'] is not None]
        water_values = [p['water_m3'] for p in matches if p['water_m3'] is not None]
        
        median_co2 = statistics.median(co2_values)
        median_land = statistics.median(land_values) if land_values else 0
        median_water = statistics.median(water_values) if water_values else 0
        
        results[category] = {
            'co2_total': median_co2,
            'land': median_land,
            'water': median_water * 1000,  # m3 to liters
            'n_products': len(matches),
            'sample_products': [m['name_display'] for m in matches[:3]]
        }
        
        print(f"\n{category}:")
        print(f"  Products: {len(matches)}")
        print(f"  Median CO2 (total): {median_co2:.2f} kg")
        print(f"  Median Land: {median_land:.2f} m²")
        print(f"  Median Water: {median_water*1000:.0f} L")
        print(f"  Sample: {', '.join([m['name_display'] for m in matches[:2]])}")
    else:
        print(f"\n{category}: ❌ NO MATCHES - using estimate")
        # Use reasonable estimates for missing categories
        estimates = {
            'Meat_Subs': {'co2_total': 2.5, 'land': 2.0, 'water': 500},
            'Ready_Meals': {'co2_total': 3.0, 'land': 2.5, 'water': 600},
            'Instant_Noodles': {'co2_total': 2.0, 'land': 1.5, 'water': 400},
            'Animal_Fats': {'co2_total': 8.0, 'land': 5.0, 'water': 3000},
            'Frying_Oil_Animal': {'co2_total': 8.0, 'land': 5.0, 'water': 3000},
        }
        if category in estimates:
            results[category] = {
                'co2_total': estimates[category]['co2_total'],
                'land': estimates[category]['land'],
                'water': estimates[category]['water'],
                'n_products': 0,
                'sample_products': ['[Estimated]']
            }

# ============================================================================
# CALIBRATE TO 1,750 kton BASELINE
# ============================================================================
print("\n" + "="*80)
print("CALIBRATING TO AMSTERDAM BASELINE (1,750 kton Scope 1+2)")
print("="*80)

# Monitor 2024 consumption
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

# Calculate baseline with RIVM total factors
total_per_capita = sum(consumption.get(cat, 0) * results[cat]['co2_total'] 
                       for cat in results if cat in consumption)

amsterdam_pop = 873000
baseline_kton = (total_per_capita * amsterdam_pop) / 1_000_000

print(f"\nRIVM Total Lifecycle CO2:")
print(f"  Per capita: {total_per_capita:.2f} kg CO2e/year")
print(f"  Amsterdam: {baseline_kton:,.0f} kton CO2e/year")

# Calculate scaling to hit 1,750 kton for Scope 1+2
target_kton = 1750
scaling_factor = target_kton / baseline_kton

print(f"\nCalibration Factor: {scaling_factor:.3f}")
print(f"  (Scales RIVM total to get Scope 1+2 = 1,750 kton)")

# ============================================================================
# FINAL FACTORS
# ============================================================================
print("\n" + "="*80)
print("FINAL FACTORS (33 categories)")
print("="*80)
print(f"\n{'Category':<25} {'Total':<10} {'Scope12':<10} {'Scope3':<10} {'Land':<10} {'Water':<10}")
print("-"*75)

final_factors = {}

for category in sorted(results.keys()):
    co2_total = results[category]['co2_total']
    land = results[category]['land']
    water = results[category]['water']
    
    # Apply calibration: scale total to get scope12 that hits 1,750
    scope12 = co2_total * scaling_factor
    scope3 = co2_total - scope12
    
    final_factors[category] = {
        'co2': scope3,
        'land': land,
        'water': water,
        'scope12': scope12
    }
    
    print(f"{category:<25} {co2_total:<10.2f} {scope12:<10.2f} {scope3:<10.2f} {land:<10.2f} {water:<10.0f}")

# Verify
verify = sum(consumption.get(cat, 0) * final_factors[cat]['scope12'] 
             for cat in final_factors if cat in consumption)
verify_kton = (verify * amsterdam_pop) / 1_000_000

print("-"*75)
print(f"\nVERIFICATION:")
print(f"  Target: 1,750 kton")
print(f"  Achieved: {verify_kton:,.0f} kton")
print(f"  Difference: {verify_kton - 1750:+.0f} kton")

# ============================================================================
# PYTHON CODE OUTPUT
# ============================================================================
print("\n" + "="*80)
print("COPY-PASTE CODE FOR MODEL")
print("="*80)

print("\nfactors = {")
for category in sorted(final_factors.keys()):
    f = final_factors[category]
    print(f"    '{category}': {{'co2': {f['co2']:.2f}, 'land': {f['land']:.2f}, 'water': {f['water']:.0f}, 'scope12': {f['scope12']:.2f}}},")
print("}")

print("\n✅ EXTRACTION COMPLETE")
