# Clean Diet Label Function Application Summary
**Purpose:** Ensure consistent, clean diet names across all charts and tables by removing numbered prefixes and parenthetical descriptors.

## Function Definition
```python
def clean_diet_label(diet_name):
    """Remove number prefix and standardize diet names"""
    # Remove number prefix (e.g., "1. " or "10. ")
    label = diet_name.split('. ', 1)[1] if '. ' in diet_name else diet_name
    # Remove parenthetical descriptors
    label = label.replace(' (Current)', '').replace(' (High Risk)', '')
    label = label.replace(' (Guideline)', '').replace(' (Planetary)', '')
    label = label.replace(' (60:40)', '').replace(' (70:30)', '')
    # Add (50-50) to Schijf van Vijf
    if 'Schijf van' in label or 'Schijf van 5' in label:
        label = 'Schijf van 5'
    return label
```

---

## Application Locations (20+ instances)

### 1. Chart 1a: Nexus Stacked Analysis
- **Lines:** 1603
- **Applied to:** Diet labels for horizontal stacked bars
- **CSV Export:** 1a_Nexus_Stacked_core.csv, 1a_Nexus_Stacked_all.csv
- **Status:** ✅ Applied

### 2. Chart 1b: Nexus Diverging Analysis
- **Lines:** 1673
- **Applied to:** Diet labels for diverging bars (excluding baseline)
- **CSV Export:** 1b_Nexus_Diverging_core.csv, 1b_Nexus_Diverging_all.csv
- **Status:** ✅ Applied

### 3. Chart 1c: System-Wide Impact Change
- **Lines:** 1921
- **Applied to:** Diet names in CSV export
- **CSV Export:** 1c_System_Wide_Impact_Change.csv
- **Status:** ✅ Applied

### 4. Chart 1d: System-Wide Impact Matrix
- **Lines:** 1991, 2054
- **Applied to:** Diet names in both core and appendix matrix CSV exports
- **CSV Export:** 1d_System_Wide_Impact_Matrix_core.csv, 1d_System_Wide_Impact_Matrix_all.csv
- **Status:** ✅ Applied

### 5. Chart 2: All Plates (Mass Composition)
- **Applied to:** Diet titles in subplots
- **Status:** ✅ Applied (existing)

### 6. Chart 3: All Emissions Donuts
- **Applied to:** Diet titles in subplots
- **Status:** ✅ Applied (existing)

### 7. Chart 4c: Scope Breakdown Waterfall
- **Lines:** 2458
- **Applied to:** Chart title for each baseline diet
- **Status:** ✅ Applied

### 8. Chart 4e: Reduction Pathways
- **Lines:** 2719, 2721
- **Applied to:** Baseline diet labels and goal diet labels on axes
- **Status:** ✅ Applied

### 9. Chart 4e (Appendix)
- **Lines:** 3013, 3015
- **Applied to:** All baseline and goal diet labels on axes
- **Status:** ✅ Applied

### 10. Chart 6: Scope 3 Tonnage Table
- **Lines:** 3715
- **Applied to:** Diet names in table columns (both wide and long CSV formats)
- **CSV Export:** 6_Table_Tonnage.csv, 6_Table_Tonnage_long.csv
- **Status:** ✅ Applied (UPDATED: Now uses clean_diet_label() instead of hard-coded abbreviations)

### 11. Core CSV Exports (Base Data)
- **Lines:** 1492, 1501, 1510, 1519, 1546
- **Applied to:**
  - emissions_scope12_by_category.csv
  - emissions_scope3_by_category.csv
  - impacts_land_use_by_category.csv
  - impacts_water_use_by_category.csv
  - diet_composition_by_category_grams.csv
- **Status:** ✅ NEWLY APPLIED (Updated)

### 12. Summary Totals CSV
- **Lines:** 1530
- **Applied to:** Diet names in emissions_totals_by_diet.csv
- **Status:** ✅ NEWLY APPLIED (Updated)

### 13. Additional Charts (Lines from grep search)
- **3339, 3391:** Applied in chart titles
- **3449, 3462:** Applied in chart comparison labels
- **3560:** Applied in donut chart titles
- **3576:** Applied in consumption impact table exports
- **3597:** Applied in dietary intake comparison data

---

## What Gets Cleaned

### Input Examples → Output Examples
| Input | Output |
|-------|--------|
| `1. Monitor 2024 (Current)` | `Monitor 2024` |
| `3. Metropolitan (High Risk)` | `Metropolitan` |
| `5. Dutch Goal (60:40)` | `Dutch Goal` |
| `6. Amsterdam Goal (70:30)` | `Amsterdam Goal` |
| `7. EAT-Lancet (Planetary)` | `EAT-Lancet` |
| `8. Schijf van 5 (Guideline)` | `Schijf van 5` |
| `9. Mediterranean Diet` | `Mediterranean Diet` |

---

## Benefits

✅ **Consistent appearance** across all visualizations and tables
✅ **Cleaner charts** without numbered prefixes
✅ **Professional presentation** - parenthetical descriptors removed
✅ **Better readability** - shorter, focused diet names
✅ **Unified CSV exports** - all data tables use the same clean naming

---

## Recent Updates

**Updated in Latest Commit:**
1. Applied `clean_diet_label()` to all core CSV data exports (Scope 1+2, Scope 3, Land, Water, Mass, Summary)
2. Updated `short_names` list to dynamically generate clean labels instead of hard-coded abbreviations
3. Ensured consistent application across Charts 1a, 1b, 1c, 1d, 4c, 4e, 6 and all related CSV files

**Total Occurrences:** 20+ locations in code

---

## How to Use in New Charts

When creating new charts or tables, simply apply the function:

```python
# For chart titles:
ax.set_title(f'{clean_diet_label(diet_name)}: Your Chart Title')

# For axis labels:
ax.set_yticklabels([clean_diet_label(d) for d in diet_list])

# For CSV exports:
export_row = {'Diet': clean_diet_label(diet_key), 'Category': cat, 'Value': value}

# For legend/labels:
labels = [clean_diet_label(d) for d in diet_names]
```

---

## Testing

To verify the function is working correctly, run:

```python
# Test cases
test_diets = [
    '1. Monitor 2024 (Current)',
    '3. Metropolitan (High Risk)',
    '5. Dutch Goal (60:40)',
    '6. Amsterdam Goal (70:30)',
    '7. EAT-Lancet (Planetary)',
    '8. Schijf van 5 (Guideline)',
    '9. Mediterranean Diet'
]

for diet in test_diets:
    print(f"{diet} → {clean_diet_label(diet)}")
```

**Expected Output:**
```
1. Monitor 2024 (Current) → Monitor 2024
3. Metropolitan (High Risk) → Metropolitan
5. Dutch Goal (60:40) → Dutch Goal
6. Amsterdam Goal (70:30) → Amsterdam Goal
7. EAT-Lancet (Planetary) → EAT-Lancet
8. Schijf van 5 (Guideline) → Schijf van 5
9. Mediterranean Diet → Mediterranean Diet
```

