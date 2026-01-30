"""
Quick test of RIVM database integration
"""
from rivm_lca_loader import load_rivm_factors, export_rivm_factors_csv

# Load factors
print("\nLoading RIVM factors...")
factors = load_rivm_factors(method='median', fill_missing=True)

# Export to CSV
print("\nExporting to CSV...")
export_rivm_factors_csv(factors, 'TEST_rivm_factors.csv')

# Show sample
print("\n=== SAMPLE FACTORS ===")
for cat in ['Beef', 'Chicken', 'Milk', 'Vegetables', 'Rice']:
    if cat in factors:
        f = factors[cat]
        print(f"{cat:15} CO2={f['co2']:6.2f}  Land={f['land']:6.2f}  Water={f['water']:8.0f}  Scope12={f['scope12']:6.2f}")

print("\n✅ Test complete - check TEST_rivm_factors.csv")
