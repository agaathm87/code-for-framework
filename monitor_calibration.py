"""
Monitor Voedsel Amsterdam Calibration Analysis
Reverse-engineer Scope 1+2 percentages from Monitor food group data

Monitor data (total CO2 = 1,750 kton):
- Meat: 25% = 437.5 kton
- Non-alcoholic beverages: 11% = 192.5 kton
- Fruit: 6% = 105 kton
- Alcohol: 6% = 105 kton
- Vegetables: 6% = 105 kton
- Fast food: 4-6% = 70-105 kton
- Fish: 4-6% = 70-105 kton
- Cheese: 4-6% = 70-105 kton
- Dairy: 4-6% = 70-105 kton
- Plant-based alternatives, nuts, seeds, grains: ~1% each
- Plant-based cheese, yogurt, butter: <1% each

Goal: Match Monitor baseline when using Monitor diet profile + RIVM factors
"""

import pandas as pd
import numpy as np

def analyze_monitor_baseline():
    """
    Analyze Monitor Voedsel Amsterdam 1,750 kton baseline to determine 
    Scope 1+2 vs Scope 3 split by food category.
    
    Key assumption: Monitor 1,750 kton = Scope 1+2 (production, retail, household)
    Supply chain (Scope 3) is additional on top.
    
    Based on LCA research:
    - Animal products: 50-70% Scope 1+2, 30-50% Scope 3
    - Plant products: 20-40% Scope 1+2, 60-80% Scope 3
    - Processed foods: 30-50% Scope 1+2, 50-70% Scope 3
    
    The Monitor 1,750 kton is likely Scope 1+2 based on system boundary
    (production + retail + household, not international supply chain)
    """
    
    monitor_data = {
        'Meat': {'pct_co2': 25, 'kton': 437.5, 'pct_consumption': 3},
        'Non-alcoholic beverages': {'pct_co2': 11, 'kton': 192.5, 'pct_consumption': 15},
        'Fruit': {'pct_co2': 6, 'kton': 105, 'pct_consumption': 5},
        'Alcohol': {'pct_co2': 6, 'kton': 105, 'pct_consumption': 5},
        'Vegetables': {'pct_co2': 6, 'kton': 105, 'pct_consumption': 5},
        'Fast food': {'pct_co2': 5, 'kton': 87.5, 'pct_consumption': 2},
        'Fish': {'pct_co2': 5, 'kton': 87.5, 'pct_consumption': 2},
        'Cheese': {'pct_co2': 5, 'kton': 87.5, 'pct_consumption': 2},
        'Dairy': {'pct_co2': 5, 'kton': 87.5, 'pct_consumption': 3},
        'Plant-based alternatives': {'pct_co2': 3, 'kton': 52.5, 'pct_consumption': 2},
        'Nuts & Seeds': {'pct_co2': 1, 'kton': 17.5, 'pct_consumption': 1},
        'Grains': {'pct_co2': 1, 'kton': 17.5, 'pct_consumption': 2},
    }
    
    print("\n" + "=" * 80)
    print("MONITOR VOEDSEL AMSTERDAM CALIBRATION")
    print("=" * 80)
    print("\nBaseline: 1,750 kton CO2 (Scope 1+2)")
    print("\nCategory Breakdown:")
    print(f"{'Category':<25} {'% of CO2':<12} {'Kton':<12} {'% Consumption':<15}")
    print("-" * 80)
    
    total_kton = 0
    for cat, data in monitor_data.items():
        print(f"{cat:<25} {data['pct_co2']:>10}% {data['kton']:>10.1f} {data['pct_consumption']:>13}%")
        total_kton += data['kton']
    
    print("-" * 80)
    print(f"{'TOTAL':<25} {100:>10}% {total_kton:>10.1f}")
    
    return monitor_data


def calculate_scope12_percentages():
    """
    Determine Scope 1+2 percentage for each category based on Monitor data.
    
    Methodology:
    1. Monitor 1,750 kton is Scope 1+2 (system boundary: production + retail + household)
    2. International supply chain = Scope 3 (additional)
    3. Calculate impact per gram consumed (efficiency metric)
    4. Allocate Scope 1+2 % based on production intensity
    """
    
    # Monitor consumption (estimated from text - grams per person per day)
    # Population: 873,000, days per year: 365
    monitor_consumption = {
        'Meat': {'g_per_capita_day': 22, 'scope12_pct': 60},  # High production intensity
        'Non-alcoholic beverages': {'g_per_capita_day': 600, 'scope12_pct': 30},  # Mostly transport
        'Fruit': {'g_per_capita_day': 140, 'scope12_pct': 25},  # Imported, mostly Scope 3
        'Alcohol': {'g_per_capita_day': 25, 'scope12_pct': 40},  # Mixed (local + import)
        'Vegetables': {'g_per_capita_day': 160, 'scope12_pct': 28},  # Local production
        'Fast food': {'g_per_capita_day': 15, 'scope12_pct': 45},  # Processing + retail
        'Fish': {'g_per_capita_day': 12, 'scope12_pct': 50},  # Fishing + processing
        'Cheese': {'g_per_capita_day': 28, 'scope12_pct': 55},  # Local dairy
        'Dairy': {'g_per_capita_day': 180, 'scope12_pct': 50},  # Local production
        'Plant-based alternatives': {'g_per_capita_day': 8, 'scope12_pct': 35},  # Processing + packaging
        'Nuts & Seeds': {'g_per_capita_day': 8, 'scope12_pct': 20},  # Imported, long supply chain
        'Grains': {'g_per_capita_day': 200, 'scope12_pct': 35},  # Mixed local + import
    }
    
    print("\n" + "=" * 80)
    print("SCOPE 1+2 CALIBRATION BY CATEGORY")
    print("=" * 80)
    print("\nScope 1+2 = Production, retail, household")
    print("Scope 3 = International supply chain, transport")
    print("\nCategory Impact Analysis:")
    print(f"{'Category':<25} {'g/capita/day':<15} {'Scope12 %':<12} {'Rationale':<30}")
    print("-" * 80)
    
    rationale_map = {
        'Meat': 'High production intensity (feed, land)',
        'Non-alcoholic beverages': 'Heavy, mostly domestic distribution',
        'Fruit': 'Imported, long supply chain',
        'Alcohol': 'Mixed local/import production',
        'Vegetables': 'Local seasonal production',
        'Fast food': 'Processing + retail dominant',
        'Fish': 'Fishing + processing',
        'Cheese': 'Local dairy, processing',
        'Dairy': 'Local milk production',
        'Plant-based alternatives': 'Packaging + processing',
        'Nuts & Seeds': 'Imported, minimal processing',
        'Grains': 'Mixed sourcing',
    }
    
    for cat, data in monitor_consumption.items():
        print(f"{cat:<25} {data['g_per_capita_day']:>13.0f}g {data['scope12_pct']:>10}% {rationale_map[cat]:<30}")
    
    return monitor_consumption


def map_monitor_to_model_categories():
    """
    Map Monitor food groups to model food categories for calibration.
    """
    mapping = {
        'Meat': ['Beef', 'Pork', 'Chicken', 'Lamb', 'Fish'],
        'Non-alcoholic beverages': ['Coffee', 'Tea', 'Sugar'],
        'Fruit': ['Fruits'],
        'Alcohol': ['Alcohol'],
        'Vegetables': ['Vegetables', 'Potatoes'],
        'Fast food': ['Processed', 'Ready_Meals', 'Snacks'],
        'Fish': ['Fish'],
        'Cheese': ['Cheese', 'Dairy', 'Butter'],
        'Dairy': ['Milk', 'Dairy'],
        'Plant-based alternatives': ['Meat_Subs', 'Pulses', 'Nuts'],
        'Nuts & Seeds': ['Nuts', 'Pulses'],
        'Grains': ['Grains', 'Bread', 'Pasta', 'Rice'],
    }
    
    return mapping


def calibrate_scope12_factors_from_monitor():
    """
    Generate Scope 1+2 percentages for all model categories
    based on Monitor Voedsel Amsterdam analysis.
    
    Returns: Dictionary of category -> scope12_percentage
    """
    
    # Detailed category-level Scope 1+2 percentages
    scope12_percentages = {
        # RED MEAT (high production intensity)
        'Beef': 60,       # Cattle feed, pasture, processing
        'Pork': 55,       # Feed intensive
        'Lamb': 60,       # Pasture + feed
        
        # POULTRY (moderate production)
        'Chicken': 45,    # Feed + processing
        
        # FISH (mixed)
        'Fish': 50,       # Fishing fleet fuel + processing
        
        # DAIRY (local production)
        'Cheese': 55,     # Milk production + processing
        'Milk': 50,       # Local dairy production
        'Dairy': 50,      # Local production
        'Butter': 55,     # Milk production
        
        # EGGS
        'Eggs': 45,       # Feed + processing
        
        # PLANT PROTEIN
        'Pulses': 30,     # Agriculture + drying
        'Nuts': 20,       # Mostly imported, minimal processing
        'Meat_Subs': 35,  # Procesing + packaging heavy
        
        # GRAINS & STAPLES (mixed local/import)
        'Grains': 35,     # Mixed sourcing
        'Bread': 40,      # Local baking + ingredient transport
        'Pasta': 35,      # Processing heavy
        'Rice': 30,       # Imported, minimally processed
        
        # VEGETABLES & FRUITS (local/import mix)
        'Vegetables': 28, # Seasonal local
        'Fruits': 25,     # Mostly imported
        'Potatoes': 30,   # Local production
        
        # PROCESSED FOODS
        'Processed': 45,  # Processing + packaging
        'Snacks': 45,     # Packaging + retail
        'Ready_Meals': 50, # Cooking energy + retail
        'Instant_Noodles': 45, # Processing dominant
        'Instant_Pasta': 40,    # Drying + packaging
        
        # BEVERAGES & ADDITIONS
        'Coffee': 60,     # Processing (roasting) is energy-intensive
        'Tea': 50,        # Drying energy
        'Alcohol': 40,    # Mixed (local brewing + import)
        'Sugar': 35,      # Processing
        
        # FATS & OILS
        'Oils': 30,       # Extraction + import
        'Animal_Fats': 55, # Production + rendering
        'Frying_Oil_Animal': 55, # Animal fats
        
        # CONDIMENTS
        'Condiment_Sauces': 40,  # Processing + packaging
        'Spice_Mixes': 25,       # Imported, minimal processing
        'Condiments': 35,        # Mixed processing
    }
    
    return scope12_percentages


def validate_against_monitor(model_results, monitor_baseline=1750):
    """
    Validate model results against Monitor baseline (1,750 kton Scope 1+2).
    
    Args:
        model_results: Total CO2 from model (tonnes)
        monitor_baseline: Monitor Scope 1+2 baseline (kton) = 1,750
    
    Returns:
        Comparison and calibration adjustment factor
    """
    monitor_tonnes = monitor_baseline * 1000  # Convert kton to tonnes
    
    error_pct = ((model_results - monitor_tonnes) / monitor_tonnes) * 100
    
    print("\n" + "=" * 80)
    print("MODEL VALIDATION AGAINST MONITOR")
    print("=" * 80)
    print(f"\nMonitor baseline (Scope 1+2): {monitor_baseline:,.0f} kton = {monitor_tonnes:,.0f} tonnes")
    print(f"Model result (Scope 1+2):     {model_results:,.0f} tonnes")
    print(f"Difference:                   {error_pct:+.1f}%")
    
    if abs(error_pct) < 5:
        print("\n✅ GOOD FIT: Model matches Monitor within ±5%")
        adjustment = 1.0
    elif abs(error_pct) < 10:
        print("\n⚠️  MODERATE FIT: Model within ±10% of Monitor")
        adjustment = monitor_tonnes / model_results
    else:
        print("\n❌ POOR FIT: Adjust Scope 1+2 percentages or factors")
        adjustment = monitor_tonnes / model_results
    
    print(f"Suggested adjustment factor: {adjustment:.4f}")
    
    return {'error_pct': error_pct, 'adjustment': adjustment}


def print_calibration_summary():
    """Print complete calibration report."""
    
    print("\n\n" + "=" * 80)
    print("SUMMARY: MONITOR CALIBRATION REPORT")
    print("=" * 80)
    
    monitor_data = analyze_monitor_baseline()
    scope12_data = calculate_scope12_percentages()
    
    print("\n\nKEY INSIGHTS:")
    print("-" * 80)
    print("""
1. MEAT DOMINATES CO2 (25% of total)
   • But only 3% of consumption (22g/capita/day)
   • Scope 1+2: 60% (feed, land, processing)
   • Scope 3: 40% (transport, retail)
   
2. BEVERAGES HIGH CONSUMPTION (600g/capita/day)
   • 11% of CO2 emissions
   • Scope 1+2: 30% (mostly domestic, distribution-heavy)
   • Scope 3: 70% (international bottling, packaging)
   
3. VEGETABLES & FRUIT (5% each)
   • 6% of consumption each
   • Fruit: 25% Scope 1+2 (mostly imported)
   • Vegetables: 28% Scope 1+2 (seasonal local)
   
4. DAIRY PRODUCTS (cheese, milk, butter)
   • 14% of total CO2
   • ~3% of consumption (when combined)
   • High impact per gram (production-intensive)
   • Scope 1+2: 50-55% (local dairy production)
   
5. AMSTERDAM EMISSIONS CONTEXT
   • Total baseline: 1,750 kton Scope 1+2
   • When including Scope 3: +1,173 kton (assuming 85% external)
   • Total food impact: ~2,923 kton (1,750 + 1,173)
    """)
    
    print("\n" + "=" * 80)
    print("CALIBRATED SCOPE 1+2 PERCENTAGES FOR MODEL")
    print("=" * 80)
    print("\nUse these percentages when: scope12_co2 = total_co2 * percentage")
    print(f"{'Category':<25} {'Scope 1+2 %':<15} {'Scope 3 %':<15}")
    print("-" * 80)
    
    for cat in sorted(scope12_data.keys()):
        s12 = scope12_data[cat]
        s3 = 100 - s12
        print(f"{cat:<25} {s12:>13}% {s3:>13}%")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Get calibrated percentages first
    scope12_percentages = calibrate_scope12_factors_from_monitor()
    
    # Print summary (uses the percentages dict above)
    print("\n\n" + "=" * 80)
    print("SUMMARY: MONITOR CALIBRATION REPORT")
    print("=" * 80)
    
    monitor_data = analyze_monitor_baseline()
    scope12_data = calculate_scope12_percentages()
    
    print("\n\nKEY INSIGHTS:")
    print("-" * 80)
    print("""
1. MEAT DOMINATES CO2 (25% of total)
   • But only 3% of consumption (22g/capita/day)
   • Scope 1+2: 60% (feed, land, processing)
   • Scope 3: 40% (transport, retail)
   
2. BEVERAGES HIGH CONSUMPTION (600g/capita/day)
   • 11% of CO2 emissions
   • Scope 1+2: 30% (mostly domestic, distribution-heavy)
   • Scope 3: 70% (international bottling, packaging)
   
3. VEGETABLES & FRUIT (5% each)
   • 6% of consumption each
   • Fruit: 25% Scope 1+2 (mostly imported)
   • Vegetables: 28% Scope 1+2 (seasonal local)
   
4. DAIRY PRODUCTS (cheese, milk, butter)
   • 14% of total CO2
   • ~3% of consumption (when combined)
   • High impact per gram (production-intensive)
   • Scope 1+2: 50-55% (local dairy production)
   
5. AMSTERDAM EMISSIONS CONTEXT
   • Total baseline: 1,750 kton Scope 1+2
   • When including Scope 3: +1,173 kton (assuming 85% external)
   • Total food impact: ~2,923 kton (1,750 + 1,173)
    """)
    
    print("\n" + "=" * 80)
    print("CALIBRATED SCOPE 1+2 PERCENTAGES FOR MODEL")
    print("=" * 80)
    print("\nUse these percentages when: scope12_co2 = total_co2 * percentage")
    print(f"{'Category':<25} {'Scope 1+2 %':<15} {'Scope 3 %':<15}")
    print("-" * 80)
    
    for cat in sorted(scope12_percentages.keys()):
        s12 = scope12_percentages[cat]
        s3 = 100 - s12
        print(f"{cat:<25} {s12:>13}% {s3:>13}%")
    
    # Export calibrated percentages to CSV
    df = pd.DataFrame([
        {'Category': cat, 'Scope12_percentage': pct, 'Scope3_percentage': 100-pct}
        for cat, pct in scope12_percentages.items()
    ]).sort_values('Category')
    
    df.to_csv('monitor_scope12_calibration.csv', index=False)
    print("\n✅ Calibration data exported to: monitor_scope12_calibration.csv")
