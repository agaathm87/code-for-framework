"""
Diagnostic script to check raw Scope 1+2 calculation
Compares what we calculate vs what Amsterdam Monitor reports
"""
import pandas as pd

# Check the rivm_impact_factors_used.csv that was generated
df = pd.read_csv('rivm_impact_factors_used.csv')

print("\n" + "="*80)
print("RIVM IMPACT FACTORS ANALYSIS")
print("="*80)

print(f"\nLoaded {len(df)} food items from rivm_impact_factors_used.csv")
print(f"\nColumns: {df.columns.tolist()}")

# Show a sample
print(f"\nSample factors (first 5 items):")
print(df.head())

# Check the scope12 column
if 'scope12' in df.columns:
    print(f"\nScope 1+2 factors (kg CO2e per kg food):")
    print(df[['Food_Item', 'scope12']].to_string())
    
    print(f"\nScope 1+2 factor statistics:")
    print(f"  Mean: {df['scope12'].mean():.3f} kg CO2e/kg")
    print(f"  Min:  {df['scope12'].min():.3f} kg CO2e/kg ({df.loc[df['scope12'].idxmin(), 'Food_Item']})")
    print(f"  Max:  {df['scope12'].max():.3f} kg CO2e/kg ({df.loc[df['scope12'].idxmax(), 'Food_Item']})")

# Check if values look reasonable
if 'co2' in df.columns and 'scope12' in df.columns:
    df['scope12_pct'] = (df['scope12'] / (df['co2'] + df['scope12'])) * 100
    print(f"\nScope 1+2 as % of total emissions:")
    print(f"  Mean: {df['scope12_pct'].mean():.1f}%")
    print(f"  This should be ~15% if using 85/15 split")
    print(f"  If it's much different, the split ratio is wrong")
    
    print(f"\nDetailed breakdown by item:")
    print(df[['Food_Item', 'scope12_pct']].to_string())

print("="*80)
