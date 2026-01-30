"""
Better focused search for the 5 missing categories with smarter filtering.
"""

import pandas as pd
from pathlib import Path

def load_rivm():
    """Load RIVM database."""
    csv_path = Path('../datasets/Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv')
    df = pd.read_csv(csv_path, skiprows=2, sep=';', encoding='utf-8')
    
    # Use first columns
    df.columns = ['Product', 'Unit', 'Unknown', 'CO2_kg', 'Acid_kg', 'FreshEutro_kg', 
                  'MarineEutro_kg', 'Land_m2a', 'Water_m3', 'NEVO_Code', 'NEVO_NL', 
                  'NEVO_Group_NL', 'NEVO_EN', 'NEVO_Group_EN', 'Extra']
    
    # Convert CO2 (European format)
    df['CO2_kg'] = pd.to_numeric(df['CO2_kg'].astype(str).str.replace(',', '.'), errors='coerce')
    df['Land_m2a'] = pd.to_numeric(df['Land_m2a'].astype(str).str.replace(',', '.'), errors='coerce')
    df['Water_m3'] = pd.to_numeric(df['Water_m3'].astype(str).str.replace(',', '.'), errors='coerce')
    
    return df

def search_category(df, category_name, search_terms, exclude_terms=None):
    """Search for products matching criteria."""
    exclude_terms = exclude_terms or []
    
    print(f"\n{'='*70}")
    print(f"🔍 Searching: {category_name}")
    print(f"{'='*70}\n")
    
    # Find matches
    matches = []
    for term in search_terms:
        mask = df['Product'].str.contains(term, case=False, na=False, regex=False)
        found = df[mask]
        
        # Apply exclusions
        for excl in exclude_terms:
            found = found[~found['Product'].str.contains(excl, case=False, na=False, regex=False)]
        
        for _, row in found.iterrows():
            matches.append({
                'product': row['Product'],
                'co2': row['CO2_kg'],
                'land': row['Land_m2a'],
                'water': row['Water_m3'],
                'matched_by': term
            })
    
    # Deduplicate
    unique = {}
    for m in matches:
        if m['product'] not in unique:
            unique[m['product']] = m
    
    # Sort by CO2
    sorted_matches = sorted(unique.values(), key=lambda x: x['co2'] if pd.notna(x['co2']) else 0, reverse=False)
    
    if sorted_matches:
        print(f"✅ Found {len(sorted_matches)} matches\n")
        
        # Show top 5 lowest CO2 (most conservative)
        print("📊 TOP 5 (Lowest CO2 - most conservative):\n")
        for i, m in enumerate(sorted_matches[:5], 1):
            print(f"{i}. {m['product']}")
            print(f"   CO2: {m['co2']:.2f} kg | Land: {m['land']:.2f} m² | Water: {m['water']:.2f} m³")
            print(f"   Matched by: '{m['matched_by']}'")
            print()
        
        # Calculate median
        co2_values = [m['co2'] for m in sorted_matches if pd.notna(m['co2'])]
        if co2_values:
            median_co2 = sorted(co2_values)[len(co2_values)//2]
            mean_co2 = sum(co2_values) / len(co2_values)
            print(f"📈 Statistics: Median = {median_co2:.2f} kg CO2 | Mean = {mean_co2:.2f} kg CO2")
            print(f"   Range: {min(co2_values):.2f} - {max(co2_values):.2f} kg CO2")
        
        return sorted_matches
    else:
        print("❌ No matches found\n")
        return None

def main():
    print("\n" + "="*70)
    print("RIVM DATABASE - TARGETED SEARCH FOR MISSING CATEGORIES")
    print("="*70)
    
    df = load_rivm()
    print(f"\n✓ Loaded {len(df)} RIVM products\n")
    
    results = {}
    
    # 1. Meat_Subs - Plant-based meat alternatives
    results['Meat_Subs'] = search_category(
        df, 
        'Meat_Subs (Plant-based meat alternatives)',
        search_terms=['Vegetarian burger', 'vegetarian hamburger', 'Tofu', 'Tempeh', 
                      'Mincemeat vegetarian', 'Vegetable burger'],
        exclude_terms=['cake', 'pie', 'peanut']  # Exclude non-meat items
    )
    
    # 2. Instant_Noodles - Just noodles/pasta products
    results['Instant_Noodles'] = search_category(
        df,
        'Instant_Noodles (Dried/instant noodles)',
        search_terms=['Pasta unprepared', 'Macaroni unprepared', 'Spaghetti unprepared',
                      'Noodles dried', 'Pasta dried'],
        exclude_terms=['soup', 'salad', 'prepared', 'w sauce']
    )
    
    # 3. Instant_Pasta - Same as noodles
    results['Instant_Pasta'] = search_category(
        df,
        'Instant_Pasta (Dried pasta products)',
        search_terms=['Pasta unprepared', 'Macaroni unprepared', 'Spaghetti unprepared',
                      'Tagliatelle unprepared', 'Penne unprepared', 'Pasta product dried'],
        exclude_terms=['soup', 'salad', 'prepared', 'w sauce', 'cheese']
    )
    
    # 4. Animal_Fats - Butter and cooking fats
    results['Animal_Fats'] = search_category(
        df,
        'Animal_Fats (Butter and animal fats)',
        search_terms=['Butter, salted', 'Butter, unsalted', 'Butter product', 'Ghee'],
        exclude_terms=['cake', 'pie', 'peanut', 'chocolate']
    )
    
    # 5. Frying_Oil_Animal - Actual oils
    results['Frying_Oil_Animal'] = search_category(
        df,
        'Frying_Oil_Animal (Cooking/frying oils)',
        search_terms=['Sunflower oil', 'Rapeseed oil', 'Olive oil', 'Peanut oil',
                      'Vegetable oil', 'Cooking oil', 'Frying oil', 'Oil liquid'],
        exclude_terms=['tuna', 'fish', 'sardine', 'meat', 'sauce', 'salad dressing']
    )
    
    # Summary
    print(f"\n\n{'='*70}")
    print("📋 RECOMMENDED VALUES (Using Median for Robustness)")
    print("="*70 + "\n")
    
    for category, matches in results.items():
        if matches:
            # Use median CO2
            co2_values = [m['co2'] for m in matches if pd.notna(m['co2'])]
            median_co2 = sorted(co2_values)[len(co2_values)//2] if co2_values else 3.0
            
            # Estimate Scope 1+2 based on category type
            if 'Meat_Subs' in category:
                scope12_pct = 45  # Processed plant foods
            elif 'Noodles' in category or 'Pasta' in category:
                scope12_pct = 35  # Grain processing
            elif 'Fats' in category:
                scope12_pct = 55  # Dairy/animal production
            elif 'Oil' in category:
                scope12_pct = 30  # Plant oil extraction
            else:
                scope12_pct = 40
            
            scope12 = median_co2 * (scope12_pct / 100)
            
            # Get representative product
            representative = sorted(matches, key=lambda x: abs(x['co2'] - median_co2))[0]
            
            print(f"✅ {category}:")
            print(f"   CO2: {median_co2:.2f} kg CO2e/kg")
            print(f"   Scope 1+2: {scope12:.2f} kg ({scope12_pct}%)")
            print(f"   Land: {representative['land']:.2f} m²/kg")
            print(f"   Water: {representative['water']*1000:.0f} L/kg")
            print(f"   Representative product: {representative['product'][:70]}")
            print(f"   Based on {len(co2_values)} RIVM products (median)")
            print()
        else:
            print(f"❌ {category}: No match - Use literature value")
            print()

if __name__ == '__main__':
    main()
