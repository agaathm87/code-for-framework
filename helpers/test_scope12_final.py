#!/usr/bin/env python3
"""
Test Scope 1+2 calculation breakdown
"""
import sys
sys.path.append('.')

from Master_hybrid_Amsterdam_Model_v2 import load_impact_factors, diets, cfg, VISUAL_MAPPING, CAT_ORDER

factors = load_impact_factors()

# Test Monitor 2024 diet
profile = diets['Monitor 2024']
cat_totals = {cat: 0.0 for cat in CAT_ORDER}

for item, grams_day in profile.items():
    if item not in factors.index:
        continue
    kg_day = grams_day / 1000.0
    kg_year_person = kg_day * 365.0
    scope12_intensity = factors.loc[item, 'scope12'] if 'scope12' in factors.columns else 0.0
    co2_scope12_person_year = kg_year_person * scope12_intensity
    cat = VISUAL_MAPPING.get(item, item)
    if cat in cat_totals:
        cat_totals[cat] += co2_scope12_person_year
    else:
        cat_totals[cat] = co2_scope12_person_year

try:
    pop = cfg.POPULATION_TOTAL
except AttributeError:
    pop = None

if pop:
    for cat in cat_totals:
        cat_totals[cat] = (cat_totals[cat] * pop) / 1000.0

# Calculate Scope 1+2 components
base_s12 = sum(cat_totals.values())
waste_s12 = base_s12 * 0.11
retail_s12 = base_s12 * 0.025
total_s12 = base_s12 + waste_s12 + retail_s12

print("Scope 1+2 Breakdown - Monitor 2024 Diet (Tonnes CO2e/Year):")
print("=" * 90)
print(f"  Base food consumption:          {int(base_s12):>13,} tonnes ({base_s12/total_s12*100:.1f}%)")
print(f"  + Food waste (11%):             {int(waste_s12):>13,} tonnes ({waste_s12/total_s12*100:.1f}%)")
print(f"  + Retail/distribution (2.5%):   {int(retail_s12):>13,} tonnes ({retail_s12/total_s12*100:.1f}%)")
print("-" * 90)
print(f"  TOTAL Scope 1+2:                {int(total_s12):>13,} tonnes (100.0%)")
print("=" * 90)
print(f"  Monitor 2024 target: 1,750,000 tonnes")
error_pct = (total_s12 - 1750000) / 1750000 * 100
print(f"  Difference: {error_pct:+.2f}%")
print("=" * 90)
