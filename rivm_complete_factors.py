"""
Enhanced RIVM LCA Factor Extractor with water data recovery and missing categories.
Combines RIVM database values with reasonable proxy estimates.
"""

import pandas as pd
import numpy as np

def main():
    print("\n" + "="*80)
    print("RIVM LCA FACTORS - ENHANCED INTEGRATION")
    print("="*80 + "\n")
    
    # RIVM-extracted factors (from previous script run)
    rivm_factors = {
        'Beef': {'co2': 25.55, 'land': 14.25, 'scope12': 13.99},
        'Pork': {'co2': 11.77, 'land': 12.73, 'scope12': 6.91},
        'Chicken': {'co2': 4.35, 'land': 5.96, 'scope12': 1.96},
        'Fish': {'co2': 5.15, 'land': 1.39, 'scope12': 2.06},
        'Eggs': {'co2': 0.40, 'land': 0.09, 'scope12': 0.51},
        'Cheese': {'co2': 7.64, 'land': 3.91, 'scope12': 4.42},
        'Milk': {'co2': 1.35, 'land': 1.24, 'scope12': 0.77},
        'Dairy': {'co2': 1.66, 'land': 0.61, 'scope12': 1.78},
        'Pulses': {'co2': 1.60, 'land': 1.36, 'scope12': 0.50},
        'Nuts': {'co2': 2.81, 'land': 7.06, 'scope12': 0.61},
        'Grains': {'co2': 1.07, 'land': 1.78, 'scope12': 0.43},
        'Bread': {'co2': 1.49, 'land': 1.89, 'scope12': 0.60},
        'Pasta': {'co2': 1.91, 'land': 0.79, 'scope12': 0.65},
        'Rice': {'co2': 2.16, 'land': 1.39, 'scope12': 0.65},
        'Potatoes': {'co2': 1.19, 'land': 0.73, 'scope12': 0.38},
        'Vegetables': {'co2': 1.22, 'land': 0.33, 'scope12': 0.26},
        'Fruits': {'co2': 1.05, 'land': 0.58, 'scope12': 0.19},
        'Sugar': {'co2': 0.99, 'land': 1.57, 'scope12': 0.24},
        'Processed': {'co2': 4.29, 'land': 5.11, 'scope12': 0.90},
        'Snacks': {'co2': 2.43, 'land': 3.53, 'scope12': 1.20},
        'Coffee': {'co2': 1.50, 'land': 0.59, 'scope12': 0.77},
        'Tea': {'co2': 0.79, 'land': 0.44, 'scope12': 1.16},
        'Alcohol': {'co2': 0.56, 'land': 0.25, 'scope12': 0.22},
        'Butter': {'co2': 3.78, 'land': 4.32, 'scope12': 1.78},
        'Oils': {'co2': 1.80, 'land': 2.10, 'scope12': 0.56},
    }
    
    # Water consumption estimates (based on literature when RIVM data unavailable)
    # Unit: liters per kg
    water_estimates = {
        'Beef': 15400,      # Very high water footprint
        'Pork': 6000,       # Moderate-high
        'Chicken': 4300,    # Moderate
        'Fish': 2000,       # Moderate-low
        'Eggs': 3300,
        'Cheese': 5000,
        'Milk': 1000,       # Dairy milk
        'Dairy': 1000,      # Other dairy products
        'Pulses': 4000,
        'Nuts': 9000,       # High water (especially almonds)
        'Grains': 1600,
        'Bread': 1500,
        'Pasta': 1600,
        'Rice': 2300,
        'Potatoes': 290,    # Low water
        'Vegetables': 320,  # Low water
        'Fruits': 960,      # Moderate
        'Sugar': 200,       # Low
        'Processed': 300,   # Variable, conservative estimate
        'Snacks': 400,
        'Coffee': 140,      # High per unit but small quantities
        'Tea': 300,
        'Alcohol': 500,
        'Butter': 5000,     # Dairy-based
        'Oils': 200,        # Low water for oils
    }
    
    # Missing categories from your original factors
    missing_categories = {
        'Meat_Subs': {'co2': 2.5, 'land': 3.0, 'water': 200, 'scope12': 3.33},
        'Ready_Meals': {'co2': 4.5, 'land': 2.2, 'water': 450, 'scope12': 6.00},
        'Instant_Noodles': {'co2': 3.5, 'land': 2.0, 'water': 400, 'scope12': 4.50},
        'Instant_Pasta': {'co2': 2.5, 'land': 1.8, 'water': 350, 'scope12': 3.00},
        'Animal_Fats': {'co2': 14.0, 'land': 9.0, 'water': 6000, 'scope12': 22.00},
        'Frying_Oil_Animal': {'co2': 14.0, 'land': 9.0, 'water': 6000, 'scope12': 22.00},
        'Condiment_Sauces': {'co2': 3.0, 'land': 1.5, 'water': 400, 'scope12': 4.50},
        'Spice_Mixes': {'co2': 2.0, 'land': 1.0, 'water': 250, 'scope12': 3.00}
    }
    
    # Merge all factors
    complete_factors = {}
    
    # Add RIVM factors with water
    for category, data in rivm_factors.items():
        complete_factors[category] = {
            'co2': data['co2'],
            'land': data['land'],
            'water': water_estimates[category],
            'scope12': data['scope12']
        }
    
    # Add missing categories
    complete_factors.update(missing_categories)
    
    # Print summary
    print("COMPLETE LCA FACTORS (RIVM + Estimates + Missing Categories)")
    print("="*80 + "\n")
    
    print(f"{'Category':<25} {'CO2':>8} {'Land':>8} {'Water':>10} {'Scope12':>8}")
    print("-" * 70)
    
    for category in sorted(complete_factors.keys()):
        f = complete_factors[category]
        print(f"{category:<25} {f['co2']:>8.2f} {f['land']:>8.2f} {f['water']:>10.0f} {f['scope12']:>8.2f}")
    
    # Export as Python code
    print("\n\n" + "="*80)
    print("PYTHON CODE FOR YOUR MODEL")
    print("="*80 + "\n")
    
    print("factors = {")
    for category in sorted(complete_factors.keys()):
        f = complete_factors[category]
        print(f"    '{category}': {{'co2': {f['co2']}, 'land': {f['land']}, 'water': {f['water']}, 'scope12': {f['scope12']}}},")
    print("}")
    
    # Export to CSV
    df = pd.DataFrame(complete_factors).T
    csv_path = 'rivm_complete_lca_factors.csv'
    df.to_csv(csv_path)
    print(f"\n✅ Exported to: {csv_path}")
    
    # Also create a detailed comparison
    print("\n\n" + "="*80)
    print("COMPARISON WITH YOUR ORIGINAL FACTORS")
    print("="*80 + "\n")
    
    original_factors = {
        'Beef': {'co2': 28.0, 'land': 25.0, 'water': 15400, 'scope12': 16.67},
        'Pork': {'co2': 5.0, 'land': 9.0, 'water': 6000, 'scope12': 13.34},
        'Chicken': {'co2': 3.5, 'land': 7.0, 'water': 4300, 'scope12': 10.00},
        'Fish': {'co2': 3.5, 'land': 0.5, 'water': 2000, 'scope12': 12.00},
        'Cheese': {'co2': 10.0, 'land': 12.0, 'water': 5000, 'scope12': 6.67},
        'Milk': {'co2': 1.3, 'land': 1.5, 'water': 1000, 'scope12': 3.33},
    }
    
    print(f"{'Category':<12} {'CO2 (Old)':>10} {'CO2 (New)':>10} {'Change %':>10}")
    print("-" * 45)
    
    for cat in ['Beef', 'Pork', 'Chicken', 'Fish', 'Cheese', 'Milk']:
        if cat in original_factors and cat in complete_factors:
            old = original_factors[cat]['co2']
            new = complete_factors[cat]['co2']
            change = ((new - old) / old) * 100
            print(f"{cat:<12} {old:>10.2f} {new:>10.2f} {change:>9.1f}%")
    
    print("\n💡 KEY NOTES:")
    print("   • RIVM values are derived from actual database entries")
    print("   • Water estimates use literature values for accuracy")
    print("   • Scope12 values are from Monitor calibration (previous integration)")
    print("   • Missing categories use your original estimates")
    print("   • CO2 values are now scientifically grounded in real LCA data")
    
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
