"""
RIVM LCA Database Loader
Converts RIVM environmental impact database to model-compatible emission factors

This module processes the RIVM "Database milieubelasting voedingsmiddelen" CSV 
and maps it to the food categories used in the Amsterdam Model.

Database columns:
- Global warming: kg CO2 eq per kg product (consumed)
- Land use: m²a crop eq per kg
- Water consumption: m³ per kg
- Product groups: Meat, Dairy, Bread, Fruits, Vegetables, etc.

Output format matches existing factors dictionary:
    {'Beef': {'co2': X, 'land': Y, 'water': Z, 'scope12': W}, ...}

Usage:
    from rivm_lca_loader import load_rivm_factors
    factors = load_rivm_factors()
    
Author: Challenge Based Project Team
Date: January 2026
"""

import pandas as pd
import numpy as np
import os


def load_rivm_database(csv_path=None):
    """
    Load RIVM LCA database from CSV file.
    
    Args:
        csv_path: Path to RIVM CSV file. If None, uses default location.
        
    Returns:
        pd.DataFrame: Raw RIVM database with Dutch and English product names
    """
    if csv_path is None:
        # Default path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, '..', 'datasets', 
                                'Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv')
    
    # Read CSV, skipping header rows (first 2 rows are headers)
    df = pd.read_csv(csv_path, skiprows=2, sep=';', encoding='utf-8')
    
    # Clean column names - based on actual CSV structure
    df.columns = ['Product_NL', 'Unit', 'Effect_Category', 'CO2_kg', 'Acidification_kg', 
                  'Freshwater_Eutro_kg', 'Marine_Eutro_kg', 'Land_m2a', 'Water_m3',
                  'NEVO_Code', 'NEVO_Name_NL', 'NEVO_Group_NL', 'NEVO_Name_EN', 'NEVO_Group_EN', 
                  'Extra_Col']  # Extra column in source data
    
    # Drop the extra column if it exists
    if 'Extra_Col' in df.columns:
        df = df.drop(columns=['Extra_Col'])
    
    # Convert numeric columns (replace commas with dots for European format)
    numeric_cols = ['CO2_kg', 'Acidification_kg', 'Freshwater_Eutro_kg', 
                    'Marine_Eutro_kg', 'Land_m2a', 'Water_m3']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
    
    return df


def map_rivm_to_categories():
    """
    Define mapping from RIVM product names/groups to model food categories.
    
    Returns:
        dict: Mapping of RIVM product patterns to model categories
    """
    # Mapping uses English NEVO names for clarity
    # Format: 'Model_Category': [list of RIVM product name patterns]
    
    mapping = {
        # RED MEAT
        'Beef': [
            'beef', 'veal', 'rundvlees', 'kalfsvlees', 'rund',
            'steak', 'hamburger', 'biefstuk'
        ],
        'Pork': [
            'pork', 'varken', 'bacon', 'ham', 'worst', 'sausage',
            'spek', 'salami'
        ],
        'Lamb': [
            'lamb', 'lam', 'sheep', 'schaap', 'mutton'
        ],
        
        # POULTRY
        'Chicken': [
            'chicken', 'kip', 'poultry', 'gevogelte', 'turkey', 'kalkoen'
        ],
        
        # FISH
        'Fish': [
            'fish', 'vis', 'salmon', 'zalm', 'tuna', 'tonijn',
            'cod', 'kabeljauw', 'haring', 'herring', 'seafood'
        ],
        
        # DAIRY
        'Cheese': [
            'cheese', 'kaas', 'cheddar', 'gouda', 'brie'
        ],
        'Milk': [
            'milk', 'melk', 'yogurt', 'yoghurt', 'kwark', 'quark',
            'buttermilk', 'karnemelk'
        ],
        'Dairy': [
            'dairy', 'zuivel', 'cream', 'room'
        ],
        'Butter': [
            'butter', 'boter'
        ],
        
        # EGGS
        'Eggs': [
            'egg', 'ei', 'eieren'
        ],
        
        # PLANT PROTEIN
        'Pulses': [
            'beans', 'bonen', 'lentils', 'linzen', 'chickpeas', 'kikkererwten',
            'peas', 'erwten', 'legumes', 'peulvruchten'
        ],
        'Nuts': [
            'nuts', 'noten', 'almonds', 'amandelen', 'walnuts', 'walnoten',
            'peanuts', 'pinda', 'cashew', 'hazelnut', 'hazelnoot'
        ],
        'Meat_Subs': [
            'tofu', 'tempeh', 'seitan', 'meat substitute', 'vleesvervangers',
            'veggie burger', 'vegetarische'
        ],
        
        # GRAINS & STAPLES
        'Grains': [
            'grain', 'graan', 'oats', 'haver', 'barley', 'gerst',
            'wheat', 'tarwe', 'rye', 'rogge', 'quinoa'
        ],
        'Bread': [
            'bread', 'brood', 'roll', 'broodje', 'baguette', 'croissant',
            'crispbread', 'knackebrod', 'beschuit'
        ],
        'Pasta': [
            'pasta', 'noodles', 'noedel', 'spaghetti', 'macaroni'
        ],
        'Rice': [
            'rice', 'rijst'
        ],
        
        # VEGETABLES & FRUITS
        'Vegetables': [
            'vegetables', 'groente', 'vegetable', 'tomato', 'tomaat',
            'lettuce', 'sla', 'carrot', 'wortel', 'onion', 'ui',
            'pepper', 'paprika', 'cucumber', 'komkommer', 'cabbage', 'kool'
        ],
        'Fruits': [
            'fruit', 'apple', 'appel', 'banana', 'banaan', 'orange', 'sinaasappel',
            'strawberry', 'aardbei', 'grape', 'druif', 'pear', 'peer',
            'peach', 'perzik', 'kiwi', 'mango', 'melon', 'meloen'
        ],
        'Potatoes': [
            'potato', 'aardappel', 'fries', 'chips'
        ],
        
        # PROCESSED FOODS
        'Processed': [
            'processed', 'verwerkt', 'canned', 'blik', 'frozen', 'diepvries'
        ],
        'Snacks': [
            'snack', 'chips', 'crisps', 'biscuit', 'cookie', 'koek'
        ],
        'Ready_Meals': [
            'ready meal', 'kant-en-klaar', 'prepared', 'bereid'
        ],
        'Instant_Noodles': [
            'instant noodles', 'instant noedel'
        ],
        'Instant_Pasta': [
            'instant pasta'
        ],
        
        # BEVERAGES & ADDITIONS
        'Coffee': [
            'coffee', 'koffie'
        ],
        'Tea': [
            'tea', 'thee'
        ],
        'Alcohol': [
            'beer', 'bier', 'wine', 'wijn', 'alcohol', 'whisky', 'gin', 'jenever'
        ],
        'Sugar': [
            'sugar', 'suiker', 'honey', 'honing', 'syrup', 'siroop'
        ],
        
        # FATS & OILS
        'Oils': [
            'oil', 'olie', 'olive oil', 'olijfolie', 'sunflower', 'zonnebloem'
        ],
        'Animal_Fats': [
            'animal fat', 'dierlijk vet', 'lard', 'reuzel'
        ],
        'Frying_Oil_Animal': [
            'frying oil animal', 'frituurvet dierlijk'
        ],
        
        # CONDIMENTS
        'Condiment_Sauces': [
            'sauce', 'saus', 'ketchup', 'mayonnaise', 'mayo', 'mustard', 'mosterd'
        ],
        'Spice_Mixes': [
            'spice', 'kruiden', 'herbs', 'seasoning', 'kruidenmix'
        ],
        'Condiments': [
            'condiment', 'vinegar', 'azijn', 'salt', 'zout'
        ]
    }
    
    return mapping


def aggregate_rivm_by_category(df, mapping, method='median'):
    """
    Aggregate RIVM database values to model food categories.
    
    Args:
        df: RIVM database DataFrame
        mapping: Category mapping dictionary
        method: Aggregation method ('median', 'mean', 'conservative')
                - 'median': Use median value (robust to outliers)
                - 'mean': Use average value
                - 'conservative': Use 75th percentile (precautionary principle)
    
    Returns:
        dict: Aggregated factors matching model structure
    """
    factors = {}
    
    for category, patterns in mapping.items():
        # Find all matching products
        mask = df['NEVO_Name_EN'].str.lower().str.contains('|'.join(patterns), 
                                                           case=False, na=False, regex=True)
        matched = df[mask]
        
        if len(matched) == 0:
            # No matches found, use fallback/default values
            print(f"⚠ Warning: No RIVM data found for '{category}', using defaults")
            factors[category] = {
                'co2': np.nan,
                'land': np.nan,
                'water': np.nan,
                'scope12': np.nan
            }
            continue
        
        # Aggregate values based on method
        if method == 'median':
            co2 = matched['CO2_kg'].median()
            land = matched['Land_m2a'].median()
            water = matched['Water_m3'].median() * 1000  # Convert m³ to liters
        elif method == 'mean':
            co2 = matched['CO2_kg'].mean()
            land = matched['Land_m2a'].mean()
            water = matched['Water_m3'].mean() * 1000
        elif method == 'conservative':
            co2 = matched['CO2_kg'].quantile(0.75)  # 75th percentile
            land = matched['Land_m2a'].quantile(0.75)
            water = matched['Water_m3'].quantile(0.75) * 1000
        else:
            raise ValueError(f"Unknown aggregation method: {method}")
        
        # Estimate Scope 1+2 as percentage of total CO2
        # RIVM "Global warming" includes full lifecycle
        # Typical Scope 1+2 ranges: 
        # - Animal products: 50-70% (production-intensive)
        # - Plant products: 20-40% (processing/transport dominant)
        # - Processed foods: 30-50%
        
        # Category-specific scope12 percentages (conservative estimates)
        scope12_pct_map = {
            'Beef': 0.60, 'Pork': 0.55, 'Lamb': 0.60, 'Chicken': 0.45,
            'Fish': 0.40, 'Cheese': 0.50, 'Milk': 0.40, 'Dairy': 0.40,
            'Eggs': 0.45, 'Butter': 0.55, 'Animal_Fats': 0.60,
            'Pulses': 0.30, 'Nuts': 0.25, 'Meat_Subs': 0.35,
            'Grains': 0.30, 'Bread': 0.35, 'Pasta': 0.35, 'Rice': 0.30,
            'Vegetables': 0.25, 'Fruits': 0.25, 'Potatoes': 0.30,
            'Sugar': 0.35, 'Processed': 0.40, 'Snacks': 0.45,
            'Ready_Meals': 0.50, 'Instant_Noodles': 0.45, 'Instant_Pasta': 0.40,
            'Coffee': 0.60, 'Tea': 0.50, 'Alcohol': 0.45,
            'Oils': 0.30, 'Frying_Oil_Animal': 0.60,
            'Condiment_Sauces': 0.40, 'Spice_Mixes': 0.35, 'Condiments': 0.35
        }
        
        scope12_pct = scope12_pct_map.get(category, 0.40)  # Default 40%
        scope12 = co2 * scope12_pct
        
        factors[category] = {
            'co2': round(co2, 2),
            'land': round(land, 2),
            'water': round(water, 0),
            'scope12': round(scope12, 2)
        }
        
        print(f"✓ {category}: {len(matched)} RIVM products matched | CO2={co2:.2f} kg")
    
    return factors


def load_rivm_factors(csv_path=None, method='median', fill_missing=True):
    """
    Main function to load RIVM database and generate model-compatible factors.
    
    Args:
        csv_path: Path to RIVM CSV file (None = auto-detect)
        method: Aggregation method ('median', 'mean', 'conservative')
        fill_missing: If True, fills missing values with current model defaults
        
    Returns:
        dict: Emission factors dictionary matching model structure
        
    Example:
        >>> factors = load_rivm_factors()
        >>> beef_co2 = factors['Beef']['co2']
        >>> print(f"Beef: {beef_co2} kg CO2e/kg")
    """
    print("=" * 70)
    print("LOADING RIVM LCA DATABASE")
    print("=" * 70)
    
    # Load database
    print(f"\n1. Loading RIVM CSV...")
    df = load_rivm_database(csv_path)
    print(f"   ✓ Loaded {len(df)} food products")
    
    # Get mapping
    print(f"\n2. Applying category mapping...")
    mapping = map_rivm_to_categories()
    print(f"   ✓ Mapping {len(mapping)} model categories")
    
    # Aggregate
    print(f"\n3. Aggregating values (method={method})...")
    factors = aggregate_rivm_by_category(df, mapping, method=method)
    
    # Fill missing values with defaults if requested
    if fill_missing:
        print(f"\n4. Filling missing values with model defaults...")
        defaults = get_default_factors()
        for category, values in factors.items():
            for key in ['co2', 'land', 'water', 'scope12']:
                if pd.isna(values[key]) and category in defaults:
                    values[key] = defaults[category][key]
                    print(f"   ⚠ {category}.{key}: Using default {defaults[category][key]}")
    
    # Summary
    print(f"\n" + "=" * 70)
    print(f"RIVM FACTORS LOADED: {len(factors)} categories")
    print("=" * 70)
    
    return factors


def get_default_factors():
    """
    Returns current model default factors as fallback values.
    These are the original manually-curated values.
    """
    return {
        'Beef':       {'co2': 28.0,  'land': 25.0,  'water': 15400, 'scope12': 16.67},
        'Pork':       {'co2': 5.0,   'land': 9.0,   'water': 6000,  'scope12': 13.34},
        'Chicken':    {'co2': 3.5,   'land': 7.0,   'water': 4300,  'scope12': 10.00},
        'Cheese':     {'co2': 10.0,  'land': 12.0,  'water': 5000,  'scope12': 6.67},
        'Milk':       {'co2': 1.3,   'land': 1.5,   'water': 1000,  'scope12': 3.33},
        'Dairy':      {'co2': 1.3,   'land': 1.5,   'water': 1000,  'scope12': 3.33},
        'Fish':       {'co2': 3.5,   'land': 0.5,   'water': 2000,  'scope12': 12.00},
        'Eggs':       {'co2': 2.2,   'land': 2.5,   'water': 3300,  'scope12': 5.34},
        'Pulses':     {'co2': 0.9,   'land': 3.0,   'water': 4000,  'scope12': 2.67},
        'Nuts':       {'co2': 0.3,   'land': 2.5,   'water': 9000,  'scope12': 1.33},
        'Meat_Subs':  {'co2': 2.5,   'land': 3.0,   'water': 200,   'scope12': 3.33},
        'Grains':     {'co2': 1.1,   'land': 1.8,   'water': 1600,  'scope12': 1.67},
        'Bread':      {'co2': 1.2,   'land': 1.6,   'water': 1500,  'scope12': 1.67},
        'Pasta':      {'co2': 1.1,   'land': 1.8,   'water': 1600,  'scope12': 1.67},
        'Rice':       {'co2': 2.5,   'land': 3.0,   'water': 2300,  'scope12': 2.50},
        'Vegetables': {'co2': 0.6,   'land': 0.5,   'water': 320,   'scope12': 1.33},
        'Fruits':     {'co2': 0.7,   'land': 0.6,   'water': 960,   'scope12': 1.33},
        'Potatoes':   {'co2': 0.4,   'land': 0.3,   'water': 290,   'scope12': 1.33},
        'Sugar':      {'co2': 2.0,   'land': 1.5,   'water': 200,   'scope12': 1.33},
        'Processed':  {'co2': 2.5,   'land': 1.5,   'water': 300,   'scope12': 3.33},
        'Snacks':     {'co2': 4.0,   'land': 2.0,   'water': 400,   'scope12': 5.00},
        'Ready_Meals': {'co2': 4.5,  'land': 2.2,   'water': 450,   'scope12': 6.00},
        'Instant_Noodles': {'co2': 3.5, 'land': 2.0, 'water': 400, 'scope12': 4.50},
        'Instant_Pasta': {'co2': 2.5,   'land': 1.8,  'water': 350,   'scope12': 3.00},
        'Coffee':     {'co2': 2.8,   'land': 0.8,   'water': 140,   'scope12': 23.34},
        'Tea':        {'co2': 0.4,   'land': 0.2,   'water': 300,   'scope12': 8.00},
        'Alcohol':    {'co2': 1.2,   'land': 0.5,   'water': 500,   'scope12': 13.34},
        'Butter':     {'co2': 12.0,  'land': 8.0,   'water': 5000,  'scope12': 18.00},
        'Animal_Fats': {'co2': 14.0, 'land': 9.0,   'water': 6000,  'scope12': 22.00},
        'Frying_Oil_Animal': {'co2': 14.0, 'land': 9.0, 'water': 6000, 'scope12': 22.00},
        'Oils':       {'co2': 1.0,   'land': 1.0,   'water': 200,   'scope12': 3.00},
        'Condiment_Sauces': {'co2': 3.0, 'land': 1.5, 'water': 400, 'scope12': 4.50},
        'Spice_Mixes': {'co2': 2.0,   'land': 1.0,   'water': 250,   'scope12': 3.00}
    }


def export_rivm_factors_csv(factors, output_path='rivm_factors_export.csv'):
    """
    Export factors dictionary to CSV for review and documentation.
    
    Args:
        factors: Factors dictionary
        output_path: Output CSV file path
    """
    rows = []
    for category, values in factors.items():
        rows.append({
            'Category': category,
            'CO2_kgCO2e_per_kg': values['co2'],
            'Land_m2a_per_kg': values['land'],
            'Water_L_per_kg': values['water'],
            'Scope12_kgCO2e_per_kg': values['scope12'],
            'Scope3_kgCO2e_per_kg': values['co2'] - values['scope12']
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"\n✓ Exported factors to: {output_path}")
    return df


# Example usage
if __name__ == "__main__":
    # Load RIVM factors
    factors = load_rivm_factors(method='median', fill_missing=True)
    
    # Export to CSV for review
    df = export_rivm_factors_csv(factors, 'rivm_factors_median.csv')
    
    # Print comparison with defaults
    print("\n" + "=" * 70)
    print("COMPARISON: RIVM vs CURRENT DEFAULTS")
    print("=" * 70)
    print(f"{'Category':<20} {'Current CO2':<12} {'RIVM CO2':<12} {'Δ%':<10}")
    print("-" * 70)
    
    defaults = get_default_factors()
    for cat in sorted(factors.keys()):
        if cat in defaults:
            current = defaults[cat]['co2']
            rivm = factors[cat]['co2']
            delta_pct = ((rivm - current) / current * 100) if current > 0 else 0
            print(f"{cat:<20} {current:<12.2f} {rivm:<12.2f} {delta_pct:+.1f}%")
