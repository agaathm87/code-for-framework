"""
Search RIVM database with expanded proxy terms for missing categories.
Focuses on: Meat_Subs, Instant_Noodles, Instant_Pasta, Animal_Fats, Frying_Oil_Animal
"""

import pandas as pd
import os
from pathlib import Path

# Define expanded search proxies for missing categories
PROXY_TERMS = {
    'Meat_Subs': [
        'Vegetarian burger', 'Tofu', 'Tempeh', 'Vleesvervanger',
        'Plant-based meat', 'Mock meat', 'Seitan', 'Plant meat', 
        'Meat substitute', 'Vegetarian', 'Vegan burger',
        'Plantaardig vlees', 'Vegetarisch'
    ],
    'Instant_Noodles': [
        'Noodles', 'Pasta dried', 'Pasta unprepared', 'Noedels',
        'Macaroni', 'Spaghetti', 'Tagliatelle'
    ],
    'Instant_Pasta': [
        'Pasta dried', 'Pasta unprepared', 'Macaroni', 'Spaghetti',
        'Tagliatelle', 'Penne', 'Fusilli', 'Pasta product'
    ],
    'Animal_Fats': [
        'Butter', 'Lard', 'Boter', 'Ghee', 
        'Butter salted', 'Butter unsalted', 'Cooking fat',
        'Animal fat', 'Margarine'
    ],
    'Frying_Oil_Animal': [
        'Oil', 'Cooking oil', 'Frying oil', 'Olie', 
        'Sunflower oil', 'Rapeseed oil', 'Vegetable oil',
        'Peanut oil', 'Olive oil', 'Frituurolie'
    ]
}

def search_rivm_database(proxies_dict):
    """
    Search RIVM database for products matching proxy terms.
    Returns matches by category.
    """
    
    # Find RIVM database file - check datasets folder first
    dataset_path = Path('../datasets/Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv')
    if dataset_path.exists():
        rivm_file = dataset_path
    else:
        # Fallback to current directory
        db_files = list(Path('.').glob('Database milieubelasting*.csv'))
        if not db_files:
            print("❌ RIVM database CSV not found")
            print(f"   Checked: {dataset_path.absolute()}")
            print(f"   Current directory: {os.getcwd()}")
            return {}
        rivm_file = db_files[0]
    
    print(f"✓ Found RIVM database: {rivm_file.absolute()}")
    print()
    
    # Load RIVM database (skip 2 header rows, use semicolon delimiter like rivm_lca_loader.py)
    try:
        df = pd.read_csv(rivm_file, skiprows=2, sep=';', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(rivm_file, skiprows=2, sep=';', encoding='latin-1')
    
    print(f"✓ Loaded {len(df)} RIVM products")
    print(f"✓ Columns: {list(df.columns[:5])}...")  # Show first 5 columns
    print()
    
    # Use first column as product name (Dutch product names)
    product_col = df.columns[0]  
    co2_col = df.columns[3]  # 4th column is typically CO2_kg
    
    print(f"✓ Using product column: '{product_col}'")
    print(f"✓ Using CO2 column: '{co2_col}'")
    print()
    
    df['product_lower'] = df[product_col].astype(str).str.lower()
    
    results = {}
    
    for category, proxies in proxies_dict.items():
        print(f"\n{'='*70}")
        print(f"Searching for: {category}")
        print(f"{'='*70}")
        
        matches = []
        
        for proxy in proxies:
            proxy_lower = proxy.lower()
            # Search for products containing this proxy term
            mask = df['product_lower'].str.contains(proxy_lower, case=False, na=False)
            category_matches = df[mask]
            
            if len(category_matches) > 0:
                for idx, row in category_matches.iterrows():
                    product_name = row[product_col]
                    co2_val = row[co2_col]
                    
                    # Convert European number format (comma to dot)
                    if isinstance(co2_val, str):
                        co2_val = co2_val.replace(',', '.')
                    try:
                        co2_val = float(co2_val)
                    except:
                        co2_val = None
                    
                    matches.append({
                        'product': product_name,
                        'proxy_term': proxy,
                        'co2': co2_val
                    })
        
        if matches:
            print(f"✅ Found {len(matches)} potential matches:")
            print()
            
            # Deduplicate by product name
            unique_matches = {}
            for match in matches:
                if match['product'] not in unique_matches:
                    unique_matches[match['product']] = match
            
            # Sort by CO2 value
            sorted_matches = sorted(
                unique_matches.values(),
                key=lambda x: float(x['co2']) if x['co2'] is not None else 0,
                reverse=True
            )
            
            for i, match in enumerate(sorted_matches[:10], 1):  # Show top 10
                co2_display = f"{float(match['co2']):.2f} kg CO2e/kg" if match['co2'] else "N/A"
                print(f"  {i}. {match['product']}")
                print(f"     → Matched by: '{match['proxy_term']}' ({co2_display})")
            
            if len(sorted_matches) > 10:
                print(f"  ... and {len(sorted_matches) - 10} more matches")
            
            # Store best match (highest CO2 value)
            best = sorted_matches[0]
            results[category] = {
                'product': best['product'],
                'co2': best['co2'],
                'num_matches': len(sorted_matches)
            }
        else:
            print(f"❌ No matches found with any proxy terms")
            results[category] = None
    
    return results

def main():
    print("\n" + "="*70)
    print("RIVM DATABASE PROXY SEARCH - MISSING CATEGORIES")
    print("="*70 + "\n")
    
    # Run search
    results = search_rivm_database(PROXY_TERMS)
    
    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY - RECOMMENDED MATCHES")
    print("="*70 + "\n")
    
    for category, result in results.items():
        if result:
            co2_display = f"{float(result['co2']):.2f} kg CO2e/kg" if result['co2'] else "N/A"
            print(f"✅ {category:20} → {result['product']:40} ({co2_display})")
            print(f"   [{result['num_matches']} total matches found]")
        else:
            print(f"❌ {category:20} → No RIVM match found")
    
    # Export recommendations
    print(f"\n\n{'='*70}")
    print("RECOMMENDED INTEGRATION VALUES")
    print("="*70 + "\n")
    
    print("Add to load_lca_factors() for missing categories:\n")
    
    for category, result in results.items():
        if result:
            co2 = float(result['co2'])
            scope12_pct = 45  # Default estimate for processed/substitute foods
            scope12 = co2 * (scope12_pct / 100)
            print(f"factors['{category}'] = {{")
            print(f"    'co2': {co2:.2f},  # From RIVM: {result['product']}")
            print(f"    'scope12': {scope12:.2f},  # Estimated {scope12_pct}%")
            print(f"    'land': 0.0,  # Not available")
            print(f"    'water': 0.0  # Not available")
            print(f"}}")
            print()
        else:
            print(f"# {category} - NO MATCH FOUND - Use industry average or literature")
            print(f"factors['{category}'] = {{")
            print(f"    'co2': 3.0,  # PLACEHOLDER - Needs research")
            print(f"    'scope12': 1.35,  # Estimated")
            print(f"    'land': 0.0,")
            print(f"    'water': 0.0")
            print(f"}}")
            print()

if __name__ == '__main__':
    main()
