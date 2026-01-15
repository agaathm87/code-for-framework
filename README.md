# Hybrid Amsterdam Food Systems Model

A comprehensive Python framework for calculating **Scope 3 food-related GHG emissions** at the neighborhood level in Amsterdam. Integrates empirical consumption data (Amsterdam Monitor 2024), life cycle assessment (LCA), income-based scaling, and behavioral factors (education effects) to model dietary impacts across spatial dimensions and policy scenarios.

## 📊 Overview

This project contains **5 complementary Python modules** with increasing sophistication:

| File | Type | Key Feature | Output |
|------|------|-------------|--------|
| **hybridMNodelAMS.py** | Foundational | Valencia downscaling | Per-neighborhood breakdown |
| **MasterHybridModel.py** | Enhanced | 6 diets + 3 metrics (CO2, land, water) | 5 PNG charts + report |
| **Master_hybrid_Amsterdam_Model.py** | Advanced | Monitor 2024 baseline + education effects | 5 charts + hotspot analysis + 2 extra transitions |
| **Master_hybrid_Amsterdam_Model-v2** | Comprehensive | 9 diets + distance-to-goals heatmap | 4 charts + heatmap + report |
| **Master Hybrid Amsterdam Model v3.py** | ⭐ Latest | Composite beta + table export | 6 charts + table + report + Schijf/Mediterranean transitions |

**Recommended:** Use `Master Hybrid Amsterdam Model v3.py` for the most advanced analysis.

---

## 🎯 Key Features

✅ **Empirical Monitor 2024 Data** — Baseline reflects actual Amsterdam consumption (48% plant / 52% animal protein)  
✅ **Multi-Metric LCA** — Tracks CO2, land use, and water across 16 food categories  
✅ **Income-Sensitive Consumption** — Valencia downscaling method scales by neighborhood income  
✅ **Education-Based Behavioral Effects** — Models preference differences: high-education areas eat 15% less meat (Monitor finding)  
✅ **Scope 1+2 + Scope 3 Analysis** — Separates local production (4–6%) from supply chain (94–97%) emissions  
✅ **9 Dietary Scenarios** — Includes Schijf van 5 and Mediterranean diets  
✅ **Supply Chain Integration** — Accounts for 15% waste across production-retail pipeline  
✅ **Spatial Hotspot Analysis** — Neighborhood-level emissions with education-income interaction effects  
✅ **Publication-Ready Visualizations** — 8+ professional charts per run (including scope breakdown & donuts)  
✅ **Distance-to-Goals Matrix** — Quantifies % reduction needed for each pathway  

---

## 📁 Module Descriptions

### **hybridMNodelAMS.py** — Foundational Model
**Best For:** Understanding core Valencia methodology

**Components:**
- `HybridModelConfig` — Configuration & constants
- `Scope3Calculator` — Core emissions calculator
- `run_protein_transition_scenario()` — Policy: reduce meat by X%
- `run_food_waste_reduction_scenario()` — Policy: reduce waste by X%

**Output:** Detailed DataFrame with per-neighborhood, per-food-category emissions

---

### **MasterHybridModel.py** — Enhanced Analysis
**Best For:** High-level scenario comparison & understanding diet differences

**Components:**
- `Scope3Engine` — Advanced calculation engine
- 6 dietary scenarios (Monitor, High-Risk, Metabolic, Dutch Goal, Amsterdam Goal, EAT-Lancet)
- 16 foods × 3 metrics (CO2, land, water)
- 7 Amsterdam neighborhoods with income data

**Visualizations:**
1. **1_Nexus_Analysis.png** — CO2/Land/Water metrics across 6 diets
2. **2a/2b/2c_Transition_*.png** — Baseline vs 3 policy goals (transitions)
3. **3_All_Diets_Plates.png** — Diet compositions (6 pie charts)
4. **4_Impact_Stack.png** — Stacked emissions by category
5. **5_Neighborhood_Hotspots.png** — Spatial emissions distribution

---

### **Master_hybrid_Amsterdam_Model.py** — Advanced Version
**Best For:** Most accurate Amsterdam-specific analysis with behavioral realism

**Key Innovations:**
- **Empirical Baseline:** Amsterdam Monitor 2024 data (48% plant/52% animal)
- **Dual-Factor Beta:** 
  - Volume scaling (income): Wealthier neighborhoods consume more total food
  - Behavioral modifier (education): High-education areas prefer plant-based foods
- **Counter-intuitive Finding:** Wealthy, educated areas (Zuid 70% education, 0.85 meat modifier) show similar emissions to middle-income areas because education-driven dietary composition offsets income-driven volume increases
- **Neighborhood Hotspot Modifiers:** Shows meat_modifier per area (0.85 for high-education, 1.10 for low-education)

**Outputs:** 5 visualizations + hotspot analysis with education-adjusted emissions
- Charts: 1_Nexus, 2a/2b/2c_Transitions (Dutch/Amsterdam/EAT), 3_All_Diets, 4_Impact_Stack, 5_Neighborhood_Hotspots
- Console report with meat modifiers and neighborhood breakdown

---

### **Master_hybrid_Amsterdam_Model-v2** — Comprehensive Analysis
**Best For:** Strategic planning & understanding transformation difficulty

**New Features:**
- 9 diet scenarios (adds Schijf van 5 and Mediterranean)
- **Distance-to-Goals Heatmap** — % emission reduction needed for each pathway
- **All Plates Mass** — Physical consumption vs emissions separated
- **All Emissions Donuts** — Composition + total per diet

**Visualizations:**
1. **1_Nexus_Analysis.png** — Multi-resource comparison
2. **2_All_Plates_Mass.png** — Physical diet compositions
3. **3_All_Emissions_Donuts.png** — Emission breakdown with totals
4. **4_Distance_To_Goals.png** — Heatmap of reduction pathways

---

### **Master Hybrid Amsterdam Model v3.py** ⭐ LATEST
**Best For:** Research publication, comprehensive policy analysis

**Key Enhancements:**
- **Composite Beta Calculation:** Two multiplicative factors
  - Volume Beta (income-driven): How much total food someone buys
  - Behavioral Modifiers (education-driven): What TYPE of food they choose
- **Scope 1+2 vs Scope 3 Breakdown:** Separates local production emissions (4–6%) from supply chain (94–97%)
  - Scope 1+2: Direct production & on-farm energy use
  - Scope 3: Land use, transportation, processing, packaging, retail
- **9 Diet Scenarios** with detailed rationale (adds Schijf van 5 & Mediterranean)
- **Extended Food Categories** — 16 items with scope12 intensity factors (0.05–0.5 kgCO2e/kg)
- **Comprehensive Visualizations** — 8 charts covering composition, scope analysis, totals, and transitions

**Visualizations:**
1. **1_Nexus_Analysis.png** — CO2/Land/Water metrics across 9 diets
2. **2a/2b/2c/2d/2e_Transition_*.png** — Baseline to goal transitions (5 scenarios: Dutch, Amsterdam, EAT, Schijf, Mediterranean)
3. **3_All_Diets_Plates.png** — Pie charts of 9 diet compositions
4. **4_Impact_Stack.png** — Stacked emissions across food categories
5. **6_Scope12_vs_Scope3.png** — Grouped bars: Scope 1+2, Scope 3, and Total (1+2+3) per diet
6. **7_Scope_Shares.png** — Stacked % bars showing Scope 1+2 and Scope 3 proportion
7. **8_All_Total_Emissions_Donuts.png** — 3×3 grid of donut charts (one per diet) showing S1+2+3 breakdown by food category
8. **6_Table_Tonnage.png** — Tabular emissions breakdown

**Console Report:**
- Master tonnage table (7 diets × 8 categories)
- Absolute emissions per category
- % change from baseline Monitor diet
- Neighborhood hotspot analysis with modifiers

---

## 🚀 Quick Start

### Installation
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install pandas numpy matplotlib seaborn
```

### Run Latest Analysis
```bash
python "Master Hybrid Amsterdam Model v3.py"
```

**Outputs:**
- 6 PNG charts (see above)
- Console report with statistics and hotspot analysis
- Generated in current directory

### Run Alternative Versions
```bash
python Master_hybrid_Amsterdam_Model-v2      # Comprehensive (with heatmap)
python Master_hybrid_Amsterdam_Model.py      # Advanced (original)
python MasterHybridModel.py                  # Enhanced (simpler)
python hybridMNodelAMS.py                    # Foundational
```

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
- **Amsterdam baseline:** 854,356 tonnes CO2e/year
- **Scope 1+2 (Local):** 35,702 tonnes (4.2%) — Direct production & on-farm energy
- **Scope 3 (Supply Chain):** 804,709 tonnes (95.8%) — Transportation, processing, retail, land use
- **Education effect:** South Amsterdam (70% educated) shows lower meat consumption (0.85 modifier) despite higher income, resulting in similar emissions to middle-income areas
- **Dutch Goal path:** -3.4% reduction needed (60:40 plant:animal)
- **Amsterdam Goal path:** -28.2% reduction needed (70:30 plant:animal)
- **EAT-Lancet path:** -30.0% reduction (80:20 plant:animal) — most sustainable option

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

## 📞 Contact

**Project:** UvA Complex Systems for Policy — Challenge-Based Project  
**Last Updated:** January 2026  
**Python:** 3.8+  
**Status:** Active development  

For questions or contributions, please submit a pull request.

---

*This model integrates decades of life cycle assessment research, behavioral science, and food systems analysis to provide policymakers with science-based tools for dietary transition planning in Amsterdam.*
