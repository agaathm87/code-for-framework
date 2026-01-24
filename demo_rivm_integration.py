"""
DEMO: RIVM LCA Database Integration
Shows how to load and use RIVM emission factors in your model

Run this script to:
1. Load RIVM database
2. See comparison with current factors
3. Generate factors for your model
4. Export results to CSV

Author: Challenge Based Project Team
"""

from rivm_lca_loader import load_rivm_factors, export_rivm_factors_csv, get_default_factors
import pandas as pd


def main():
    print("\n" + "=" * 80)
    print(" RIVM LCA DATABASE INTEGRATION DEMO")
    print("=" * 80)
    
    # Method 1: Load RIVM factors with MEDIAN aggregation (recommended)
    print("\n📊 METHOD 1: Median aggregation (robust to outliers)")
    print("-" * 80)
    rivm_median = load_rivm_factors(method='median', fill_missing=True)
    
    # Method 2: Load with MEAN aggregation
    print("\n\n📊 METHOD 2: Mean aggregation (average values)")
    print("-" * 80)
    rivm_mean = load_rivm_factors(method='mean', fill_missing=True)
    
    # Method 3: Load with CONSERVATIVE aggregation (75th percentile)
    print("\n\n📊 METHOD 3: Conservative aggregation (precautionary principle)")
    print("-" * 80)
    rivm_conservative = load_rivm_factors(method='conservative', fill_missing=True)
    
    # Export all methods to CSV
    print("\n\n📁 EXPORTING RESULTS TO CSV...")
    print("-" * 80)
    export_rivm_factors_csv(rivm_median, 'rivm_factors_MEDIAN.csv')
    export_rivm_factors_csv(rivm_mean, 'rivm_factors_MEAN.csv')
    export_rivm_factors_csv(rivm_conservative, 'rivm_factors_CONSERVATIVE.csv')
    
    # Detailed comparison
    print("\n\n📈 DETAILED COMPARISON: CURRENT vs RIVM MEDIAN")
    print("=" * 80)
    
    defaults = get_default_factors()
    comparison_data = []
    
    for category in sorted(rivm_median.keys()):
        if category in defaults:
            current = defaults[category]
            rivm = rivm_median[category]
            
            comparison_data.append({
                'Category': category,
                'Current_CO2': current['co2'],
                'RIVM_CO2': rivm['co2'],
                'CO2_Delta_%': ((rivm['co2'] - current['co2']) / current['co2'] * 100) if current['co2'] > 0 else 0,
                'Current_Land': current['land'],
                'RIVM_Land': rivm['land'],
                'Land_Delta_%': ((rivm['land'] - current['land']) / current['land'] * 100) if current['land'] > 0 else 0,
                'Current_Water': current['water'],
                'RIVM_Water': rivm['water'],
                'Water_Delta_%': ((rivm['water'] - current['water']) / current['water'] * 100) if current['water'] > 0 else 0,
            })
    
    df_comparison = pd.DataFrame(comparison_data)
    df_comparison.to_csv('comparison_CURRENT_vs_RIVM.csv', index=False)
    
    # Print summary statistics
    print("\n📊 CO2 EMISSIONS COMPARISON SUMMARY:")
    print(f"  • Average difference: {df_comparison['CO2_Delta_%'].mean():+.1f}%")
    print(f"  • Max increase: {df_comparison['CO2_Delta_%'].max():+.1f}% ({df_comparison.loc[df_comparison['CO2_Delta_%'].idxmax(), 'Category']})")
    print(f"  • Max decrease: {df_comparison['CO2_Delta_%'].min():+.1f}% ({df_comparison.loc[df_comparison['CO2_Delta_%'].idxmin(), 'Category']})")
    
    print("\n📊 LAND USE COMPARISON SUMMARY:")
    print(f"  • Average difference: {df_comparison['Land_Delta_%'].mean():+.1f}%")
    
    print("\n📊 WATER USE COMPARISON SUMMARY:")
    print(f"  • Average difference: {df_comparison['Water_Delta_%'].mean():+.1f}%")
    
    # Show top 5 biggest changes
    print("\n\n🔝 TOP 5 LARGEST CO2 CHANGES (RIVM vs Current):")
    print("-" * 80)
    top5 = df_comparison.nlargest(5, 'CO2_Delta_%', keep='all')[['Category', 'Current_CO2', 'RIVM_CO2', 'CO2_Delta_%']]
    print(top5.to_string(index=False))
    
    print("\n\n🔻 TOP 5 LARGEST CO2 DECREASES (RIVM vs Current):")
    print("-" * 80)
    bottom5 = df_comparison.nsmallest(5, 'CO2_Delta_%', keep='all')[['Category', 'Current_CO2', 'RIVM_CO2', 'CO2_Delta_%']]
    print(bottom5.to_string(index=False))
    
    # Integration instructions
    print("\n\n" + "=" * 80)
    print(" HOW TO INTEGRATE INTO YOUR MODEL")
    print("=" * 80)
    print("""
OPTION 1: Direct replacement in load_lca_factors()
--------------------------------------------------
In Master Hybrid Amsterdam Model v3.py, replace the hardcoded factors dict with:

    from rivm_lca_loader import load_rivm_factors
    
    def load_lca_factors():
        # Load RIVM database
        factors = load_rivm_factors(method='median', fill_missing=True)
        return pd.DataFrame.from_dict(factors, orient='index')


OPTION 2: Hybrid approach (RIVM + manual overrides)
----------------------------------------------------
Use RIVM as base, but override specific categories:

    from rivm_lca_loader import load_rivm_factors
    
    def load_lca_factors():
        # Start with RIVM factors
        factors = load_rivm_factors(method='median', fill_missing=True)
        
        # Override specific categories with validated values
        factors['Beef']['co2'] = 28.0  # Keep Monitor-validated beef value
        factors['Coffee']['scope12'] = 23.34  # Keep verified scope split
        
        return pd.DataFrame.from_dict(factors, orient='index')


OPTION 3: Scenario comparison (test both datasets)
---------------------------------------------------
Run model with both factor sets to quantify sensitivity:

    # Run 1: Current factors
    results_current = run_full_analysis(use_rivm=False)
    
    # Run 2: RIVM factors
    results_rivm = run_full_analysis(use_rivm=True)
    
    # Compare total emissions
    delta = (results_rivm - results_current) / results_current * 100
    print(f"RIVM vs Current: {delta:+.1f}% difference")


RECOMMENDATION:
---------------
Use OPTION 2 (Hybrid approach) for publication:
  • RIVM provides scientific credibility and Dutch-specific data
  • Manual overrides preserve Monitor 2024 calibration
  • Document all overrides with clear justification
  • Include sensitivity analysis showing ±10% variation in LCA factors

FILES GENERATED:
----------------
✓ rivm_factors_MEDIAN.csv           - Recommended for general use
✓ rivm_factors_MEAN.csv             - Alternative aggregation
✓ rivm_factors_CONSERVATIVE.csv     - Precautionary estimates
✓ comparison_CURRENT_vs_RIVM.csv    - Side-by-side comparison

NEXT STEPS:
-----------
1. Review CSV files to validate RIVM mappings
2. Check categories with large deltas (>20%)
3. Verify Scope 1+2 percentages align with Monitor 2024
4. Test integrated model with sample diet profile
5. Document methodology in report (cite RIVM database version)
    """)
    
    print("\n✅ DEMO COMPLETE - Review generated CSV files")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
