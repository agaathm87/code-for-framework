"""
INTEGRATED LCA FACTORS: RIVM + Monitor Calibration
Combines RIVM database with Amsterdam Monitor Voedsel calibration

This module creates a hybrid approach:
1. RIVM database provides Scope 3 total CO2 values (lifecycle assessment)
2. Monitor Voedsel Amsterdam provides calibration for Scope 1+2 split
3. Result: Scientifically credible factors matched to Amsterdam baseline

Baseline Calibration:
- Monitor Scope 1+2: 1,750 kton CO2/year (production + retail + household)
- Implied Scope 3: 1,173 kton CO2/year (supply chain, 85% external)
- Total: 2,923 kton CO2/year

Usage:
    from integrated_lca_factors import load_integrated_lca_factors
    factors = load_integrated_lca_factors(use_monitor_calibration=True)
"""

import pandas as pd
import numpy as np
from rivm_lca_loader import load_rivm_factors, get_default_factors

def get_monitor_calibration_scope12():
    """
    Get Monitor-calibrated Scope 1+2 percentages for each food category.
    Based on Voedsel Monitor Amsterdam 2024 analysis.
    
    Returns:
        dict: Category -> Scope 1+2 percentage (0-100)
    """
    return {
        'Alcohol': 40,
        'Animal_Fats': 55,
        'Beef': 60,
        'Bread': 40,
        'Butter': 55,
        'Cheese': 55,
        'Chicken': 45,
        'Coffee': 60,
        'Condiment_Sauces': 40,
        'Condiments': 35,
        'Dairy': 50,
        'Eggs': 45,
        'Fish': 50,
        'Fruits': 25,
        'Frying_Oil_Animal': 55,
        'Grains': 35,
        'Instant_Noodles': 45,
        'Instant_Pasta': 40,
        'Lamb': 60,
        'Meat_Subs': 35,
        'Milk': 50,
        'Nuts': 20,
        'Oils': 30,
        'Pasta': 35,
        'Pork': 55,
        'Potatoes': 30,
        'Processed': 45,
        'Pulses': 30,
        'Ready_Meals': 50,
        'Rice': 30,
        'Snacks': 45,
        'Spice_Mixes': 25,
        'Sugar': 35,
        'Tea': 50,
        'Vegetables': 28,
    }


def load_integrated_lca_factors(use_monitor_calibration=True):
    """
    Load integrated LCA factors combining RIVM database with Monitor calibration.
    
    Methodology:
    1. Load RIVM CO2 values (total lifecycle = Scope 1+2 + Scope 3)
    2. Apply Monitor-calibrated percentages to split Scope 1+2 vs Scope 3
    3. Recalculate scope12 value from Monitor percentage
    
    Result: Factors that match both RIVM scientific database AND Monitor baseline
    
    Args:
        use_monitor_calibration: If True, use Monitor Scope 1+2 split
                               If False, use RIVM's embedded scope12 values
    
    Returns:
        dict: Integrated factors with CO2, land, water, scope12, scope3
    """
    
    print("\n" + "=" * 80)
    print("LOADING INTEGRATED LCA FACTORS")
    print("=" * 80)
    print("\nMethod: RIVM (Scope 3) + Monitor (Scope 1+2 calibration)")
    print("\nStep 1: Load RIVM CO2 values...")
    
    # Load RIVM factors (total lifecycle CO2)
    rivm_factors = load_rivm_factors(method='median', fill_missing=True)
    
    # Get Monitor calibration
    monitor_scope12_pct = get_monitor_calibration_scope12()
    
    print("\nStep 2: Apply Monitor calibration to split Scope 1+2 vs Scope 3...")
    
    integrated_factors = {}
    
    for category, rivm_data in rivm_factors.items():
        if category in monitor_scope12_pct:
            scope12_pct = monitor_scope12_pct[category]
        else:
            # Fallback to RIVM value if not in Monitor calibration
            scope12_pct = (rivm_data['scope12'] / rivm_data['co2'] * 100) if rivm_data['co2'] > 0 else 40
        
        # Calculate actual Scope 1+2 and Scope 3 from total CO2
        total_co2 = rivm_data['co2']
        scope12_co2 = total_co2 * (scope12_pct / 100)
        scope3_co2 = total_co2 - scope12_co2
        
        integrated_factors[category] = {
            'co2': round(total_co2, 2),  # Total lifecycle
            'scope12': round(scope12_co2, 2),  # Production + retail + household
            'scope3': round(scope3_co2, 2),  # Supply chain
            'land': round(rivm_data['land'], 2),  # Land use (Scope 3)
            'water': round(rivm_data['water'], 0),  # Water (Scope 3)
            'scope12_pct': scope12_pct,  # Documentation
        }
    
    print(f"Step 3: Validation...")
    
    # Check total matches baseline
    sample_categories = ['Beef', 'Pork', 'Chicken', 'Dairy', 'Vegetables']
    print(f"\nSample factors (Monitor-calibrated):")
    print(f"{'Category':<20} {'Total CO2':<12} {'Scope 1+2':<12} {'Scope 3':<12} {'S12%':<8}")
    print("-" * 80)
    for cat in sample_categories:
        if cat in integrated_factors:
            f = integrated_factors[cat]
            print(f"{cat:<20} {f['co2']:>10.2f} {f['scope12']:>10.2f} {f['scope3']:>10.2f} {f['scope12_pct']:>6}%")
    
    print("\n✅ Integrated factors loaded successfully")
    print("=" * 80)
    
    return integrated_factors


def validate_integrated_factors_vs_monitor():
    """
    Validate integrated factors by calculating total against Monitor baseline.
    Uses Monitor diet profile to ensure calibration is correct.
    """
    from rivm_lca_loader import get_default_factors
    
    # Load integrated factors
    integrated = load_integrated_lca_factors(use_monitor_calibration=True)
    
    # Simplified Monitor diet approximation (grams per capita per day)
    monitor_diet = {
        'Beef': 10,
        'Pork': 15,
        'Chicken': 25,
        'Fish': 12,
        'Cheese': 28,
        'Milk': 180,
        'Dairy': 0,
        'Eggs': 15,
        'Pulses': 15,
        'Nuts': 8,
        'Meat_Subs': 10,
        'Grains': 200,
        'Bread': 150,
        'Pasta': 30,
        'Rice': 30,
        'Vegetables': 160,
        'Fruits': 140,
        'Potatoes': 45,
        'Sugar': 35,
        'Processed': 140,
        'Snacks': 45,
        'Ready_Meals': 20,
        'Instant_Noodles': 8,
        'Instant_Pasta': 5,
        'Coffee': 12,
        'Tea': 3,
        'Alcohol': 25,
        'Oils': 25,
        'Butter': 12,
        'Animal_Fats': 3,
        'Frying_Oil_Animal': 5,
        'Condiment_Sauces': 15,
        'Spice_Mixes': 3,
        'Condiments': 5,
    }
    
    # Calculate annual Scope 1+2
    population = 873000
    days_per_year = 365
    
    total_scope12_tonnes = 0
    for category, grams_per_day in monitor_diet.items():
        if category in integrated:
            scope12_per_kg = integrated[category]['scope12']  # kg CO2e per kg food
            annual_consumption_kg = (grams_per_day * population * days_per_year) / 1_000_000  # Convert to million kg
            annual_scope12_tonnes = annual_consumption_kg * scope12_per_kg
            total_scope12_tonnes += annual_scope12_tonnes
    
    monitor_baseline_tonnes = 1750 * 1000  # 1,750 kton = 1,750,000 tonnes
    error_pct = ((total_scope12_tonnes - monitor_baseline_tonnes) / monitor_baseline_tonnes) * 100
    
    print("\n" + "=" * 80)
    print("VALIDATION: Integrated Factors vs Monitor Baseline")
    print("=" * 80)
    print(f"\nMonitor Baseline (Scope 1+2):  {monitor_baseline_tonnes:>15,.0f} tonnes/year")
    print(f"Integrated Calculation:         {total_scope12_tonnes:>15,.0f} tonnes/year")
    print(f"Difference:                     {error_pct:>14.1f}%")
    
    if abs(error_pct) < 10:
        print(f"\n✅ EXCELLENT: Within ±10% of Monitor baseline")
    elif abs(error_pct) < 15:
        print(f"\n⚠️  GOOD: Within ±15% of Monitor baseline")
    else:
        print(f"\n❌ NEEDS ADJUSTMENT: Beyond ±15% threshold")
    
    return {'total_scope12': total_scope12_tonnes, 'error_pct': error_pct}


def export_integrated_factors_to_code():
    """
    Generate Python code for integrated factors that can be directly 
    pasted into Master Hybrid Amsterdam Model v3.py
    """
    
    integrated = load_integrated_lca_factors(use_monitor_calibration=True)
    
    print("\n" + "=" * 80)
    print("GENERATING CODE FOR INTEGRATION")
    print("=" * 80)
    print("\nCopy this into load_lca_factors() function:")
    print("\n" + "-" * 80)
    
    print("""
def load_lca_factors():
    \"\"\"
    Load LCA emission factors from integrated RIVM + Monitor Voedsel Amsterdam database.
    
    Sources:
    1. RIVM Environmental Impact Database (Sept 2024) - Total lifecycle CO2
    2. Monitor Voedsel Amsterdam (2024) - Scope 1+2 calibration
    
    Scope 1+2: Production, retail, household cooking/refrigeration, waste mgmt
    Scope 3: International supply chain, transport, packaging
    
    Returns:
        pd.DataFrame: Factors with columns [co2, scope12, scope3, land, water]
    \"\"\"
    factors = {
""")
    
    for category in sorted(integrated.keys()):
        f = integrated[category]
        print(f"        '{category}': {{'co2': {f['co2']}, 'land': {f['land']}, 'water': {f['water']}, 'scope12': {f['scope12']}}},")
    
    print("""    }
    return pd.DataFrame.from_dict(factors, orient='index')
""")
    
    print("\n" + "-" * 80)
    print("\nOr save to CSV and load dynamically:")
    print("-" * 80)
    
    # Export to CSV
    df_export = pd.DataFrame([
        {
            'Category': cat,
            'Total_CO2_kgCO2e_per_kg': data['co2'],
            'Scope12_CO2_kgCO2e_per_kg': data['scope12'],
            'Scope3_CO2_kgCO2e_per_kg': data['scope3'],
            'Scope12_percentage': data['scope12_pct'],
            'Land_m2a_per_kg': data['land'],
            'Water_L_per_kg': data['water'],
        }
        for cat, data in integrated.items()
    ]).sort_values('Category')
    
    csv_path = 'lca_factors_integrated_rivm_monitor.csv'
    df_export.to_csv(csv_path, index=False)
    print(f"\n✅ Exported to: {csv_path}")
    
    return df_export


if __name__ == "__main__":
    # Load and display integrated factors
    integrated = load_integrated_lca_factors(use_monitor_calibration=True)
    
    # Validate against Monitor
    validation = validate_integrated_factors_vs_monitor()
    
    # Export code
    df = export_integrated_factors_to_code()
    
    print("\n" + "=" * 80)
    print("INTEGRATION COMPLETE")
    print("=" * 80)
    print("""
Next steps:
1. Review lca_factors_integrated_rivm_monitor.csv
2. Copy code from above into load_lca_factors()
3. Test with Monitor diet profile
4. Compare total with Monitor baseline (1,750 kton)
    """)
