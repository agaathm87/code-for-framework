"""
Search RIVM database for missing 8 categories using proxy search terms and synonyms.
Creates mapping for Meat_Subs, Ready_Meals, Instant_Noodles, Instant_Pasta, 
Animal_Fats, Frying_Oil_Animal, Condiment_Sauces, Spice_Mixes
"""

import pandas as pd
import numpy as np

def load_rivm_database():
    """Load RIVM database with proper encoding."""
    df = pd.read_csv(
        'Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv',
        sep=';',
        encoding='utf-8',
        skiprows=2
    )
    
    # Rename columns for clarity
    df.columns = [col.strip() for col in df.columns]
    
    # Convert to numeric (handle European decimal format)
    for col in ['kg CO2 eq', 'm2a crop eq', 'm3']:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(',', '.'),
            errors='coerce'
        )
    
    return df

def search_category(df, search_terms, exclude_terms=None, name_col='Naam'):
    """
    Search for products matching search terms, optionally excluding certain terms.
    Returns all matches with CO2, land, water values.
    """
    if exclude_terms is None:
        exclude_terms = []
    
    matches = pd.DataFrame()
    
    for term in search_terms:
        mask = df[name_col].str.contains(term, case=False, na=False, regex=False)
        matches = pd.concat([matches, df[mask]])
    
    # Remove duplicates
    matches = matches.drop_duplicates(subset=[name_col])
    
    # Exclude unwanted items
    if exclude_terms:
        for term in exclude_terms:
            matches = matches[~matches[name_col].str.contains(term, case=False, na=False, regex=False)]
    
    return matches

def print_matches(category_name, matches, co2_col='kg CO2 eq', land_col='m2a crop eq', water_col='m3', name_col='Naam'):
    """Print results for a category search."""
    if len(matches) == 0:
        print(f"\n❌ {category_name}: NO MATCHES FOUND")
        return None, None, None
    
    co2_values = matches[co2_col].dropna()
    land_values = matches[land_col].dropna()
    water_values = matches[water_col].dropna()
    
    if len(co2_values) == 0:
        print(f"\n❌ {category_name}: NO VALID CO2 DATA")
        return None, None, None
    
    co2_median = co2_values.median()
    land_median = land_values.median() if len(land_values) > 0 else 0
    water_median = water_values.median() if len(water_values) > 0 else 0
    
    print(f"\n✅ {category_name} | {len(matches)} products found")
    print(f"   Median CO2: {co2_median:.2f} kg | Land: {land_median:.2f} m²a | Water: {water_median:.0f} m³")
    print(f"   Products:")
    
    for idx, (_, row) in enumerate(matches.iterrows(), 1):
        if idx <= 5:  # Show first 5 products
            print(f"      {idx}. {row[name_col][:60]} → CO2: {row[co2_col]:.2f}")
    
    if len(matches) > 5:
        print(f"      ... and {len(matches) - 5} more products")
    
    return co2_median, land_median, water_median

def main():
    print("\n" + "="*90)
    print("RIVM DATABASE - PROXY SEARCH FOR MISSING CATEGORIES")
    print("="*90 + "\n")
    
    df = load_rivm_database()
    print(f"✓ Loaded {len(df)} RIVM products\n")
    
    results = {}
    
    # ===== 1. MEAT SUBSTITUTES =====
    print("─" * 90)
    print("1. MEAT SUBSTITUTES / MEAT ALTERNATIVES")
    print("─" * 90)
    
    meat_sub_terms = [
        'vegetarian', 'vegan', 'plant-based', 'meat substitute', 'meat-free',
        'tofu', 'seitan', 'tempeh', 'burger', 'veggie', 'mock meat',
        'soya', 'soy', 'legume-based', 'bean burger', 'lentil burger'
    ]
    matches = search_category(df, meat_sub_terms, exclude_terms=['sausage'])
    co2, land, water = print_matches('Meat_Subs', matches)
    if co2:
        results['Meat_Subs'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== 2. READY MEALS / CONVENIENCE FOODS =====
    print("\n" + "─" * 90)
    print("2. READY MEALS / CONVENIENCE FOODS")
    print("─" * 90)
    
    ready_meal_terms = [
        'ready meal', 'ready-to-eat', 'frozen meal', 'prepared meal',
        'convenience', 'heat and eat', 'microwave', 'dish', 'recipe'
    ]
    ready_meal_exclude = ['beer', 'wine', 'juice', 'milk', 'bread', 'butter']
    matches = search_category(df, ready_meal_terms, exclude_terms=ready_meal_exclude)
    co2, land, water = print_matches('Ready_Meals', matches)
    if co2:
        results['Ready_Meals'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== 3. INSTANT NOODLES =====
    print("\n" + "─" * 90)
    print("3. INSTANT NOODLES")
    print("─" * 90)
    
    instant_noodle_terms = [
        'instant noodle', 'ramen', 'noodle soup', 'instant pasta', 'cup noodle',
        'dried noodle', 'egg noodle', 'wheat noodle', 'pasta', 'macaroni'
    ]
    instant_noodle_exclude = ['fresh', 'refrigerated']
    matches = search_category(df, instant_noodle_terms, exclude_terms=instant_noodle_exclude)
    co2, land, water = print_matches('Instant_Noodles', matches)
    if co2:
        results['Instant_Noodles'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== 4. INSTANT PASTA =====
    print("\n" + "─" * 90)
    print("4. INSTANT PASTA (DRIED)")
    print("─" * 90)
    
    instant_pasta_terms = [
        'pasta', 'spaghetti', 'macaroni', 'penne', 'farfalle', 'fettuccine',
        'dried pasta', 'pasta dry', 'durum wheat'
    ]
    instant_pasta_exclude = ['fresh', 'egg pasta', 'instant noodle', 'ramen', 'soup']
    matches = search_category(df, instant_pasta_terms, exclude_terms=instant_pasta_exclude)
    co2, land, water = print_matches('Instant_Pasta', matches)
    if co2:
        results['Instant_Pasta'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== 5. ANIMAL FATS =====
    print("\n" + "─" * 90)
    print("5. ANIMAL FATS (TALLOW, LARD, etc.)")
    print("─" * 90)
    
    animal_fat_terms = [
        'tallow', 'lard', 'shortening', 'beef fat', 'pork fat', 'fat',
        'suet', 'dripping', 'schmaltz', 'rendered fat'
    ]
    animal_fat_exclude = ['butter', 'vegetable', 'oil', 'margarine', 'spread']
    matches = search_category(df, animal_fat_terms, exclude_terms=animal_fat_exclude)
    co2, land, water = print_matches('Animal_Fats', matches)
    if co2:
        results['Animal_Fats'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== 6. FRYING OIL (ANIMAL-BASED) =====
    print("\n" + "─" * 90)
    print("6. FRYING OIL - ANIMAL BASED")
    print("─" * 90)
    
    frying_oil_animal_terms = [
        'animal oil', 'beef oil', 'fish oil', 'lard oil', 'rendered oil',
        'deep fry', 'frying fat', 'frying oil'
    ]
    frying_oil_exclude = ['vegetable', 'plant', 'sunflower', 'olive', 'coconut', 'palm']
    matches = search_category(df, frying_oil_animal_terms, exclude_terms=frying_oil_exclude)
    co2, land, water = print_matches('Frying_Oil_Animal', matches)
    if co2:
        results['Frying_Oil_Animal'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== 7. CONDIMENTS & SAUCES =====
    print("\n" + "─" * 90)
    print("7. CONDIMENTS & SAUCES")
    print("─" * 90)
    
    condiment_terms = [
        'sauce', 'condiment', 'ketchup', 'mustard', 'mayo', 'mayonnaise',
        'salad dressing', 'pesto', 'vinegar', 'soy sauce', 'worcester'
    ]
    condiment_exclude = ['butter', 'oil', 'spread']
    matches = search_category(df, condiment_terms, exclude_terms=condiment_exclude)
    co2, land, water = print_matches('Condiment_Sauces', matches)
    if co2:
        results['Condiment_Sauces'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== 8. SPICE MIXES =====
    print("\n" + "─" * 90)
    print("8. SPICE MIXES / SEASONINGS")
    print("─" * 90)
    
    spice_terms = [
        'spice', 'seasoning', 'herb', 'curry', 'mixed spice', 'bouillon',
        'stock cube', 'seasoning mix', 'spice blend', 'dried herb',
        'peppercorn', 'garlic powder', 'onion powder'
    ]
    spice_exclude = ['sugar', 'salt', 'bread']
    matches = search_category(df, spice_terms, exclude_terms=spice_exclude)
    co2, land, water = print_matches('Spice_Mixes', matches)
    if co2:
        results['Spice_Mixes'] = {'co2': co2, 'land': land, 'water': water}
    
    # ===== SUMMARY =====
    print("\n\n" + "="*90)
    print("SUMMARY - FOUND PROXIES FOR MISSING CATEGORIES")
    print("="*90 + "\n")
    
    print(f"{'Category':<25} {'Found?':>10} {'CO2':>10} {'Land':>10} {'Water':>12}")
    print("-" * 70)
    
    found_count = 0
    missing_categories = ['Meat_Subs', 'Ready_Meals', 'Instant_Noodles', 'Instant_Pasta',
                         'Animal_Fats', 'Frying_Oil_Animal', 'Condiment_Sauces', 'Spice_Mixes']
    
    for cat in missing_categories:
        if cat in results:
            found_count += 1
            data = results[cat]
            print(f"{cat:<25} {'✅ YES':>10} {data['co2']:>10.2f} {data['land']:>10.2f} {data['water']:>12.0f}")
        else:
            print(f"{cat:<25} {'❌ NO':>10}")
    
    print(f"\nTotal found: {found_count}/8")
    
    # Export as Python code
    print("\n\n" + "="*90)
    print("PYTHON CODE FOR FOUND PROXIES")
    print("="*90 + "\n")
    
    print("# Update missing_categories dict in rivm_complete_factors.py with:")
    print("missing_categories = {")
    
    for cat in missing_categories:
        if cat in results:
            data = results[cat]
            print(f"    '{cat}': {{'co2': {data['co2']}, 'land': {data['land']}, 'water': {data['water']}, 'scope12': ???}},")
        else:
            print(f"    '{cat}': {{# NO RIVM PROXY FOUND - USE LITERATURE ESTIMATE}}")
    
    print("}")
    
    # Export to CSV
    if results:
        df_results = pd.DataFrame(results).T
        csv_path = 'rivm_missing_categories_proxies.csv'
        df_results.to_csv(csv_path)
        print(f"\n✅ Exported to: {csv_path}")
    
    print("\n" + "="*90 + "\n")

if __name__ == '__main__':
    main()
