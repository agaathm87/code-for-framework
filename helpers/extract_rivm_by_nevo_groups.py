"""
Extract RIVM environmental factors and aggregate by NEVO product groups.
Map to model's 33 categories and save comprehensive CSVs.
"""
import csv
import statistics
from collections import defaultdict

print("="*80)
print("RIVM DATABASE EXTRACTION & NEVO PRODUCT GROUP AGGREGATION")
print("="*80)

# ============================================================================
# STEP 1: Load RIVM database
# ============================================================================
rivm_file = "Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv"
print(f"\nLoading: {rivm_file}")

with open(rivm_file, 'r', encoding='latin-1') as f:
    lines = f.readlines()

# Parse header (row 3)
header = lines[2].strip().split(';')

# Find column indices
col_name_idx = header.index('Naam')
col_co2_idx = header.index('kg CO2 eq')
col_land_idx = header.index('m2a crop eq')
col_water_idx = header.index('m3')
col_nevo_group_idx = header.index('NEVO productgroep')

print(f"Columns found: Name, CO2, Land, Water, NEVO Group")

# Parse all products
all_products = []
for line in lines[3:]:
    row = line.strip().split(';')
    if len(row) > max(col_co2_idx, col_land_idx, col_water_idx, col_nevo_group_idx):
        try:
            name = row[col_name_idx].strip()
            nevo_group = row[col_nevo_group_idx].strip()
            
            co2_str = row[col_co2_idx].replace(',', '.')
            land_str = row[col_land_idx].replace(',', '.')
            water_str = row[col_water_idx].replace(',', '.')
            
            co2 = float(co2_str) if co2_str else None
            land = float(land_str) if land_str else None
            water = float(water_str) if water_str else None
            
            if co2 is not None:  # Only keep products with CO2 data
                all_products.append({
                    'name': name,
                    'nevo_group': nevo_group,
                    'co2': co2,
                    'land': land if land else 0,
                    'water': water if water else 0
                })
        except:
            continue

print(f"Total products loaded: {len(all_products)}")

# ============================================================================
# STEP 2: Group by NEVO product groups and calculate statistics
# ============================================================================
print("\n" + "="*80)
print("AGGREGATING BY NEVO PRODUCT GROUPS")
print("="*80)

nevo_groups = defaultdict(list)
for product in all_products:
    if product['nevo_group']:  # Only if group exists
        nevo_groups[product['nevo_group']].append(product)

print(f"\nUnique NEVO product groups: {len(nevo_groups)}")

# Calculate aggregated statistics for each NEVO group
nevo_aggregated = {}
for group, products in sorted(nevo_groups.items()):
    co2_values = [p['co2'] for p in products]
    land_values = [p['land'] for p in products if p['land'] > 0]
    water_values = [p['water'] for p in products if p['water'] > 0]
    
    nevo_aggregated[group] = {
        'n_products': len(products),
        'co2_median': statistics.median(co2_values),
        'co2_mean': statistics.mean(co2_values),
        'co2_min': min(co2_values),
        'co2_max': max(co2_values),
        'land_median': statistics.median(land_values) if land_values else 0,
        'land_mean': statistics.mean(land_values) if land_values else 0,
        'water_median': statistics.median(water_values) if water_values else 0,
        'water_mean': statistics.mean(water_values) if water_values else 0,
        'products': products
    }

print(f"\n{'NEVO Product Group':<40} {'Products':<10} {'CO2 (median)':<15} {'Land (median)':<15} {'Water (median)'}")
print("-"*100)
for group, data in sorted(nevo_aggregated.items()):
    print(f"{group:<40} {data['n_products']:<10} {data['co2_median']:<15.2f} {data['land_median']:<15.2f} {data['water_median']:<15.2f}")

# ============================================================================
# STEP 3: Map NEVO groups to model's 33 categories
# ============================================================================
print("\n" + "="*80)
print("MAPPING NEVO GROUPS TO MODEL CATEGORIES (33 categories)")
print("="*80)

# Mapping NEVO product groups -> Model categories
nevo_to_model = {
    'Vlees, vleeswaren en gevogelte': ['Beef', 'Pork', 'Chicken', 'Processed'],
    'Vis': ['Fish'],
    'Eieren': ['Eggs'],
    'Melk en melkproducten': ['Milk', 'Dairy', 'Cheese', 'Butter'],
    'Peulvruchten': ['Pulses'],
    'Noten en zaden': ['Nuts'],
    'Granen en graanproducten': ['Grains', 'Rice', 'Pasta', 'Bread'],
    'Aardappelen en knolgewassen': ['Potatoes'],
    'Groenten': ['Vegetables'],
    'Fruit': ['Fruits'],
    'Suiker en suikerproducten': ['Sugar'],
    'Oliën en vetten': ['Oils', 'Animal_Fats', 'Frying_Oil_Animal'],
    'Alcoholische dranken': ['Alcohol'],
    'Koffie en thee': ['Coffee', 'Tea'],
    'Diversen': ['Meat_Subs', 'Condiment_Sauces', 'Spice_Mixes'],
    'Brood': ['Bread'],
    'Flesvoeding en preparaten': ['Ready_Meals'],
}

# Additional keyword-based mapping for granular categories
model_category_keywords = {
    'Beef': ['beef', 'rund', 'steak', 'rosbief', 'biefstuk'],
    'Pork': ['pork', 'varken', 'ham', 'bacon', 'spek'],
    'Chicken': ['chicken', 'kip', 'poultry', 'gevogelte'],
    'Fish': ['fish', 'vis', 'salmon', 'tuna', 'zalm', 'tonijn'],
    'Eggs': ['egg', 'ei ', 'eieren'],
    'Milk': ['milk', 'melk'],
    'Dairy': ['yoghurt', 'yogurt', 'kwark', 'vla', 'pudding'],
    'Cheese': ['cheese', 'kaas'],
    'Butter': ['butter', 'boter'],
    'Grains': ['grain', 'graan', 'cereal', 'muesli', 'haver'],
    'Rice': ['rice', 'rijst'],
    'Pasta': ['pasta', 'macaroni', 'spaghetti'],
    'Bread': ['bread', 'brood', 'bun', 'roll', 'baguette'],
    'Vegetables': ['vegetable', 'groente', 'tomato', 'carrot', 'lettuce', 'cucumber'],
    'Fruits': ['fruit', 'apple', 'banana', 'orange', 'strawberr', 'grape'],
    'Potatoes': ['potato', 'aardappel', 'frites', 'chips frozen'],
    'Nuts': ['nuts', 'noten', 'peanut', 'almond', 'cashew', 'walnut'],
    'Pulses': ['beans', 'bonen', 'lentil', 'chickpea', 'pea ', 'soy'],
    'Oils': ['oil sunflower', 'oil olive', 'olie'],
    'Processed': ['sausage', 'worst', 'salami', 'liver'],
    'Snacks': ['chips', 'cookie', 'koek', 'biscuit', 'chocolate'],
    'Sugar': ['sugar', 'suiker', 'honey', 'jam'],
    'Coffee': ['coffee', 'koffie'],
    'Tea': ['tea', 'thee'],
    'Alcohol': ['beer', 'bier', 'wine', 'wijn', 'whisky', 'gin'],
    'Ready_Meals': ['ready', 'prepared', 'wrap', 'tortilla'],
    'Meat_Subs': ['vegetarian', 'burger', 'tofu', 'tempeh'],
    'Condiment_Sauces': ['sauce', 'saus', 'ketchup', 'mayonnaise', 'mustard'],
    'Animal_Fats': ['gravy', 'jus', 'lard', 'mayonnaise'],
    'Spice_Mixes': ['spice', 'bouillon', 'stock', 'cake mix'],
    'Instant_Noodles': ['instant', 'noodle', 'ramen'],
    'Instant_Pasta': ['pasta white', 'pasta with egg'],
    'Frying_Oil_Animal': ['fried', 'deep frying', 'friet'],
}

# Map each product to a model category
model_categories = defaultdict(list)

for product in all_products:
    name_lower = product['name'].lower()
    matched = False
    
    # Try keyword matching
    for category, keywords in model_category_keywords.items():
        if any(kw in name_lower for kw in keywords):
            model_categories[category].append(product)
            matched = True
            break
    
    if not matched:
        # Fallback to NEVO group mapping
        nevo_group = product['nevo_group']
        for nevo, model_cats in nevo_to_model.items():
            if nevo == nevo_group:
                # Assign to first category in list
                model_categories[model_cats[0]].append(product)
                break

# Calculate aggregated values for model categories
model_aggregated = {}

print(f"\n{'Model Category':<25} {'Products':<10} {'CO2':<12} {'Land':<12} {'Water':<12}")
print("-"*75)

for category in sorted(model_categories.keys()):
    products = model_categories[category]
    
    if len(products) > 0:
        co2_values = [p['co2'] for p in products]
        land_values = [p['land'] for p in products if p['land'] > 0]
        water_values = [p['water'] for p in products if p['water'] > 0]
        
        model_aggregated[category] = {
            'n_products': len(products),
            'co2_median': statistics.median(co2_values),
            'land_median': statistics.median(land_values) if land_values else 0,
            'water_median': statistics.median(water_values) * 1000 if water_values else 0,  # m3 to liters
            'products': products
        }
        
        print(f"{category:<25} {len(products):<10} {model_aggregated[category]['co2_median']:<12.2f} "
              f"{model_aggregated[category]['land_median']:<12.2f} {model_aggregated[category]['water_median']:<12.0f}")

# ============================================================================
# STEP 4: Save CSVs
# ============================================================================
print("\n" + "="*80)
print("SAVING CSV FILES")
print("="*80)

# CSV 1: NEVO product groups aggregated
csv1_file = "rivm_nevo_groups_aggregated.csv"
with open(csv1_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['NEVO_Product_Group', 'N_Products', 'CO2_Median_kg', 'CO2_Mean_kg', 'CO2_Min_kg', 'CO2_Max_kg',
                     'Land_Median_m2', 'Land_Mean_m2', 'Water_Median_m3', 'Water_Mean_m3'])
    
    for group, data in sorted(nevo_aggregated.items()):
        writer.writerow([
            group, data['n_products'],
            round(data['co2_median'], 2), round(data['co2_mean'], 2),
            round(data['co2_min'], 2), round(data['co2_max'], 2),
            round(data['land_median'], 2), round(data['land_mean'], 2),
            round(data['water_median'], 4), round(data['water_mean'], 4)
        ])

print(f"✅ Saved: {csv1_file}")

# CSV 2: Model categories aggregated
csv2_file = "rivm_model_categories_aggregated.csv"
with open(csv2_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Model_Category', 'N_Products', 'CO2_Total_kg', 'Land_m2', 'Water_Liters'])
    
    for category, data in sorted(model_aggregated.items()):
        writer.writerow([
            category, data['n_products'],
            round(data['co2_median'], 2),
            round(data['land_median'], 2),
            round(data['water_median'], 0)
        ])

print(f"✅ Saved: {csv2_file}")

# CSV 3: Detailed product listing by model category
csv3_file = "rivm_products_by_model_category.csv"
with open(csv3_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Model_Category', 'Product_Name', 'NEVO_Group', 'CO2_kg', 'Land_m2', 'Water_m3'])
    
    for category in sorted(model_categories.keys()):
        for product in model_categories[category]:
            writer.writerow([
                category,
                product['name'],
                product['nevo_group'],
                round(product['co2'], 3),
                round(product['land'], 3),
                round(product['water'], 4)
            ])

print(f"✅ Saved: {csv3_file}")

# CSV 4: Python dictionary for model
csv4_file = "rivm_model_factors_dict.csv"
with open(csv4_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Model_Category', 'CO2_Total', 'Land_m2', 'Water_L', 'N_Products', 'Sample_Products'])
    
    for category, data in sorted(model_aggregated.items()):
        sample_products = ', '.join([p['name'][:30] for p in data['products'][:3]])
        writer.writerow([
            category,
            round(data['co2_median'], 2),
            round(data['land_median'], 2),
            round(data['water_median'], 0),
            data['n_products'],
            sample_products
        ])

print(f"✅ Saved: {csv4_file}")

# ============================================================================
# STEP 5: Generate Python dict for model
# ============================================================================
print("\n" + "="*80)
print("PYTHON DICTIONARY (copy-paste to model)")
print("="*80)

print("\n# RIVM factors by model category (total lifecycle CO2)")
print("rivm_factors = {")
for category, data in sorted(model_aggregated.items()):
    print(f"    '{category}': {{'co2_total': {data['co2_median']:.2f}, "
          f"'land': {data['land_median']:.2f}, "
          f"'water': {data['water_median']:.0f}, "
          f"'n_products': {data['n_products']}}},")
print("}")

print("\n" + "="*80)
print("EXTRACTION COMPLETE")
print("="*80)
print(f"\nFiles created:")
print(f"  1. {csv1_file} - NEVO groups aggregated")
print(f"  2. {csv2_file} - Model categories aggregated")
print(f"  3. {csv3_file} - Detailed product listing")
print(f"  4. {csv4_file} - Model factors dict")
