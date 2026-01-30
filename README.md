# Hybrid Amsterdam Model: Urban Food Systems & Scope 3 Emissions
## Addressing the "Urban Paradox" in Climate Governance

**Publication-ready analysis framework for metropolitan food system emissions**

A comprehensive Python implementation of the **Hybrid Amsterdam Model** developed for the UvA Challenge-Based Project on Complex Systems for Policy. This research addresses the "Urban Paradox": cities pursuing net-zero targets while systematically ignoring transboundary supply chain emissions (Scope 3) that comprise 61% of their food-related carbon footprint.

The model synthesizes macro-level Life Cycle Assessment (LCA) with micro-level demographic inputs, quantifying Amsterdam's 4,487 kton CO₂e annual food emissions and evaluating dietary transition scenarios toward the city's 70:30 plant-based protein target.


---

## 🚀 Quick Start

### Running the Complete Analysis
```bash
python "Master Hybrid Amsterdam Model v3.py"
```

**Primary Output**: 
- `images/core/` — 30 publication-ready visualizations for policy communication
- `images/appendix/` — Full 9-diet analysis for scientific transparency
- `data/results/` — 64 CSV files for reproducibility and auditing

**Runtime**: ~100-120 seconds | **Total emissions quantified**: 4,487 kton CO₂e/year

---

## 📑 Research Framework

### Conceptual Foundation
The model operationalizes three integrated components:

| Component | Type | Purpose |
|-----------|------|---------|
| **GHG Scope Framework** | Theoretical | Reconfigures corporate Scope 1-2-3 definitions for municipal food systems |
| **Causal Loop Diagram (CLD)** | Qualitative | Maps governance constraints and infrastructural lock-ins (221 feedback loops) |
| **Hybrid Amsterdam Model** | Quantitative | Synthesizes macro-LCA with micro-demographics for spatial emissions analysis |

### Key Research Findings

**Baseline Assessment (Monitor 2024):**
- **Total Annual Emissions**: 4,487 kton CO₂e (5,138 kg/capita/year)
- **Scope 3 (Transboundary)**: 2,737 kton (61%) — Global supply chains
- **Scope 1+2 (Territorial)**: 1,750 kton (39%) — Local operations
- **Land Footprint**: 105,000 hectares (5.5× Amsterdam's surface area)

**Supply Chain Dependency:**
- 85% of Amsterdam's food originates outside the Netherlands
- Only 11% comes from surrounding provinces
- Validates Scope 3 dominance: most emissions occur beyond municipal control

**Dietary Transition Scenarios:**
| Scenario | Total Emissions | Reduction | Key Characteristic |
|----------|-----------------|-----------|-------------------|
| Monitor 2024 (Baseline) | 4,487 kton | — | 48% plant / 52% animal protein |
| Dutch Goal (60:40) | 3,680 kton | -18.0% | National 2030 target |
| **Amsterdam Goal (70:30)** | **3,350 kton** | **-25.3%** | **Highest feasible reduction** |
| EAT-Lancet | 3,450 kton | -23.1% | Planetary health boundaries |
| Metropolitan (Risk) | 5,420 kton | +20.8% | Western convenience pattern |

**Critical Barriers Identified:**
- **Socioeconomic Gradient**: 35% of minimum-income households cannot afford healthy meals
- **Food Swamps**: 68% perceive neighborhood overabundance of unhealthy options
- **Infrastructural Lock-in**: Waste-to-Energy dependencies conflict with waste reduction targets

---

## 📈 What's Included: 30 Total Visualizations

### Foundation Charts (1-4)
Establish baseline understanding and gaps to policy goals.

| # | Chart | Purpose | Focus | Output |
|---|-------|---------|-------|--------|
| 1 | **Nexus Analysis** | Multi-resource comparison | CO₂, Land, Water across diets | Bar charts |
| 2 | **All Plates** | Physical diet composition | Category breakdown by mass | Pie charts (grid) |
| 3 | **All Emissions** | Food category contributions | CO₂ by category with totals | Donuts (grid) |
| 4 | **Distance to Goals** | Gap to policy targets | % reduction needed for each goal | Heatmap |

### Transition Charts (5a-5e)
Visualize transformation from baseline to each policy goal.

| Chart | From | To | Type |
|-------|------|----|----|
| 5a | Monitor 2024 | Dutch Goal (60:40) | Sankey/transition |
| 5b | Monitor 2024 | Amsterdam Goal (70:30) | Sankey/transition |
| 5c | Monitor 2024 | EAT-Lancet (Planetary) | Sankey/transition |
| 5d | Monitor 2024 | Schijf van 5 (Guideline) | Sankey/transition |
| 5e | Monitor 2024 | Mediterranean Diet | Sankey/transition |

### Scope Analysis (6-8)
Breakdown of Scope 1+2 (production) vs Scope 3 (transport/processing) emissions.

| # | Chart | Purpose | Key View |
|---|-------|---------|----------|
| 6 | **Scope 1+2 vs Scope 3** | Total by scope type | ~40% Scope 3, ~60% Scope 1+2 |
| 7 | **Scope Shares** | Percentage breakdown | Consistency across diets |
| 8 | **All Total Emissions** | 9-diet donuts (Scope 1+2+3) | Complete system view |

### Detailed Analysis (9-13)
In-depth food system analysis by category, type, and nutritional content.

| # | Chart | X-axis | Y-axis | Usage |
|---|-------|--------|--------|-------|
| 9 | **CO₂ vs Mass Share** | Share of consumption mass (%) | Share of CO₂ emissions (%) | Identify inefficient foods |
| 10 | **Impact by Food Type** | Plant / Animal / Processed | Scope 1+2 / Scope 3 (stacked %) | Compare production methods |
| 11 | **Emissions vs Protein** | Total protein (g/person/day) | Total emissions (kton CO₂e) | Assess nutritional efficiency |
| 12 | **Dietary Intake** | Food items/categories | Consumption (g/day) vs Schijf van 5 | Check nutritional alignment |
| 13 | **Amsterdam Infographic** | Monitor 2024 breakdown | Top 6 categories by emissions | System overview figure |

### Delta Analysis (14a-14d)
Quantify emissions changes when adopting each policy goal.

| # | Chart | Metric | Purpose |
|---|-------|--------|---------|
| 14a | **Total Emissions Delta** | Total CO₂ change (kton) | Overall reduction potential |
| 14b | **Category-Level Delta** | Per-category change | Identify high-impact shifts |
| 14c | **Mass vs CO₂ Share** | Dual axis comparison | Decoupling analysis |
| 14d | **Scope 1+2 vs Scope 3** | Scope breakdown for goals | Identify scope opportunities |

### **🌟 Sensitivity Analysis Suite (16a-16e) — COMPREHENSIVE 5-VISUALIZATION ANALYSIS**

**Baseline**: Monitor 2024 (2,923,844 kton CO₂e/year)

**Parameters Analyzed**:
| Parameter | Variation | Impact | Rank |
|-----------|-----------|--------|------|
| **Diet Adherence** | ±20% | ±350,861 kton | 🥇 1st (CRITICAL) |
| **Impact Factors** | ±10% | ±292,384 kton | 🥈 2nd |
| **Waste Rate** | ±3% | ±116,954 kton | 🥉 3rd |
| **Total Range** | **-17% to +17%** | **±34% from baseline** | |

**5 Complementary Visualizations**:

| Chart | Format | Purpose | Best For |
|-------|--------|---------|----------|
| **16a: Tornado** | Horizontal bars | Rank impacts visually | Quick reference (policy brief) |
| **16b: Table** | APA-styled data | Numerical precision | Technical reports |
| **16c: Grouped** | Grouped bars (3 params × diets) | Multi-diet comparison | Sensitivity across scenarios |
| **16d: Radar** | Polar/spider plot | Holistic parameter profile | Scientific papers |
| **16e: Waterfall** | Cascading bars | Cumulative impact stacking | Uncertainty visualization |

**Key Insight**: Diet adherence (consumption volume) is the **single most important uncertainty driver**, far exceeding impact factor and waste rate uncertainties.

### Data Tables & References (15, 17-18)

| # | Chart | Content | Export |
|---|-------|---------|--------|
| 15 | **APA Table** | Emissions by diet & category | PNG + CSV |
| 17 | **Category Comparison** | Emissions by category vs reference | Line plot |
| 18 | **Intake Comparison** | Dietary intake vs Schijf van 5 | Grouped bars |

---

## 📊 Data Exports Catalog

### **Reproducibility: 64 CSV Files Exported**

All visualizations (charts 1–16) export underlying data to `data/results/` for reproducibility, auditing, and downstream analysis.

**Quick Access**: See [`data/results/EXPORT_MANIFEST.csv`](data/results/EXPORT_MANIFEST.csv) for the complete file catalog with schemas.

### Export Categories

#### 1. Core Calculation Outputs (6 files)
Foundational datasets generated from diet compositions and impact factors.

| File | Rows | Schema | Description |
|------|------|--------|-------------|
| `emissions_scope12_by_category.csv` | 126 | diet, category, scope12_tonnes_per_year | Scope 1+2 emissions (production, retail, waste) by food category for all 9 diets |
| `emissions_scope3_by_category.csv` | 126 | diet, category, scope3_tonnes_per_year | Scope 3 emissions (supply chain, transport) by food category |
| `impacts_land_use_by_category.csv` | 126 | diet, category, land_use_m2_per_year | Land use impacts by food category |
| `impacts_water_use_by_category.csv` | 126 | diet, category, water_use_L_per_year | Water use impacts by food category |
| `emissions_totals_by_diet.csv` | 9 | diet, total_scope12_tonnes, total_scope3_tonnes, grand_total_tonnes | Aggregated emission totals across all scopes |
| `diet_composition_by_category_grams.csv` | 126 | diet, category, grams_per_day | Daily intake in grams by food category |

#### 2. Charts 1–4: Nexus, Composition, and Goal Distances (24 files)
Multi-resource analysis, diet composition, and policy goal gap analysis.

**Core vs Appendix**: Charts 1–4 export both `_core.csv` (3-7 focus diets) and `_all.csv` (full 9 diets) variants.

**Key Files**:
- `1a_Nexus_Stacked_*.csv` — CO₂/land/water percentage composition
- `1b_Nexus_Diverging_*.csv` — Percent change vs baseline (long-form: diet, resource, pct_change)
- `1c_System_Wide_Impact_Change.csv` — System-wide aggregate changes
- `2_All_Plates_Mass_*.csv` — Mass share by food category
- `3_All_Emissions_Donuts_*.csv` — Scope 3 emission shares
- `4_Distance_To_Goals_*.csv` — Reduction percentages needed to reach each goal
- `4a_Distance_*_*.csv` — Separate scope 3 and total distance matrices
- `4b_Gap_Analysis_Readiness_*.csv` — Long-form gap data (base_diet, goal_diet, gap_distance_pct)
- `4c_Scope_Breakdown_Waterfall_*.csv` — S1+2/S3 current vs goal averages with reduction %
- `4d_Diet_Shift_Categories_*.csv` — Top 8 category deltas per baseline→goal transition
- `4e_Reduction_Pathways_*.csv` — Matrix replicating distance-to-goals for pathway visualization

#### 3. Charts 5–8: Transitions, Scopes, and Totals (10 files)
Transition scenarios, scope breakdowns, and comprehensive emission totals.

| File | Schema | Description |
|------|--------|-------------|
| `5_Transitions_Scope3_by_Category.csv` | Baseline, Goal, Category, Baseline/Goal scope3 values, Delta, Delta_pct | Scope 3 changes for all baseline→goal pairs (5 transitions × 14 categories) |
| `6_Scope12_vs_Scope3_Total_core.csv` | Diet, Scope 1+2, Scope 3, Total | Absolute emissions by scope (focus diets) |
| `6_Scope12_vs_Scope3_Total_all.csv` | Diet, Scope 1+2, Scope 3, Total | Absolute emissions by scope (all 9 diets) |
| `6_Table_Tonnage.csv` | Category, [9 diet columns] | Wide format: scope 3 tonnage per category and diet |
| `6_Table_Tonnage_long.csv` | Diet, Category, Scope3_tonnes_per_year | Long format variant for easy analysis |
| `7_Scope_Shares_core.csv` | Diet, Scope1+2_share_pct, Scope3_share_pct | Percentage shares of each scope (focus diets) |
| `7_Scope_Shares_all.csv` | Diet, Scope1+2_share_pct, Scope3_share_pct | Percentage shares of each scope (all 9 diets) |
| `8_Total_Emissions_by_Category_all.csv` | Diet, Category, Total_emissions_tonnes_per_year | Combined S1+2+3 emissions per category |

#### 4. Charts 9–13: Detailed Breakdowns and Infographic (10 files)
Category-level scope breakdown, multi-resource impacts, protein efficiency, dietary intake vs reference, and infographic summary data.

| File | Schema | Description |
|------|--------|-------------|
| `9_Scope_Breakdown_by_Category.csv` | Diet, Category, Scope1+2/Scope3/Total tonnes, Scope1+2/Scope3 pct | Full scope breakdown by category for all 9 diets (126 rows) |
| `9_CO2_vs_Mass_Share.csv` | Diet, Category, CO2_share_pct, Mass_share_pct | Share in emissions vs share in consumption (126 rows) |
| `10_Multi_Resource_Impact.csv` | Diet, Food_Type, CO2_pct, Land_pct, Water_pct | Multi-resource % by food type (plant/animal/dairy/processed/oils/fats) |
| `10_Impact_by_Food_Type.csv` | Diet, Food_Type, CO2_pct | Simplified CO₂ impact by food type (4 comparison diets) |
| `11_Emissions_vs_Protein.csv` | Diet, Category, Emissions_share_pct, Protein_share_pct | Emissions efficiency vs protein contribution (all 9 diets) |
| `11_Mass_vs_Protein.csv` | Diet, Category, Mass_share_pct, Protein_share_pct | Dietary mass vs protein contribution (all 9 diets) |
| `12_Diets_vs_Goals_MultiResource.csv` | Diet, Goal_Reference, Resource, Pct_vs_goal | Multi-resource gap: 4 diets × 4 goals × 3 resources = 48 rows |
| `12b_Emissions_vs_Reference_MultiGoal.csv` | Diet, Goal_Reference, Total_emissions_pct_of_goal, Goal/Diet totals | Total emissions comparison (4 diets × 4 goals) |
| `12_Dietary_Intake_Comparison.csv` | Diet, Category, Pct_of_reference, Diet/Reference mass values | Intake vs Schijf van 5 reference (5 diets × 14 categories) |
| `13_Infographic_Summary.csv` | Total_Scope12/Scope3/Emissions, Base_Food, Waste, Retail, Land, Water totals | Key infographic metrics (Monitor 2024 baseline) |
| `13_Infographic_Top6_Categories.csv` | Category, Scope1+2/Scope3/Total kton, Mass/Scope3 share % | Top 6 emitting categories for infographic panel |

#### 5. Charts 14a–d: Delta Analysis (4 files)
Quantify emission changes when transitioning from baseline diets to policy goals.

| File | Schema | Description |
|------|--------|-------------|
| `14a_Delta_Analysis_Total_Emissions.csv` | Baseline_Diet, Goal_Diet, Baseline/Goal totals, Reduction_pct | Total emissions change (3 focus × 4 goals = 12 transitions) |
| `14b_Delta_Analysis_By_Category.csv` | Goal_Diet, Category, Baseline/Goal tonnes, Delta_kton, Delta_pct | Category-level deltas from Monitor 2024 to each goal (4 goals × 14 categories) |
| `14c_Mass_vs_Emissions_Share.csv` | Diet, Category, Mass_share_pct, Emissions_share_pct, Gap_pct | Mass vs emissions gap (over-emitting categories, 3 focus diets) |
| `14d_Scope_Breakdown_Baseline_vs_Goals.csv` | Focus_Diet, Scenario, Scope1+2_kton, Scope3_kton, Total_kton | Scope breakdown across scenarios (3 focus × 5 scenarios = 15 rows) |

#### 6. Charts 15–16: APA Summary and Sensitivity Analysis (11 files)
Publication-ready APA table and comprehensive sensitivity suite.

| File | Schema | Description |
|------|--------|-------------|
| `15_APA_emissions_summary.csv` | Diet, Scope 1+2 (kton), Scope 3 (kton), Total (kton), S1+2 %, S3 % | APA-formatted emissions summary (4 key diets) |
| `16a_Sensitivity_Tornado_Diagram.csv` | parameter, baseline/low/high values, low/high impacts | Tornado diagram data (parameter rankings) |
| `16b_Sensitivity_Analysis_Table.csv` | parameter, baseline, low, high, impact_range | Sensitivity analysis table |
| `16c_Sensitivity_Grouped_Comparison.csv` | group, parameter, impact_range | Grouped sensitivity comparison |
| `16d–16i_Sensitivity_*.csv` | various schemas | Additional sensitivity visualizations (radar, waterfall, scenario stacking, feasibility, heatmap, policy levers) |
| `sensitivity_analysis_parameters.csv` | parameter, baseline, low, high, impact_low, impact_high | Master sensitivity parameter definitions |

### Verification and Regeneration

**Verify Exports**:
```bash
cd data/results
ls *.csv | wc -l  # Should return 64
```

**Regenerate All Exports**:
```bash
python "Master Hybrid Amsterdam Model v3.py"
```
All CSVs are regenerated in `data/results/` each run. Existing files are overwritten.

**Schema Consistency**:
- **Diet names**: Cleaned labels (e.g., "Monitor 2024" instead of "1. Monitor 2024 (Current)")
- **Percentages**: Columns ending in `_pct` are percentages (0-100 scale)
- **Absolute values**: Tonnes CO₂e per year, m² land, L water
- **Long vs wide formats**: Most exports use long-form (diet, category, value); some use wide matrices for direct visual mapping

---

## 📊 Methodology: The Hybrid Approach

### Three-Scale Integration

**Macro-Level: Transboundary LCA Logic**
- Quantifies global environmental "load" of food products through international supply chains
- Incorporates Land Use Change (LUC), blue water usage, and full lifecycle impacts
- Data source: RIVM Environmental Impact Database (September 2024 version)

**Meso-Level: Systemic Governance Framework**
- Causal Loop Diagram mapping 221 feedback loops
- Identifies leverage points: dietary shifts and waste reduction
- Reveals "infrastructural lock-ins" (e.g., Waste-to-Energy dependencies)

**Micro-Level: Neighborhood Disaggregation**
- Spatial microsimulation to Buurt (neighborhood) level
- Demographics: 873,374 residents (2024), 7 administrative districts
- Heterogeneity multipliers: Income Scalar (Volume Beta) × Education Modifier (Plant Beta)

### Mathematical Formalization

**Total Emissions:**
```
E_total = Σ(districts) Σ(categories) M_actual × β_heterogeneity × EF_combined
```

Where:
- **M_actual** = Produced mass accounting for 15% supply chain waste
- **β_heterogeneity** = f(income, education) — Dual-driver mechanism
- **EF_combined** = EF_scope3 + EF_scope12 (transboundary + local)

**Income Scalar (Volume Beta):**
```
β_volume = 0.8 × exp(0.2 × (income_neighborhood / 38,300))
```
0.2% increase in food expenditure per 1% income increase above national average

**Education Scalar (Plant Beta):**
```
β_plant = 0.85  if education% > 50%  (high-education areas)
         1.10  otherwise              (low-education areas)
```

**Key Insight**: High-income, high-education neighborhoods (e.g., Amsterdam Zuid) show similar total emissions to middle-income areas because education-driven plant preference offsets income-driven volume increases.

### Data Sources & Calibration

| Component | Source | Coverage |
|-----------|--------|----------|
| **Consumption Baseline** | Amsterdam Monitor 2024 | 1,833 participants (weighted to 1,872) |
| **LCA Factors** | RIVM Database | 411 products, 29 food categories |
| **Demographics** | KBT 2025 & CBS 2023 | 7 districts, income/education profiles |
| **Cultural Diversity** | HELIUS Study | 5 major ethnic groups dietary patterns |
| **Protein Content** | NEVO 2023 | Dutch Food Composition Database |

**Calibration Target**: Monitor 2024 verified baseline (1,750 kton Scope 1+2) achieved within 0.06% error.

---

## 🎨 Design Standards

### Color Palette
**Paul Tol Colorblind-Safe Palette** (14 colors for food categories)

Consistent category ordering throughout all visualizations ensures readers can quickly identify foods across charts.

### Typography & Spacing
- **Titles**: 13-16pt bold, pad=15 to avoid subplot overlap
- **Labels**: 9-11pt regular weight
- **Legends**: 9-10pt with frameOn=True
- **Margins**: 0.5-1.0 inch (all sides)
- **All value labels**: Externally positioned (NO overlapping text)

### Quality Checklist
- ✅ NO overlapping labels or clipped text
- ✅ All value labels externally positioned
- ✅ Legends present on all charts (frameOn=True)
- ✅ Paul Tol colorblind-safe palette
- ✅ Consistent spacing & margins
- ✅ Grid backgrounds don't obscure data
- ✅ Proper font sizing (readable at 100% zoom)
- ✅ Suptitles avoid subplot overlap

---

## 📁 Output Folder Structure

```
images/
├── core/
│   ├── 1_Nexus_Analysis.png
│   ├── 2_All_Plates_Mass.png
│   ├── 3_All_Emissions_Donuts.png
│   ├── 4_Distance_To_Goals.png
│   ├── 5a_Transition_Dutch.png
│   ├── 5b_Transition_Amsterdam.png
│   ├── 5c_Transition_EAT.png
│   ├── 5d_Transition_Schijf.png
│   ├── 5e_Transition_Mediterranean.png
│   ├── 6_Scope12_vs_Scope3_Total.png
│   ├── 7_Scope_Shares.png
│   ├── 8_All_Total_Emissions_Donuts.png
│   ├── 9_CO2_vs_Mass_Share.png
│   ├── 10_Impact_by_Food_Type.png
│   ├── 11_Emissions_vs_Protein.png
│   ├── 12_Dietary_Intake_Comparison.png
│   ├── 13_Amsterdam_Food_Infographic.png
│   ├── 14a_Delta_Analysis_Total_Emissions.png
│   ├── 14b_Delta_Analysis_By_Category.png
│   ├── 14c_Mass_vs_Emissions_Share.png
│   ├── 14d_Scope_Breakdown_Baseline_vs_Goals.png
│   ├── 15_Table_APA_Emissions.png
│   ├── 16a_Sensitivity_Tornado_Diagram.png      ⭐ NEW
│   ├── 16b_Sensitivity_Analysis_Table.png       ⭐ NEW
│   ├── 16c_Sensitivity_Grouped_Comparison.png   ⭐ NEW
│   ├── 16d_Sensitivity_Radar_Chart.png          ⭐ NEW
│   ├── 16e_Sensitivity_Waterfall_Chart.png      ⭐ NEW
│   ├── 17_Emissions_by_Category_vs_Reference.png
│   └── 18_Dietary_Intake_vs_Reference.png
│
└── appendix/
    ├── All 30 files identical to core/
    ├── 15_Table_APA_Emissions.csv
    └── (Full 9-diet detail for each visualization)
```

**Output Statistics**:
- Core folder: 30 files (~10.3 MB, 150-300 DPI)
- Appendix folder: 30 files + 1 CSV (~12.5 MB, 150-300 DPI)

---

## � Policy Implications & Leverage Points

### High-Impact Interventions (Ranked)

| Intervention | Climate Impact | Implementation Cost | Timeline | Key Barrier |
|--------------|----------------|---------------------|----------|-------------|
| **Dietary shift (70:30)** | -25.3% | Medium | 5-10 years | Food affordability |
| **Waste reduction (-3%)** | -2.7% | Low | Immediate | Infrastructure lock-in |
| **Supply chain optimization** | -5-8% | High | 10+ years | Data transparency |
| **Local sourcing** | -2-4% | Medium | 5-10 years | Production capacity |

### Critical Findings for Urban Governance

**1. Territorial Accounting is Insufficient**
- Current Scope 1+2 focus captures only 39% of food-related emissions
- 61% (2,737 kton) occurs in transboundary supply chains
- Cities must shift from passive territorial reporting to active consumption-based management

**2. The "Volume vs. Composition" Paradox**
- Wealthy neighborhoods: High total consumption × Plant-based preference = Moderate emissions
- Low-income neighborhoods: Lower consumption × Meat-heavy diet = Comparable emissions
- Implication: Income-based interventions alone are insufficient

**3. Socioeconomic Equity Constraints**
- 35% of minimum-income households face food poverty
- Plant-based foods perceived as expensive choice
- Without subsidies, Amsterdam Goal (70:30) may achieve only 15-18% reduction vs. theoretical 25.3%

**4. Infrastructural Lock-ins**
- Waste-to-Energy facilities create perverse incentives against waste reduction
- Cold chain optimization conflicts with local sourcing goals
- Municipal capacity constrained by vertical governance (national/EU regulations)

### Sensitivity Analysis Results

**Parameter Uncertainty (±20% baseline range):**

| Parameter | Baseline | Impact Range | Sensitivity Rank |
|-----------|----------|--------------|------------------|
| **Diet Adherence** | Monitor 2024 | ±897 kton CO₂e | 🥇 CRITICAL |
| **Impact Factors** | RIVM Database | ±449 kton CO₂e | 🥈 High |
| **Waste Rate** | 15% supply chain | ±135 kton CO₂e | 🥉 Moderate |

**Cross-Scenario Insight**: Animal-heavy diets (Metropolitan, Metabolic) show 2× higher waste sensitivity due to longer livestock supply chains and waste-prone processing stages.

---

## 🔬 Methodology

### Data Sources
1. **Food Consumption**: Amsterdam Monitor 2024 survey (empirical DNFCS data)
2. **Emission Factors**: Scope 1+2 (production) + Scope 3 (transport/processing)
3. **Impact Metrics**: CO₂ (primary), Land use, Water use
4. **Nutritional Data**: Protein content by food item

### Calculations
- **Consumption**: grams/person/day from standardized diet profiles
- **Emissions**: kg CO₂e/person/day (sum across all foods)
- **Scope Split**: Scope 1+2 vs Scope 3 explicit breakdown
- **Categories**: 14 granular food categories
- **Sensitivity**: ±10-20% parameter variation from baseline values

### 14 Food Categories (Granular)
1. Red Meat
2. Poultry
3. Fish
4. Shellfish
5. Eggs
6. Dairy
7. Oils & Fats
8. Grains
9. Legumes
10. Vegetables
11. Fruits
12. Nuts & Seeds
13. Condiments
14. Processed Foods

---

## 💡 Usage Guide

### For Policy Briefs
1. **Start with**: Chart 1 (Nexus) for multi-resource overview
2. **Add context**: Charts 4 (Distance) + 14a (Delta) for reduction targets
3. **Include uncertainty**: Chart 16a (Tornado) for sensitivity context
4. **Show scenarios**: Charts 5a-5e (Transitions) for pathway options

### For Academic Reports
1. **Establish baseline**: Charts 2-3 (Plates/Emissions) 
2. **Detailed analysis**: Charts 9-12 (Food-specific breakdown)
3. **Uncertainty quantification**: Chart 16 (full 5-visualization suite)
4. **Reference data**: Table 15 (APA-formatted)
5. **Comparative context**: Charts 17-18

### For Stakeholder Presentations
1. **System overview**: Chart 13 (Infographic)
2. **Scenario comparison**: Charts 5a-5e (Transitions)
3. **Cumulative impacts**: Chart 16e (Waterfall)
4. **Feasibility assessment**: Chart 4 (Distance to Goals)

### For Scientific Publications
1. **Holistic view**: Chart 16d (Radar - normalized parameter space)
2. **Scenario sensitivity**: Chart 16c (Grouped - multi-diet comparison)
3. **Nutritional context**: Charts 11-12 (Protein/Intake efficiency)
4. **Supplementary data**: Table 15 (APA format)

---

## ⚠️ Known Limitations

- **Transition charts (5a-5e)**: No explicit legends (baseline vs goal color coding could be clearer)
- **Sensitivity analysis**: Based on ±10-20% parameter variation (not full Monte Carlo uncertainty quantification)
- **Spatial analysis**: No neighborhood-level disaggregation (city-level aggregation only)
- **Behavioral factors**: Simplified education modifier (doesn't capture full socioeconomic complexity)
- **Time dynamics**: Static snapshot (no temporal projections or trends)
- **Supply chain detail**: Aggregated impact factors (not supply-chain-specific)

---

## 🚀 Future Enhancements

- [ ] Add legends to transition charts (5a-5e) showing baseline vs goal diet color coding
- [ ] Implement Monte Carlo uncertainty quantification (beyond ±10-20% fixed ranges)
- [ ] Develop neighborhood-level spatial analysis
- [ ] Include expanded education/income behavioral modifiers
- [ ] Add temporal trend analysis and future projections
- [ ] Create interactive web dashboard (Plotly/Streamlit)
- [ ] Expand to regional/national comparisons
- [ ] Include circular economy and food waste reduction scenarios
- [ ] Develop cost-benefit analysis module

---

## 📧 Project Information



**Academic Context:**
- **Project**: Challenge-Based Project: Complex Systems for Policy
- **Institution**: University of Amsterdam (UvA)
- **Partner**: Gemeente Amsterdam (Department of Sustainability)
- **Academic Year**: 2024-2025
- **Submission Date**: January 30, 2026


**Model Version**: v3.1  
**Last Updated**: January 30, 2026

---

## 🎯 Research Question

**Primary RQ:**  
*"How does the lack of acknowledgement of the role of food impact emission Scope 3 of metropolitan cities to pursue climate neutrality?"*

**Sub-Questions:**
1. What is the role of food within urban Scope 3 emissions?
2. What governance and informational constraints limit municipal influence over food-related emissions?
3. What types of insights do cities require to integrate food systems into climate strategies?

**Operational Translation:**  
The CLD's central variable "food-related GHG emissions of metropolitan cities" serves as the quantitative anchor, connecting theoretical frameworks to empirical measurement.

---

## 📄 License & Academic Integrity

**AI Usage Statement:**  
We declare compliance with UvA rules regarding fraud and plagiarism. AI tools (ChatGPT, Claude) were used for:
- Grammar and spelling refinement
- Diagnostic testing during model development
- Debugging coding syntax errors
- Code logic verification

All content, analysis, conceptual frameworks, and argumentation are original work by the research team.

**Usage Rights:**  
This analysis is provided for academic, policy research, and stakeholder engagement purposes. The framework supports:
- Municipal climate strategy development
- Academic research and peer review
- Policy analysis and target setting
- Stakeholder communication and education

**Citation:**  
If using this model or methodology, please cite:
```
Keet, T., Učelniece, M., & de Vries, A. (2026). Hybrid Amsterdam Model: 
Addressing the Urban Paradox in Food System Emissions. Challenge-Based 
Project, University of Amsterdam.
```

---

## 🔬 Methodological Strengths & Limitations

### Strengths
✅ **Triangulated Approach**: Integrates theoretical (Scope frameworks), qualitative (CLD), and quantitative (Hybrid Model) methods  
✅ **Empirical Calibration**: Monitor 2024 baseline validated within 0.06% error  
✅ **Spatial Granularity**: Neighborhood-level disaggregation enables targeted interventions  
✅ **Behavioral Realism**: Education modifier captures non-linear dietary preferences  
✅ **Policy Relevance**: Directly aligned with Amsterdam's Six Pillars for Food Security  
✅ **Transparency**: 64 CSV exports ensure full reproducibility  

### Limitations & Future Research Directions

**Data Constraints:**
- ⚠️ Uniform Waste Coefficient (15%) — Lacks category-specific waste rates
- ⚠️ Secondary LCA data — "Data Blockade" prevents retailer-specific supply chain analysis
- ⚠️ RIVM database limited to 411 products, 29 food categories

**Methodological Boundaries:**
- ⚠️ Fixed Infrastructure Assumption — Scope 1+2 held constant at 1,750 kton
- ⚠️ Static Elasticity Coefficients — May understate rapid cultural/market shifts
- ⚠️ Water-Carbon Nexus Blind Spot — Neglects blue water footprint of imports

**Generalizability:**
- ⚠️ Amsterdam-specific parameters — Demographics (Surinamese/Turkish/Moroccan mix) not directly transferable
- ⚠️ Methodology is replicable; coefficients require local recalibration

**Recommended Extensions:**
1. Dynamic Infrastructure Modeling (variable Scope 1+2 under dietary transitions)
2. Integration of "Action Line 1" (Food from the Region) to quantify local vs. global trade-offs
3. Nutritional adequacy assessment (protein quality, micronutrients)
4. Cost-benefit analysis linking affordability constraints to emission targets
5. Temporal trend analysis and 2030/2050 projections
6. Multi-city comparative analysis (Rotterdam, Utrecht, The Hague)

---

## 📚 References & Data Sources

### Primary Data Sources
- **Gemeente Amsterdam** (2024). Monitor Voedsel Amsterdam 2024: Meer Plantaardig. Municipality Research & Statistics (O&S).
- **RIVM** (2024). Database Milieubelasting Voedingsmiddelen [Environmental Impact of Foods Database]. Version September 2024.
- **RIVM** (2024). NEVO-online version 2023/8.0: Dutch Food Composition Database.
- **CBS** (2023). Kerncijfers Wijken en Buurten 2023 [Key Figures Districts and Neighborhoods]. Statistics Netherlands.
- **KBT** (2025). Amsterdam Neighborhood Demographics. Gemeente Amsterdam.

### Methodological Frameworks
- **Boyer, D., & Ramaswami, A.** (2020). Comparing urban food system characteristics and actions in US and Indian cities from a multi-environmental impact perspective. *Journal of Industrial Ecology*, 24(5), 1150-1162.
- **Muñoz-Arango, A. M., et al.** (2025). Methodology for estimating indirect emissions from Scope 3 applied in Valencia (Spain). *Journal of Cleaner Production*, 434, 139962.
- **Mohareb, E. A., et al.** (2018). Cities' role in mitigating United States food system greenhouse gas emissions. *Environmental Science & Technology*, 52(10), 5545-5554.

### Policy & Dietary Guidelines
- **Gezondheidsraad** (2023). A Healthy Protein Transition. Health Council of the Netherlands.
- **Willett, W., et al.** (2019). Food in the Anthropocene: The EAT-Lancet Commission on healthy diets from sustainable food systems. *The Lancet*, 393(10170), 447-492.
- **Voedingscentrum** (n.d.). Richtlijnen Schijf van Vijf [Wheel of Five Guidelines]. Netherlands Nutrition Centre.

### Climate Governance Literature
- **Acuto, M., & Leffel, B.** (2021). Understanding the global ecosystem of city networks. *Urban Studies*, 58(9), 1758-1774.
- **Gordon, D. J., & Johnson, C. A.** (2018). City-networks, global climate governance, and the road to 1.5°C. *Current Opinion in Environmental Sustainability*, 30, 35-41.
- **Kuramochi, T., et al.** (2020). Beyond national climate action: The impact of region, city, and business commitments on global greenhouse gas emissions. *Climate Policy*, 20(3), 275-291.
- **Seto, K. C., et al.** (2012). Urban land teleconnections and sustainability. *PNAS*, 109(20), 7687-7692.
- **Spiliotopoulou, M., & Roseland, M.** (2020). Urban Sustainability: From Theory Influences to Practical Agendas. *Sustainability*, 12(18), 7245.

### International Climate Policy
- **European Parliament & Council** (2021). Regulation (EU) 2021/1119: European Climate Law.
- **UNFCCC** (2025). The Paris Agreement. United Nations Climate Change.
- **UNEP** (2024). Emissions Gap Report 2024. United Nations Environment Programme.

### LCA & Environmental Impact
- **Poore, J., & Nemecek, T.** (2018). Reducing food's environmental impacts through producers and consumers. *Science*, 360(6392), 987-992.
- **Crippa, M., et al.** (2021). Food systems are responsible for a third of global anthropogenic GHG emissions. *Nature Food*, 2(3), 198-209.

### Cultural & Demographic Context
- **Galenkamp, H., et al.** (2025). Cohort Profile Update: The Healthy Life in an Urban Setting (HELIUS) Study. *International Journal of Epidemiology*, 54(3), dyaf071.
- **Stronks, K., et al.** (2013). Unravelling the impact of ethnicity on health in Europe: The HELIUS study. *BMC Public Health*, 13, 402.

---

## 🎓 Model Versions & Evolution

### **Master Hybrid Amsterdam Model v3.py** ⭐ CURRENT (January 2026)
**Best For:** Publication-ready analysis with comprehensive sensitivity analysis

**Key Features:**
- 30 publication-ready visualizations (core + appendix outputs)
- 64 CSV exports for full reproducibility
- 5-visualization sensitivity analysis suite
- APA-formatted tables (PNG + CSV)
- Paul Tol colorblind-safe palette
- 31 food items across 14 granular categories
- Fixed infrastructure approach (Scope 1+2 constant at 1,750 kton)
- Calibrated to Monitor 2024 within 0.06% error

**Outputs:**
- Charts 1-18: Full analytical suite (nexus, transitions, scopes, deltas)
- Charts 16a-16e: Comprehensive sensitivity analysis
- `data/results/`: 64 CSV files with complete data exports

**Runtime:** ~100-120 seconds

---

### **Master_hybrid_Amsterdam_Model-v2** (December 2025)
**Best For:** Strategic planning with distance-to-goals analysis

**Innovations:**
- Distance-to-Goals heatmap (reduction pathways)
- 9 diet scenarios including Mediterranean
- Separate mass vs. emissions visualization
- 16 core visualizations

**Key Addition:** Visual gap analysis showing % emission reduction needed for each baseline→goal transition

---

### **Master_hybrid_Amsterdam_Model.py** (November 2025)
**Best For:** Behavioral realism with education effects

**Key Innovation:**
- Dual-Factor Beta (Volume × Behavioral)
- Education modifier (0.85 for high-education, 1.10 for low-education)
- Empirical baseline from Monitor 2024 (48% plant/52% animal)
- Neighborhood hotspot analysis

**Counter-intuitive Finding:** Wealthy, educated areas show similar emissions to middle-income areas due to plant-based preferences offsetting higher consumption volumes.

---

### **MasterHybridModel.py** (October 2025)
**Best For:** High-level scenario comparison

**Components:**
- 6 dietary scenarios
- 16 foods × 3 metrics (CO2, land, water)
- 7 Amsterdam neighborhoods with income data
- 5 core visualizations

---

### **hybridMNodelAMS.py** (September 2025)
**Best For:** Foundational spatial analysis

**Focus:**
- Neighborhood-level emissions mapping
- Income-based scaling only (no education effects yet)
- Basic food categories

---

## 🚀 Installation & Usage

### Prerequisites
```bash
Python 3.8+
pandas
numpy
matplotlib
seaborn
```

### Setup
```bash
# Clone repository
git clone https://github.com/agaathm87/code-for-framework.git
cd code-for-framework

# Create virtual environment (recommended)
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install pandas numpy matplotlib seaborn
```

### Running the Analysis
```bash
# Run latest version (v3.1)
python "Master Hybrid Amsterdam Model v3.py"

# Alternative versions
python Master_hybrid_Amsterdam_Model-v2.py      # v2 with distance-to-goals
python Master_hybrid_Amsterdam_Model.py          # Original with education effects
python MasterHybridModel.py                      # Simplified 6-scenario version
```

### Expected Outputs
```
images/
├── core/                # 30 PNG visualizations (150-300 DPI)
├── appendix/            # Full 9-diet transparency
data/
├── results/             # 64 CSV files for reproducibility
```

---

## 🌟 Key Contributions to Urban Climate Science

### Theoretical Contributions

**1. Reconfigured GHG Scope Framework for Cities**
- Adapted corporate-oriented GHG Protocol for municipal food systems
- Demonstrated that territorial accounting (Scope 1+2) captures only 39% of food-related impact
- Established consumption-based accounting as prerequisite for net-zero credibility

**2. Operationalized "Urban Paradox" Concept**
- Quantified governance gap: cities expected to lead climate action while lacking Scope 3 visibility
- Identified "infrastructural lock-ins" (Waste-to-Energy dependencies) as structural barriers
- Mapped 221 feedback loops constraining municipal intervention capacity

**3. Dual-Driver Mechanism for Heterogeneity**
- Volume Beta (income): Economic purchasing power determines total consumption
- Plant Beta (education): Cultural capital shapes dietary composition
- Revealed "Volume vs. Composition Paradox": wealthy educated areas ≈ middle-income emissions

### Methodological Innovations

**4. Hybrid Modeling Framework**
- First integration of macro-LCA with micro-demographic spatial simulation for urban food
- Bridges Boyer & Ramaswami (2020) transboundary logic with Muñoz-Arango (2025) neighborhood granularity
- Enables "what, where, who" analysis: emissions × location × demographics

**5. Fixed Infrastructure Approach**
- Novel technique isolating behavioral (Scope 3) from operational (Scope 1+2) interventions
- Demonstrates that under current capacity, dietary shifts offer 10× higher leverage than efficiency gains
- Facilitates near-term policy design without requiring infrastructure transformation modeling

**6. Sensitivity Transparency**
- 5-visualization suite reveals diet adherence as critical uncertainty (±897 kton vs ±135 kton for waste)
- Cross-scenario analysis shows animal-heavy diets have 2× waste sensitivity
- Establishes behavioral compliance as primary determinant, not technical parameters

### Policy-Relevant Findings

**7. Quantified Socioeconomic Equity Constraints**
- 35% of minimum-income households face food poverty
- Without subsidies, achievable reduction drops from 25.3% to 15-18%
- Demonstrates that climate targets must integrate affordability interventions

**8. Validated Amsterdam's Progressive Status**
- City already at 48% plant protein (vs 43% national) due to demographic composition
- Yet 52% "stubborn core" of animal consumption drives 68% of emissions
- Confirms early municipal interventions are effective but insufficient alone

**9. Established Food as Central Climate Lever**
- Food represents ~30% of global emissions yet remains marginal in urban climate strategies
- Amsterdam Goal (70:30) offers -1,137 kton reduction—equivalent to removing 247,000 cars
- Highest-leverage intervention: dietary shift > waste reduction > local sourcing

### Contribution to "Global Ecosystem of City Networks"

**10. Scalable Methodology**
- Framework replicable for any metropolitan city with local calibration
- Addresses post-Paris governance gap (Gordon & Johnson, 2018)
- Operationalizes subnational potential projected at 3.8-5.5% global emission reduction (Kuramochi et al., 2020)

**11. Data Production Capability**
- Transforms cities from passive standard recipients to active data producers (Acuto & Leffel, 2021)
- 64 CSV exports enable municipal monitoring dashboards
- Bridges science-policy gap through transparent, auditable calculations

---

## 🔍 Understanding "The Urban Paradox"

### The Problem
Metropolitan cities face a structural contradiction:
1. **Expected Role**: Lead global climate mitigation (C40, Covenant of Mayors)
2. **Accounting Framework**: Territorial boundaries (Scope 1+2) designed for nation-states
3. **Actual Impact**: 61% of food emissions occur in transboundary supply chains (Scope 3)
4. **Governance Capacity**: Municipalities lack legal authority over international agriculture

### The Evidence
- Amsterdam's 105,000 hectare land footprint = 5.5× city surface area
- 85% of food sourced outside Netherlands
- 2,737 kton CO₂e in Scope 3 vs 1,750 kton in Scope 1+2
- Red meat (1,360 kton) > All local operations (1,750 kton)

### The Solution Pathway
**Shift 1**: From territorial reporting → consumption-based management  
**Shift 2**: From passive standards recipient → active data producer  
**Shift 3**: From sectoral silos → integrated food-climate-health strategies  
**Shift 4**: From efficiency focus → behavioral transformation priority  

**Primary Leverage Points** (ranked by impact):
1. **Dietary shift to 70:30** (-25.3%, -1,137 kton)
2. **Waste reduction** (-2.7%, immediate implementation)
3. **Supply chain optimization** (-5-8%, long-term)
4. **Local sourcing expansion** (-2-4%, capacity-limited)

---

## 📊 Sample Output

### Console Report Example
```
================================================================================
                    MASTER SCOPE 3 TONNAGE REPORT
================================================================================
CATEGORY              1.Monitor  2.Theory  3.Metro  4.Meta  5.DuGoal  6.AmGoal   7.EAT
Red Meat              118,200    142,000  185,600  250,000  85,000    35,000    42,500
Poultry                92,100    105,600  138,900  185,000  58,000    23,000    84,600
Dairy & Eggs          142,300    154,800  108,700   98,000 105,000    75,000    95,000
Fish                   55,800     37,200   38,500   92,000  38,500    38,500    72,100
Plant Protein          48,900     28,600   18,200   24,000  89,000   145,000    98,300
Staples                82,600     79,200   65,500   18,000  81,000    90,000    67,000
Veg & Fruit            35,400     31,000   25,500   46,000  52,000    82,000   110,000
Ultra-Processed        38,100     41,700   65,300   12,000  18,000     8,000        0
────────────────────────────────────────────────────────────────────────────────────
TOTAL (Tonnes)        613,500    620,100  646,300  725,000 526,600   496,600   569,500
Change vs Baseline        +0%      +1.1%   +5.3%   +18.2%  -14.2%    -19.1%     -7.1%
================================================================================

--- NEIGHBORHOOD HOTSPOT ANALYSIS (MONITOR ADJUSTED) ---
Neighborhood      Population  Meat_Mod   Volume_Beta  Total_CO2_Tonnes
Zuid              145,000      0.85        1.15         185,400
Centrum            87,000      0.85        1.10         111,200
Oost              135,000      0.90        1.05         172,500
West              145,000      1.10        0.95         194,300
Noord              99,000      1.10        0.90         126,800
Nieuw-West        160,000      1.10        0.92         204,500
Zuidoost           89,000      1.10        0.85         113,400
```

**Key Insights:**
**Amsterdam Scope 1+2 (food only):** 1,748,905 tonnes CO2e/year
  - Base consumption (88.1%): 1,540,886 tonnes — from 22 explicit food items
  - Food waste (9.7%): 169,497 tonnes — spoilage in supply chain
  - Retail/distribution (2.2%): 38,522 tonnes — cold chain operations
  - **Verification:** 0.06% error vs Monitor 2024 target of 1,750 kton ✓
- **Scope 3 (supply chain beyond retail):** 877,000–914,000 tonnes per diet
- **Total Scope 1+2+3:** 2,418,084–2,662,905 tonnes for different diets
- **Scope 1+2 represents 63.8%** of total (Monitor baseline); **Scope 3 is 36.2%**
- **Education effect:** South Amsterdam (70% educated) shows 15% lower meat consumption (0.85 modifier) vs low-education areas (1.10 modifier)
- **Highest-impact food:** Coffee (23.34 kgCO2e/kg), Beef (16.67), Alcohol (13.34)
- **Lowest-impact foods:** Vegetables, Fruits, Potatoes (1.33), Nuts (1.67)
- **Dutch Goal path:** -14.2% reduction (60:40 plant:animal)
- **Amsterdam Goal path:** -19.1% reduction (70:30 plant:animal) — most ambitious
- **EAT-Lancet path:** -7.1% reduction (80:20 plant:animal) with lower total consumption

---

## 🔍 Understanding the Model

### The Hybrid Approach: Three Dimensions

**1. Geographic/Economic (Valencia Downscaling)**
```
Beta_Volume = C1 × e^(C2 × income_ratio)
```
- Wealthier neighborhoods consume MORE total food
- Accounts for eating out, packaging waste, disposal
- Empirical: wealthy Amsterdam produces more food waste

**2. Behavioral (Education Effects) — Monitor Insight**
```
If High_Education_Pct > 0.5 (50% bachelor degree or higher):
    Meat_Modifier = 0.85     (eat 15% less meat)
    Plant_Modifier = 1.15    (eat 15% more plant foods)
Else:
    Meat_Modifier = 1.10     (eat 10% more meat)
    Plant_Modifier = 0.90    (eat 10% less plant foods)
```
- **Source:** Amsterdam Monitor 2024 survey data
- **Finding:** High-education areas (52% plant protein) vs low-education (39% plant protein)
- **Independence:** Education effect is INDEPENDENT of income — creates multiplicative behavioral pattern
- **Example:** 
  - Zuid (70% educated, high income): 0.85 meat × 1.15 volume = moderate meat total
  - Zuidoost (30% educated, low income): 1.10 meat × 0.85 volume = moderate meat total
- **Policy Implication:** Education-based interventions are as important as income-based policies

**3. Environmental (LCA)**
```
Total_Emissions = Consumption × Emission_Factor × Waste_Factor × Population × Time
```
- Multi-metric: CO2, land use, water footprint
- Includes supply chain (production through retail)
- Default waste factor: 1.15 (15% loss)

### The 7 Diet Scenarios

| # | Diet | Plant:Animal | Use Case |
|---|------|-------------|----------|
| 1 | Monitor 2024 | 48:52 | Empirical baseline |
| 2 | Theoretical | 44:56 | Pre-Monitor estimate |
| 3 | High-Risk | 26:74 | Western excess |
| 4 | Metabolic | 16:84 | Low-carb animal |
| 5 | Dutch Goal | 60:40 | National policy target |
| 6 | Amsterdam | 70:30 | Municipal target (2030) |
| 7 | EAT-Lancet | 80:20 | Planetary health |

---

## ⚙️ Customization

### Modify Parameters
Edit `HybridModelConfig()`:
```python
class HybridModelConfig:
    NATIONAL_AVG_INCOME = 32000      # €/year baseline
    SCALING_C1 = 0.8                 # Income elasticity intercept
    SCALING_C2 = 0.2                 # Income elasticity slope
    WASTE_FACTOR = 1.15              # Supply chain loss (15%)
    POPULATION_TOTAL = 882000        # Amsterdam population
```

### Add Custom Diet
Edit `load_diet_profiles()`:
```python
'Custom_Vegetarian': {
    'Beef': 0, 'Pork': 0, 'Chicken': 15, 'Fish': 10,
    'Cheese': 50, 'Milk': 300, 'Eggs': 35,
    'Pulses': 100, 'Nuts': 40, 'Meat_Subs': 60,
    'Grains': 250, 'Vegetables': 220, 'Fruits': 200, 'Potatoes': 100,
    'Sugar': 30, 'Processed': 50
}
```
(All values in grams/day)

### Update Emission Factors
Edit `load_impact_factors()`:
```python
'Beef': {'co2': 28.0, 'land': 25.0, 'water': 15400},  # kg CO2, m², L
```

### Add Neighborhoods
Edit `load_neighborhood_data()` with CBS statistics (education % is critical for behavioral effects):
```python
'Neighborhood': ['Centrum', 'Zuid', 'West', 'Noord', 'Zuidoost', 'Nieuw-West', 'Oost'],
'Population': [87000, 145000, 145000, 99000, 89000, 160000, 135000],
'Avg_Income': [48000, 56000, 34000, 29000, 24000, 26000, 36000],  # EUR/year
'High_Education_Pct': [0.65, 0.70, 0.60, 0.40, 0.30, 0.35, 0.55]   # Bachelor+ fraction
```
**Note:** High_Education_Pct drives behavioral modifiers (meat vs plant preference), not just income scaling!

---

## 🔬 Transparent Scope 1+2 System

### The Problem: Why Initial Estimates Were So Wrong

The original model's Scope 1+2 factors (0.05–0.5 kgCO2e/kg) only covered **on-farm production**. This produced just 35.7 kton for Amsterdam—but the Monitor 2024 showed 1,750 kton. The missing **49x gap** was the entire food system beyond the farm:

- **On-farm production** (5–10% of total)
- **Processing & packaging** (10–15%)
- **Transportation & retail** (15–25%)
- **Food waste** (10–15%)
- **Cold chain & distribution** (5–10%)

**Solution:** Transparent, component-based Scope 1+2 calculation that shows exactly where emissions come from.

### Complete Scope 1+2 Breakdown (Verified)

For **Amsterdam Monitor 2024 baseline (882,000 people):**

```
Base food consumption:  1,540,886 tonnes CO2e/year  (88.1%)
  ├─ On-farm production
  ├─ Processing
  ├─ Primary transportation
  └─ Retail operations

Food waste (11%):         169,497 tonnes CO2e/year  (9.7%)
  └─ 11% of base (spoilage in supply chain & retail)

Retail/distribution (2.5%): 38,522 tonnes CO2e/year  (2.2%)
  └─ Cold chain & last-mile delivery

────────────────────────────────────────────────────
TOTAL Scope 1+2:       1,748,905 tonnes CO2e/year  (100%)
────────────────────────────────────────────────────
Monitor 2024 Target:   1,750,000 tonnes CO2e/year
Error:                  -0.06%  ✓ VERIFIED
```

### Calibrated Emission Factors (All 22 Foods)

**Scope 1+2 Factors — kgCO2e per kg consumed (includes all pre-consumer stages):**

| Category | Food | Factor | Notes |
|----------|------|--------|-------|
| **Proteins** | Beef | 16.67 | Highest impact; land use + methane |
| | Pork | 13.34 | Grain feed + processing |
| | Chicken | 10.00 | More efficient than red meat |
| | Fish | 12.00 | Fishing + cold chain |
| | Eggs | 5.34 | Lower than meat |
| | Pulses | 2.67 | Legume production + processing |
| | Nuts | 1.67 | Tree crops; water-intensive |
| | Meat_Subs | 8.00 | Plant-based alternatives |
| **Dairy** | Cheese | 6.67 | High processing impact |
| | Milk | 3.33 | Dairy processing & cooling |
| **Staples** | Grains | 1.67 | Crop production + milling |
| | Potatoes | 1.33 | Field crops; low processing |
| **Fresh** | Vegetables | 1.33 | Field production + retail |
| | Fruits | 1.33 | Orchard/field + retail |
| **Processed** | Sugar | 2.67 | Refining energy-intensive |
| | Processed | 6.67 | Ultra-processed foods |
| **Beverages** | Coffee | 23.34 | **Highest of all** — tropical crop, roasting, transport |
| | Tea | 8.00 | Drying & processing intensive |
| | Alcohol | 13.34 | Fermentation + distillation |
| **Additions** | Oils | 5.34 | Extraction & refining |
| | Snacks | 10.00 | Ultra-processed comparable |
| | Condiments | 4.00 | Spices + processing |

**Key Observations:**
- **Coffee dominates beverages** (23.34) due to tropical production, roasting, and long supply chain
- **Beef dominates proteins** (16.67) due to methane + land use
- **Plant foods lowest** (1.33–2.67) except processed forms
- **Range: 1.33–23.34** kgCO2e/kg — 17× variation across food types
- All factors **calibrated against Monitor 2024** to match 1,750 kton target

### Why Waste & Retail Are Explicit (Not Hidden)

**Previous approach (problematic):**
- Added opaque 1.241× multiplier to factors
- Users didn't know where emissions came from
- Impossible to model interventions separately

**Current approach (transparent):**
```python
# Base consumption × 22 foods × 365 days × population
base_co2 = 1,540,886 tonnes

# Food waste: 11% of base (spoilage in supply chain)
waste_co2 = base_co2 × 0.11 = 169,497 tonnes

# Retail/distribution: 2.5% of base (cold chain)
retail_co2 = base_co2 × 0.025 = 38,522 tonnes

# Total Scope 1+2
total = base_co2 + waste_co2 + retail_co2 = 1,748,905 tonnes
```

**Policy advantages:**
- **Separate interventions:** "Reduce food waste" vs "improve cold chain"
- **Technology tracking:** Monitor progress on waste reduction independently
- **Communication:** "88% from what we eat, 10% wasted, 2% in distribution"
- **Calibration:** Validate each component against Monitor data

### Verification: How We Matched 1,750 kton Target

**Step 1:** Applied initial Scope 1+2 factors (from literature)
- Result: 2,624 kton (49.9% overshoot)

**Step 2:** Calculated reduction factor
```python
target = 1,750 kton (Monitor data)
overshoot = 2,624 / 1,750 = 1.499
reduction_factor = 1 / 1.499 = 0.6669
```

**Step 3:** Applied uniformly across all 22 foods
- All factors × 0.6669 (≈33% reduction)
- Maintains relative ratios (Beef stays ~2× Pork)
- Preserves behavioral realism

**Step 4:** Added waste & retail
- Accounts for supply chain losses already in Monitor target
- Explains the full 1,750 kton breakdown transparently

**Step 5:** Cross-validation
```python
Created final_verification.py
Ran with all 9 diets + all 22 foods
Result: 1,748,905 tonnes for Monitor 2024
Error: -0.06%  ✓ SUCCESS
```

### Scope 1+2 vs Scope 3: What's Included?

**Scope 1+2 (11–14% of total):**
- On-farm production (heating, machinery, diesel)
- Direct methane emissions (livestock)
- Processing & packaging
- Transportation to retail
- Retail operations (electricity, refrigeration)
- Supply chain losses (food waste in transit)

**Scope 3 (86–89% of total):**
- Land use change (deforestation)
- Biogenic emissions (crop production)
- Manufacturing supply chain
- International transport
- Consumer cooking (in some frameworks)
- End-of-life disposal

**Why this split matters:**
- Scope 1+2 interventions: **efficiency, waste reduction, cold chain**
- Scope 3 interventions: **dietary shift, land use efficiency, transport**
- In Amsterdam: **Scope 3 dominates** (96–97%) → **diet change > local efficiency**

### Implementation Notes (For Developers)

**Updated in all v2+ models:**
- Lines 88–129 (v3): `load_impact_factors()` — all 22 foods with calibrated factors
- Lines 469–520 (v2): Waste/retail calculation logic
- Lines 600–630 (v2): Console output showing transparent breakdown
- Lines 730–738 (v3): `FOOD_TYPE_MAP` extended to 10 categories
- Lines 792–797 (v3): `PROTEIN_CONTENT` mappings for new foods

**Testing:**
```bash
python "Master Hybrid Amsterdam Model v3.py"
# Check console output for:
# "Base food consumption: 1,540,886 tonnes (88.1%)"
# "+ Food waste (11%): 169,497 tonnes (9.7%)"
# "+ Retail/distribution (2.5%): 38,522 tonnes (2.2%)"
# "Total: 1,748,905 tonnes"
```

---

## 📚 Data Sources

**Consumption:**
- Amsterdam Monitor 2024 — Actual consumption patterns
- RIVM DNFCS 2019-2021 — National dietary survey
- CBS Kerncijfers Wijken — Neighborhood statistics

**Emission Factors:**
- Boyer et al. — LCA methodology
- Blonk Consultants — Food product LCA database
- Poore & Nemecek (2018) — Land footprint analysis
- WaterFootprint Network — Water consumption data

**Behavioral & Demographic:**
- CBS Statline — Official statistics
- Amsterdam Monitor 2024 — Local survey data

**Validation:**
- Monitor baseline = actual consumption (not extrapolated)
- Income elasticity calibrated to Dutch research
- Education modifiers from Monitor survey itself
- Cross-validated with EAT-Lancet & Dutch guidelines

---

## 🎓 References

- **Valencia Downscaling** — Income-based shadow inventory adjustment
- **Boyer et al.** — Food systems LCA framework
- **Blonk Consultants** — Industry-standard emission factors
- **EAT-Lancet Commission (2019)** — Planetary boundaries & health optimization
- **Poore & Nemecek (2018)** — Global agricultural impact meta-analysis
- **Amsterdam Monitor 2024** — Municipal consumption survey
- **CBS (Statistics Netherlands)** — Official demographic data

---

## 💡 Strengths & Limitations

**Strengths:**
- ✅ Empirical baseline (actual Amsterdam consumption)
- ✅ Multi-metric assessment (CO2, land, water) shows trade-offs
- ✅ Education effects capture real behavioral heterogeneity
- ✅ Neighborhood-level analysis enables targeted interventions
- ✅ Composite beta factors reflect multiplicative effects

**Limitations & Future Work:**
- ⚠️ Assumes stable consumption patterns
- ⚠️ Waste factor is global average (not household-specific)
- ⚠️ No upstream supply chain innovation modeling
- ⚠️ Education as proxy for preference (not causal)
- ⚠️ No nutritional adequacy assessment

**Recommended Extensions:**
1. Integrate real CBS/Monitor databases
2. Model dietary transition trajectories
3. Include household waste measurement
4. Add price elasticity effects
5. Extend to supply-chain interventions
6. Add health impact assessment (HIA)

---

## 📁 Project Structure

```
code-for-framework/
├── hybridMNodelAMS.py                    # Foundational
├── MasterHybridModel.py                  # Enhanced (6 diets)
├── Master_hybrid_Amsterdam_Model.py      # Advanced (Monitor 2024)
├── Master_hybrid_Amsterdam_Model-v2      # Comprehensive (7 diets + heatmap)
├── Master Hybrid Amsterdam Model v3.py   # ⭐ Latest (7 diets + table)
└── README.md                             # Documentation

Output files:
├── 1_Nexus_Analysis.png
├── 2a_Transition_DutchGoal.png
├── 2b_Transition_AmsterdamGoal.png
├── 2c_Transition_EAT_Lancet.png
├── 3_All_Diets_Plates.png
├── 4_Impact_Stack.png
├── 5_Neighborhood_Hotspots.png
└── 6_Table_Tonnage.png                   # v3 only
```

### Transitions Index
- MasterHybridModel.py: [2a_Transition_DutchGoal.png](2a_Transition_DutchGoal.png), [2b_Transition_AmsterdamGoal.png](2b_Transition_AmsterdamGoal.png), [2c_Transition_EAT_Lancet.png](2c_Transition_EAT_Lancet.png), [2d_Transition_Schijf.png](2d_Transition_Schijf.png), [2e_Transition_Mediterranean.png](2e_Transition_Mediterranean.png)
- Master_hybrid_Amsterdam_Model.py: [2a_Transition_DutchGoal.png](2a_Transition_DutchGoal.png), [2b_Transition_AmsterdamGoal.png](2b_Transition_AmsterdamGoal.png), [2c_Transition_EAT_Lancet.png](2c_Transition_EAT_Lancet.png), [2d_Transition_Schijf.png](2d_Transition_Schijf.png), [2e_Transition_Mediterranean.png](2e_Transition_Mediterranean.png)
- Master Hybrid Amsterdam Model v3.py: [5a_Transition_Dutch.png](5a_Transition_Dutch.png), [5b_Transition_Amsterdam.png](5b_Transition_Amsterdam.png), [5c_Transition_EAT.png](5c_Transition_EAT.png), [5d_Transition_Schijf.png](5d_Transition_Schijf.png), [5e_Transition_Mediterranean.png](5e_Transition_Mediterranean.png)

### Scope Analysis Outputs (v3 & Advanced Models)
- [6_Scope12_vs_Scope3.png](6_Scope12_vs_Scope3.png): **Grouped bars** comparing Scope 1+2, Scope 3, and Total (1+2+3) emissions per diet
  - Shows that Scope 1+2 = 4–6% of total, Scope 3 = 94–97% (supply chain dominates)
  - Key insight: Local production changes have minimal impact; food choice (meat vs plant) is what matters
- [7_Scope_Shares.png](7_Scope_Shares.png): **Stacked % bars** showing Scope 1+2 and Scope 3 proportions
  - Reveals consistency across all diets: Scope 3 is 94–97% regardless of plant:animal ratio
  - Implication: Reducing meat is about supply chain (shipping, processing, land) not local production
- [8_All_Total_Emissions_Donuts.png](8_All_Total_Emissions_Donuts.png): **3×3 grid** of donut charts (one per diet)
  - Each donut shows S1+2+3 breakdown by food category (16 items)
  - Center text displays total emissions in thousands of tonnes
  - Reveals which food categories drive emissions in each scenario

---

## 🤝 Contributing

**Model Improvements:**
- Integrate real CBS/Monitor databases
- Validate education effects with primary data
- Add temporal dynamics & projections
- Model price elasticity

**Scenario Expansion:**
- Policy interventions (carbon tax, subsidies, labeling)
- Supply-side innovations (alternative proteins, local sourcing)
- Population & demographic changes
- Climate adaptation scenarios

**Visualization:**
- Interactive dashboards (Plotly/Dash)
- Sensitivity analysis (Monte Carlo)
- City comparisons
- Health co-benefits analysis

---

## 📞 Contact & Collaboration

**For Academic Inquiries:**
- Research methodology questions
- Model replication for other cities
- Collaboration opportunities

**For Policy Applications:**
- Municipal climate strategy integration
- Stakeholder workshop facilitation
- Custom scenario development

**Repository:** [github.com/agaathm87/code-for-framework](https://github.com/agaathm87/code-for-framework)

**Project:** UvA Complex Systems for Policy — Challenge-Based Project  
**Last Updated:** January 30, 2026  
**Python:** 3.8+  

For questions or contributions, please submit a pull request.

---

## ✅ Project Status

**Current Status:** ✅ **COMPLETED & PUBLISHED**  
**Submission Date:** January 30, 2026  
**Final Report:** 14,165 words (excluding citations, tables, appendices)

**Deliverables:**
- ✅ Final academic report (PDF)
- ✅ Policy brief for Gemeente Amsterdam
- ✅ 30 publication-ready visualizations
- ✅ 64 CSV data exports
- ✅ Presentation slides
- ✅ Comprehensive documentation

**Model Validation:**
- ✅ Calibrated to Monitor 2024 baseline (0.06% error)
- ✅ Cross-validated with EAT-Lancet and Dutch guidelines
- ✅ Peer-reviewed through academic supervision
- ✅ Stakeholder feedback integrated (Gemeente Amsterdam)

**Future Development** (Post-Project):
- [ ] Dynamic infrastructure modeling (variable Scope 1+2)
- [ ] Integration with real-time municipal dashboards
- [ ] Multi-city comparative analysis (Rotterdam, Utrecht, The Hague)
- [ ] Cost-benefit analysis module
- [ ] Interactive web application (Streamlit/Plotly)
- [ ] Temporal projections to 2030/2050

---

## 🙏 Acknowledgments

**Project Partner:**
- Gemeente Amsterdam, Department of Sustainability — for data access and policy context

**Academic Supervision:**
- UvA Complex Systems for Policy program faculty

**Data Providers:**
- RIVM (National Institute for Public Health)
- CBS (Statistics Netherlands)
- Amsterdam Research & Statistics (O&S)

**Methodological Foundations:**
- Boyer & Ramaswami (transboundary LCA framework)
- Muñoz-Arango et al. (spatial microsimulation)
- EAT-Lancet Commission (planetary health boundaries)

**Open-Source Community:**
- Python scientific computing ecosystem (NumPy, pandas, Matplotlib, Seaborn)
- Paul Tol (colorblind-safe visualization palettes)

---

*"Effective climate action hinges on addressing Scope 3 emissions. This research bridges the governance gap between territorial accounting and consumption-based reality, providing metropolitan cities with the data production capability needed to move from passive targets to active climate leadership."*

**— Research Team, January 2026**

---

*This model integrates life cycle assessment research, behavioral science, and food systems analysis to provide policymakers with science-based tools for dietary transition planning in Amsterdam.*
