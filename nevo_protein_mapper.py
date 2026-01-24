"""
Extract protein content from NEVO database and map to model categories.
Maps NEVO food products to the 14 visualization categories used in the model.
"""

import pandas as pd
import numpy as np

# Visualization categories mapping (from Master Hybrid Model v3)
VISUAL_MAPPING = {
    'Beef': 'Red Meat', 'Pork': 'Red Meat', 'Lamb': 'Red Meat',
    'Chicken': 'Poultry', 'Poultry': 'Poultry',
    'Milk': 'Dairy (Liquid)', 'Dairy': 'Dairy (Liquid)',
    'Cheese': 'Dairy (Solid) & Eggs', 'Eggs': 'Dairy (Solid) & Eggs',
    'Fish': 'Fish',
    'Pulses': 'Plant Protein', 'Nuts': 'Plant Protein', 'Meat_Subs': 'Plant Protein', 'Plant Protein': 'Plant Protein',
    'Grains': 'Staples', 'Potatoes': 'Staples', 'Staples': 'Staples', 'Pasta': 'Staples', 'Bread': 'Staples',
    'Rice': 'Rice',
    'Vegetables': 'Veg & Fruit', 'Fruits': 'Veg & Fruit', 'Veg & Fruit': 'Veg & Fruit',
    'Sugar': 'Ultra-Processed', 'Processed': 'Ultra-Processed', 'Ultra-Processed': 'Ultra-Processed', 
    'Drinks': 'Ultra-Processed', 'Snacks': 'Ultra-Processed', 'Ready_Meals': 'Ultra-Processed', 
    'Instant_Noodles': 'Ultra-Processed', 'Instant_Pasta': 'Ultra-Processed',
    'Coffee': 'Beverages & Additions', 'Tea': 'Beverages & Additions', 'Alcohol': 'Beverages & Additions',
    'Butter': 'Fats (Solid, Animal)', 'Animal_Fats': 'Fats (Solid, Animal)', 'Frying_Oil_Animal': 'Fats (Solid, Animal)',
    'Oils': 'Oils (Plant-based)',
    'Condiment_Sauces': 'Condiments', 'Spice_Mixes': 'Condiments'
}

def load_nevo_database():
    """Load NEVO 2025 database and extract protein content."""
    print("\n" + "="*80)
    print("LOADING NEVO 2025 DATABASE")
    print("="*80 + "\n")
    
    # Load NEVO database - pipe delimited with quoted strings
    df = pd.read_csv('NEVO2025_v9.0.csv', encoding='utf-8', delimiter='|', quotechar='"')
    
    print(f"✓ Loaded {len(df)} NEVO products")
    print(f"✓ Columns (first 20): {list(df.columns[:20])}")
    print()
    
    # Protein column is "PROT (g)" - 15th column (index 14)
    protein_col = 'PROT (g)'
    
    print(f"✓ Using protein column: '{protein_col}'")
    
    # English food name column
    name_col = 'Engelse naam/Food name'
    
    print(f"✓ Using product name column: '{name_col}'")
    print()
    
    return df, name_col, protein_col

def map_nevo_to_categories(df, name_col, protein_col):
    """
    Map NEVO products to model categories and calculate median protein content.
    """
    
    # Define search terms for each model food item
    NEVO_SEARCH_TERMS = {
        'Beef': ['beef', 'rund', 'steak', 'veal', 'kalf'],
        'Pork': ['pork', 'varken', 'ham', 'bacon', 'spek'],
        'Lamb': ['lamb', 'lam', 'mutton', 'schaap'],
        'Chicken': ['chicken', 'kip', 'poultry', 'gevogelte'],
        'Fish': ['fish', 'vis', 'salmon', 'zalm', 'cod', 'kabeljauw', 'tuna', 'tonijn'],
        'Eggs': ['egg', 'ei'],
        'Cheese': ['cheese', 'kaas', 'gouda', 'edam'],
        'Milk': ['milk', 'melk'],
        'Dairy': ['yogurt', 'yoghurt', 'quark', 'custard', 'vla'],
        'Pulses': ['beans', 'bonen', 'lentils', 'linzen', 'chickpea', 'kikkererwt'],
        'Nuts': ['nuts', 'noten', 'almond', 'amandel', 'walnut', 'walnoot', 'peanut', 'pinda'],
        'Meat_Subs': ['tofu', 'tempeh', 'vegetarian', 'vegetarisch', 'meat substitute'],
        'Bread': ['bread', 'brood'],
        'Pasta': ['pasta', 'macaroni', 'spaghetti'],
        'Rice': ['rice', 'rijst'],
        'Grains': ['wheat', 'tarwe', 'oats', 'haver', 'barley', 'gerst'],
        'Potatoes': ['potato', 'aardappel'],
        'Vegetables': ['vegetable', 'groente', 'carrot', 'wortel', 'broccoli', 'tomato', 'tomaat'],
        'Fruits': ['fruit', 'apple', 'appel', 'banana', 'banaan', 'orange', 'sinaasappel'],
        'Sugar': ['sugar', 'suiker', 'candy', 'snoep'],
        'Snacks': ['chips', 'crisp', 'cookie', 'koek'],
        'Coffee': ['coffee', 'koffie'],
        'Tea': ['tea', 'thee'],
        'Alcohol': ['beer', 'bier', 'wine', 'wijn', 'spirit'],
        'Butter': ['butter', 'boter'],
        'Oils': ['oil', 'olie', 'sunflower', 'zonnebloem', 'olive', 'olijf'],
        'Condiment_Sauces': ['sauce', 'saus', 'ketchup', 'mayo'],
        'Spice_Mixes': ['spice', 'kruiden', 'pepper', 'peper', 'salt', 'zout']
    }
    
    # Extract protein values (convert European decimal format if needed)
    df['protein_g'] = pd.to_numeric(
        df[protein_col].astype(str).str.replace(',', '.'), 
        errors='coerce'
    )
    
    # Map each NEVO product to model categories
    category_proteins = {cat: [] for cat in set(VISUAL_MAPPING.values())}
    
    print("\n" + "="*80)
    print("MAPPING NEVO PRODUCTS TO MODEL CATEGORIES")
    print("="*80 + "\n")
    
    for food_item, search_terms in NEVO_SEARCH_TERMS.items():
        # Find matching products
        matches = pd.DataFrame()
        for term in search_terms:
            mask = df[name_col].str.contains(term, case=False, na=False, regex=False)
            matches = pd.concat([matches, df[mask]])
        
        # Remove duplicates
        matches = matches.drop_duplicates(subset=[name_col])
        
        if len(matches) > 0:
            # Get protein values (g per 100g)
            protein_values = matches['protein_g'].dropna()
            
            if len(protein_values) > 0:
                median_protein = protein_values.median()
                mean_protein = protein_values.mean()
                
                # Convert to fraction (g protein / g food)
                median_fraction = median_protein / 100.0
                
                # Map to visualization category
                vis_category = VISUAL_MAPPING.get(food_item, 'Unknown')
                category_proteins[vis_category].append(median_fraction)
                
                print(f"✅ {food_item:20} → {vis_category:25} | "
                      f"{len(protein_values):3} products | "
                      f"Median: {median_protein:5.2f}g/100g ({median_fraction:.3f})")
        else:
            print(f"❌ {food_item:20} → No matches found")
    
    # Calculate median for each visualization category
    print("\n" + "="*80)
    print("VISUALIZATION CATEGORY PROTEIN CONTENT (Median)")
    print("="*80 + "\n")
    
    category_medians = {}
    for category, proteins in sorted(category_proteins.items()):
        if proteins:
            median_val = np.median(proteins)
            category_medians[category] = median_val
            print(f"{category:30} | {median_val:.3f} ({median_val*100:5.2f}g per 100g)")
        else:
            category_medians[category] = 0.0
            print(f"{category:30} | NO DATA - defaulting to 0.000")
    
    return category_medians

def generate_python_dict(category_medians):
    """Generate Python dictionary code for integration."""
    
    print("\n\n" + "="*80)
    print("PYTHON CODE FOR INTEGRATION")
    print("="*80 + "\n")
    
    print("# Protein content from NEVO 2025 database (fraction: g protein / g food)")
    print("# Source: NEVO 2025 v9.0 - Nederlandse Voedingsmiddelentabel")
    print("# Mapped to 14 visualization categories using median values")
    print("PROTEIN_CONTENT = {")
    
    for category in sorted(category_medians.keys()):
        value = category_medians[category]
        print(f"    '{category}': {value:.3f},")
    
    print("}")
    
    # Export to CSV
    df_export = pd.DataFrame([
        {'Category': cat, 'Protein_Fraction': val, 'Protein_g_per_100g': val*100}
        for cat, val in sorted(category_medians.items())
    ])
    
    csv_path = 'nevo_protein_content_by_category.csv'
    df_export.to_csv(csv_path, index=False)
    print(f"\n✅ Exported to: {csv_path}")

def main():
    print("\n" + "="*80)
    print("NEVO PROTEIN CONTENT MAPPER")
    print("Extract protein data from NEVO 2025 and map to model categories")
    print("="*80)
    
    # Load NEVO database
    result = load_nevo_database()
    if result is None:
        return
    
    df, name_col, protein_col = result
    
    # Map to categories
    category_medians = map_nevo_to_categories(df, name_col, protein_col)
    
    # Generate code
    generate_python_dict(category_medians)
    
    print("\n" + "="*80)
    print("✅ COMPLETE")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
