"""
Extract LCA factors from RIVM database and map to model categories.
Handles multiple product entries and preparation methods to get representative values.
"""

import pandas as pd
import numpy as np

def load_rivm_lca_database():
    """Load RIVM Environmental Impact Database."""
    print("\n" + "="*80)
    print("LOADING RIVM LCA DATABASE")
    print("="*80 + "\n")
    
    # Load database with proper delimiter and encoding
    df = pd.read_csv(
        'Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv',
        sep=';',
        encoding='utf-8',
        skiprows=2  # Skip the metadata header rows
    )
    
    print(f"✓ Loaded {len(df)} RIVM product entries")
    print(f"✓ Columns: {list(df.columns[:12])}")
    
    # Rename columns for clarity
    df.columns = [col.strip() for col in df.columns]
    
    # Find the columns we need
    name_col = 'Naam'
    co2_col = 'kg CO2 eq'
    land_col = 'm2a crop eq'
    water_col = 'm3'
    
    # Convert to numeric (handle European decimal format)
    for col in [co2_col, land_col, water_col]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(',', '.'),
            errors='coerce'
        )
    
    print(f"✓ Using columns: CO2={co2_col}, Land={land_col}, Water={water_col}")
    print()
    
    return df, name_col, co2_col, land_col, water_col

def map_rivm_to_model_categories(df, name_col, co2_col, land_col, water_col):
    """
    Map RIVM products to model food categories.
    Uses product name matching to group similar items.
    """
    
    # Define search terms for each food item
    PRODUCT_SEARCH = {
        'Beef': ['Beef', 'Rundvlees', 'Steak', 'Veal', 'Kalfsvlees'],
        'Pork': ['Pork', 'Varkensvlees', 'Ham', 'Bacon', 'Spek'],
        'Lamb': ['Lamb', 'Lamsvlees', 'Mutton', 'Schaap'],
        'Chicken': ['Chicken', 'Kip', 'Poultry', 'Gevogelte'],
        'Fish': ['Fish', 'Vis', 'Salmon', 'Zalm', 'Cod', 'Kabeljauw', 'Tuna', 'Tonijn'],
        'Eggs': ['Egg', 'Ei'],
        'Cheese': ['Cheese', 'Kaas', 'Gouda', 'Edam'],
        'Milk': ['Milk', 'Melk'],
        'Dairy': ['Yogurt', 'Yoghurt', 'Custard', 'Vla'],
        'Pulses': ['Bean', 'Bonen', 'Lentil', 'Linzen', 'Chickpea', 'Kikkererwt'],
        'Nuts': ['Nut', 'Noten', 'Almond', 'Amandel', 'Walnut', 'Walnoot'],
        'Grains': ['Wheat', 'Tarwe', 'Oats', 'Haver', 'Barley', 'Gerst'],
        'Bread': ['Bread', 'Brood'],
        'Pasta': ['Pasta', 'Macaroni', 'Spaghetti'],
        'Rice': ['Rice', 'Rijst'],
        'Potatoes': ['Potato', 'Aardappel'],
        'Vegetables': ['Vegetable', 'Groente', 'Carrot', 'Wortel', 'Tomato', 'Tomaat', 'Broccoli'],
        'Fruits': ['Fruit', 'Apple', 'Appel', 'Banana', 'Banaan', 'Orange', 'Sinaasappel'],
        'Sugar': ['Sugar', 'Suiker'],
        'Processed': ['Pizza', 'Soup', 'Soep', 'Sauce', 'Saus'],
        'Snacks': ['Chips', 'Crisp', 'Cookie', 'Koek'],
        'Coffee': ['Coffee', 'Koffie'],
        'Tea': ['Tea', 'Thee'],
        'Alcohol': ['Beer', 'Bier', 'Wine', 'Wijn', 'Spirit'],
        'Butter': ['Butter', 'Boter'],
        'Oils': ['Oil', 'Olie', 'Sunflower', 'Zonnebloem', 'Olive', 'Olijf'],
    }
    
    print("MAPPING PRODUCTS TO CATEGORIES")
    print("="*80 + "\n")
    
    category_data = {cat: [] for cat in PRODUCT_SEARCH.keys()}
    
    for product_name, search_terms in PRODUCT_SEARCH.items():
        matches = pd.DataFrame()
        
        # Find all products matching this category
        for term in search_terms:
            mask = df[name_col].str.contains(term, case=False, na=False, regex=False)
            matches = pd.concat([matches, df[mask]])
        
        # Remove duplicates
        matches = matches.drop_duplicates(subset=[name_col])
        
        if len(matches) > 0:
            # Extract valid values
            co2_values = matches[co2_col].dropna()
            land_values = matches[land_col].dropna()
            water_values = matches[water_col].dropna()
            
            if len(co2_values) > 0:
                # Store all matches for category
                category_data[product_name] = {
                    'co2_values': co2_values.values,
                    'land_values': land_values.values,
                    'water_values': water_values.values,
                    'products_found': len(matches)
                }
                
                print(f"✅ {product_name:20} | {len(matches):3} products | "
                      f"CO2: {co2_values.median():.2f} kg (median)")
    
    return category_data

def calculate_factors(category_data, scope12_values):
    """
    Calculate final factors using median values and Monitor calibration.
    """
    
    print("\n" + "="*80)
    print("CALCULATED FACTORS (RIVM + Monitor Calibration)")
    print("="*80 + "\n")
    
    factors = {}
    
    for category, data in category_data.items():
        if data and data['co2_values'].size > 0:
            # Use median for robustness
            co2_median = np.median(data['co2_values'])
            land_median = np.median(data['land_values']) if data['land_values'].size > 0 else 0.0
            water_median = np.median(data['water_values']) if data['water_values'].size > 0 else 0.0
            
            # Get Scope 1+2 from Monitor calibration (from previous work)
            s12 = scope12_values.get(category, co2_median * 0.5)  # Default fallback
            
            factors[category] = {
                'co2': round(co2_median, 2),
                'land': round(land_median, 2),
                'water': round(water_median, 0),
                'scope12': round(s12, 2)
            }
            
            print(f"{category:20} | CO2: {co2_median:6.2f} | Land: {land_median:6.2f} | "
                  f"Water: {water_median:8.0f} | S12: {s12:6.2f}")
    
    return factors

def export_factors_code(factors):
    """Generate Python code for integration."""
    
    print("\n\n" + "="*80)
    print("PYTHON CODE FOR INTEGRATION")
    print("="*80 + "\n")
    
    print("factors = {")
    for category in sorted(factors.keys()):
        f = factors[category]
        print(f"    '{category}': {{'co2': {f['co2']}, 'land': {f['land']}, "
              f"'water': {f['water']}, 'scope12': {f['scope12']}}},")
    print("}")
    
    # Export to CSV for reference
    df_export = pd.DataFrame(factors).T.round(2)
    csv_path = 'rivm_lca_factors_extracted.csv'
    df_export.to_csv(csv_path)
    print(f"\n✅ Exported to: {csv_path}")
    
    return factors

def main():
    print("\n" + "="*80)
    print("RIVM LCA DATABASE EXTRACTOR")
    print("="*80)
    
    # Load RIVM database
    df, name_col, co2_col, land_col, water_col = load_rivm_lca_database()
    
    # Map to model categories
    category_data = map_rivm_to_model_categories(df, name_col, co2_col, land_col, water_col)
    
    # Monitor-calibrated Scope 1+2 percentages (from previous integration)
    scope12_calibration = {
        'Beef': 13.99,
        'Pork': 6.91,
        'Chicken': 1.96,
        'Fish': 2.06,
        'Cheese': 4.42,
        'Milk': 0.77,
        'Dairy': 1.78,
        'Eggs': 0.51,
        'Pulses': 0.5,
        'Nuts': 0.61,
        'Grains': 0.43,
        'Bread': 0.6,
        'Pasta': 0.65,
        'Rice': 0.65,
        'Potatoes': 0.38,
        'Vegetables': 0.26,
        'Fruits': 0.19,
        'Sugar': 0.24,
        'Processed': 0.9,
        'Snacks': 1.2,
        'Coffee': 0.77,
        'Tea': 1.16,
        'Alcohol': 0.22,
        'Butter': 1.78,
        'Oils': 0.56,
    }
    
    # Calculate final factors
    factors = calculate_factors(category_data, scope12_calibration)
    
    # Export code
    export_factors_code(factors)
    
    print("\n" + "="*80)
    print("✅ COMPLETE - Ready to integrate into Master Hybrid Model")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
