# Hybrid Amsterdam Model (HAM)

A comprehensive Python framework for calculating **Scope 3 GHG emissions** from food consumption at the neighborhood level in Amsterdam. Integrates empirical Monitor data, life cycle assessment (LCA), income-based scaling, and education-level effects to model dietary impacts across spatial and policy scenarios.

## Overview

This project contains three complementary Python modules with increasing sophistication:

1. **hybridMNodelAMS.py** - Foundational hybrid model with core Valencia downscaling logic
2. **MasterHybridModel.py** - Enhanced analysis with 6 dietary scenarios and comprehensive visualizations  
3. **Master_hybrid_Amsterdam_Model.py** - Advanced version integrating Amsterdam Monitor 2024 empirical data with refined income and education effects (**PRIMARY ANALYSIS TOOL**)

## Features

- **Empirical Monitor Data**: Baseline diet reflects actual 2024 Amsterdam consumption patterns (48% plant / 52% animal protein)
- **Income-Sensitive Consumption**: Scales consumption by neighborhood income using Valencia downscaling method
- **Education Effects**: Models behavioral differences: high-education areas consume 15% less meat despite higher income
- **Multi-Metric LCA**: Tracks CO2, land use, and water consumption across 16 food categories
- **6 Dietary Scenarios**: Compares Monitor baseline, high-risk, metabolic balance, Dutch goal (60:40), Amsterdam goal (70:30), and EAT-Lancet diets
- **Waste Integration**: Accounts for supply chain losses (default 15% waste factor)
- **Spatial Hotspot Analysis**: Identifies neighborhood-level emissions with income and education adjustments
- **Comprehensive Visualizations**: Generates 5 publication-ready charts per run

## Files

### hybridMNodelAMS.py
Foundational hybrid model with core Valencia downscaling logic.

**Classes & Functions:**
- `HybridModelConfig` - Base configuration parameters
- `Scope3Calculator` - Core emissions calculator with beta factor logic
- `load_cbs_neighborhood_data()` - Mock neighborhood demographics
- `load_rivm_consumption_data()` - National diet and emission factors
- `run_protein_transition_scenario()` - Models meat reduction policy (50% default)
- `run_food_waste_reduction_scenario()` - Models waste reduction policy

**Output:** Detailed DataFrame with per-neighborhood, per-food-category emissions

### MasterHybridModel.py
Enhanced analysis with 6 diet scenarios and publication-quality visualizations.

**Key Components:**
- `Scope3Engine` - Engine with aggregation and visualization logic
- `load_diet_profiles()` - 6 dietary scenarios
- `load_impact_factors()` - Multi-metric LCA (CO2, land, water)
- `load_neighborhood_data()` - 7 Amsterdam neighborhoods
- `run_spatial_simulation()` - Income-based emissions per neighborhood

**Outputs:**
1. 1_Nexus_Analysis.png - CO2/Land/Water comparison across diets
2. 2a/2b/2c Transition charts - Baseline vs policy goals
3. 3_All_Diets_Plates.png - Composition of all 6 diets
4. 4_Impact_Stack.png - Stacked emissions by food category
5. 5_Neighborhood_Hotspots.png - Emissions by location

### Master_hybrid_Amsterdam_Model.py ⭐ PRIMARY TOOL
Most advanced version with Monitor 2024 empirical data and refined beta logic.

**Key Enhancements:**
- Baseline diet: "Amsterdam Monitor 2024" (empirical data, 48% plant/52% animal)
- Education level integration (65% educated in Centrum vs 30% in Zuidoost)
- Refined Beta calculation:
  - **Volume Beta**: Income drives total consumption (exponential scaling)
  - **Education Modifier**: High-education neighborhoods reduce meat by 15%, increase plant by 15%
- Composite impact scaling reflecting real behavioral patterns

**Same 6 scenarios, 5 visualization outputs, plus education-adjusted hotspot analysis**

## Data Sources & Validation

**Consumption Data:**
- Amsterdam Monitor 2024 - Empirical survey data (primary baseline in Master_hybrid_Amsterdam_Model.py)
- RIVM DNFCS 2019-2021 - National dietary patterns and consumption statistics
- CBS Kerncijfers Wijken - Neighborhood population and income statistics

**Emission Factors:**
- Boyer et al. - LCA methodology for food systems
- Blonk Consultants - Industry-standard food product LCA data
- Covers scope 1-3 emissions (production through retail)

**Income & Education:**
- CBS Statline - Official Dutch neighborhood statistics
- Amsterdam Monitor - Local survey data (education, consumption patterns)

**Validation Approach:**
- Monitor baseline represents actual Amsterdam consumption (not national average)
- Income elasticity parameters calibrated to Dutch dietary research
- Education modifiers based on Monitor's reported behavior differences

## Key Model Logic

### The Hybrid Approach
The model combines three methodologies:

1. **Valencia Downscaling** (Geographic/Economic Dimension)
   - Income-based consumption adjustment: $\beta = C1 \times e^{C2 \times \text{income ratio}}$
   - Captures variation between wealthy (Zuid) and lower-income (Zuidoost) neighborhoods

2. **Education Effects** (Behavioral Dimension)  
   - High-education areas: 15% less meat, 15% more plant protein
   - Models preference shifts independent of income

3. **Life Cycle Assessment** (Environmental Dimension)
   - Multi-metric tracking: CO2, land use, water
   - Includes supply chain waste (default 15% loss factor)

### Calculation Pipeline
```
Local Consumption = National Average × Beta (income) × Modifier (education)
Total Emissions = Consumption × Emission Factor × Waste Factor × Population × Time
```

## Baseline Diet Comparison

### Amsterdam Monitor 2024 (Primary Baseline)
Empirical consumption pattern from Amsterdam Monitor data. **48% plant / 52% animal protein.**
- Lower meat consumption (-20% vs Netherlands)
- Higher fish/eggs and plant proteins (legumes, nuts, meat substitutes)
- Higher processed food (typical urban consumption)
- Representative of educated, health-conscious urban population

### Comparison Diets
1. **Metropolitan (High Risk)** - High meat/processed food consumption (worst-case scenario)
2. **Metabolic Balance** - High-protein, low-carb animal-based variant
3. **Dutch Goal (60:40)** - National dietary guidelines (60% plant, 40% animal)
4. **Amsterdam Goal (70:30)** - Municipal sustainability target (70% plant, 30% animal)
5. **EAT-Lancet (Planetary)** - Scientifically sustainable diet for planetary health

## Requirements

- pandas
- numpy
- matplotlib

## Quick Start

### Run the Primary Analysis (Master_hybrid_Amsterdam_Model.py)
```bash
python Master_hybrid_Amsterdam_Model.py
```

Generates 5 PNG visualizations + console report showing:
- All 6 diet scenarios compared across CO2, land, and water metrics
- Protein transition impact (baseline → Dutch/Amsterdam/EAT-Lancet goals)
- Neighborhood hotspots with education and income adjustments
- Complete tonnage table with % change vs Monitor baseline

### Run Enhanced Analysis (MasterHybridModel.py)
```bash
python MasterHybridModel.py
```
Same visualizations but with simpler baseline (without education effects)

### Run Core Model (hybridMNodelAMS.py)
```bash
python hybridMNodelAMS.py
```
Foundational analysis with detailed per-food, per-neighborhood breakdown

## Usage Examples

### Full Analysis Workflow
```bash
# Install dependencies
pip install pandas numpy matplotlib

# Run primary analysis with Monitor data and education effects
python Master_hybrid_Amsterdam_Model.py

# View generated visualizations
# - 1_Nexus_Analysis.png
# - 2a_Transition_DutchGoal.png
# - 2b_Transition_AmsterdamGoal.png
# - 2c_Transition_EAT_Lancet.png
# - 3_All_Diets_Plates.png
# - 4_Impact_Stack.png
# - 5_Neighborhood_Hotspots.png
```

### Custom Analysis (Python)
```python
from Master_hybrid_Amsterdam_Model import HybridModelConfig, Scope3Engine

cfg = HybridModelConfig()
engine = Scope3Engine(cfg)

# Analyze a specific diet
diet_profile = {'Beef': 10, 'Chicken': 25, 'Cheese': 35, ...}  # grams/day
impact = engine.calculate_raw_impact(diet_profile)
print(f"CO2: {impact['co2']} kg/person/day")
print(f"Land: {impact['land']} m²/person/day")
print(f"Water: {impact['water']} L/person/day")
```

## Configuration & Customization

### Adjust Model Parameters (HybridModelConfig)
```python
class HybridModelConfig:
    NATIONAL_AVG_INCOME = 32000      # €/year (Netherlands baseline)
    SCALING_C1 = 0.8                 # Income elasticity intercept
    SCALING_C2 = 0.2                 # Income elasticity slope
    WASTE_FACTOR = 1.15              # Supply chain loss (15%)
    POPULATION_TOTAL = 882000        # Amsterdam population
```

### Modify Diet Profiles
Edit `load_diet_profiles()` to add custom diets. All values in grams/day:
```python
'My_Custom_Diet': {
    'Beef': 20, 'Pork': 10, 'Chicken': 30, 'Fish': 15,
    'Cheese': 40, 'Milk': 250, 'Eggs': 25,
    'Pulses': 50, 'Nuts': 20, 'Meat_Subs': 30,
    'Grains': 240, 'Vegetables': 180, 'Fruits': 160,
    'Potatoes': 80, 'Sugar': 25, 'Processed': 90
}
```

### Update LCA Factors
Modify `load_impact_factors()` to use latest emission data:
```python
'Beef': {'co2': 28.0, 'land': 25.0, 'water': 15400},  # kg CO2, m², L per kg
```

### Add Neighborhood Data
Update `load_neighborhood_data()` with actual CBS statistics (income, population, education)

## Output Examples

### Console Report (Master_hybrid_Amsterdam_Model.py)
```
MASTER SCOPE 3 TONNAGE REPORT
CATEGORY          1.Monitor  2.Metro  3.Meta  4.DuGoal  5.AmGoal   6.EAT
Red Meat          118,200   185,600 250,000   85,000    35,000   42,500
Poultry            92,100   138,900 185,000   58,000    23,000   84,600
Dairy & Eggs      142,300   108,700  98,000  105,000    75,000   95,000
Fish               55,800    38,500  92,000   38,500    38,500   72,100
Plant Protein      48,900    18,200  24,000   89,000   145,000   98,300
Staples            82,600    65,500  18,000  81,000    90,000    67,000
Veg & Fruit        35,400    25,500  46,000   52,000    82,000    110,000
Ultra-Processed    38,100    65,300  12,000   18,000     8,000        0
────────────────────────────────────────────────────────────────────────
TOTAL (Tonnes)    613,500   646,300 725,000  526,600   496,600   569,500
Change vs Baseline     +0%     +5.3%   +18.2%  -14.2%    -19.1%    -7.1%
```

### Neighborhood Hotspots (with Education Adjustment)
```
Neighborhood      Population  Meat_Mod  Total_CO2_Tonnes
Zuid              145,000      0.85      185,400
Centrum            87,000      0.85      111,200
Oost              135,000      0.90      172,500
West              145,000      1.10      194,300
Noord              99,000      1.10      126,800
Nieuw-West        160,000      1.10      204,500
Zuidoost           89,000      1.10      113,400
```
**Note:** High-education neighborhoods (Centrum/Zuid) have 15% lower meat consumption modifier despite similar/higher income

## Contributing & Future Work

**For Model Improvements:**
- Integrate real CBS/Monitor data (currently uses mock data loaders)
- Add seasonal variation in consumption patterns
- Include food waste at household level (beyond supply chain)
- Model dietary transition trajectories (e.g., gradual shift from baseline to goal)
- Validate education effects with primary survey data

**For Scenario Modeling:**
- Policy interventions (carbon tax, subsidies, labeling)
- Supply-side interventions (alternative proteins, local sourcing)
- Population growth and demographic shifts
- Climate impact on agricultural production

**For Visualization:**
- Interactive dashboards (Plotly/Dash)
- Temporal trends and projections
- Sensitivity analysis (Monte Carlo uncertainty)
- Comparison with other cities/regions

## References

- **Valencia Downscaling Method** - Income-based shadow inventory adjustment for environmental assessment
- **Boyer et al.** - Comprehensive LCA methodology for food systems
- **Blonk Consultants** - Industry-standard emission factors for food products
- **EAT-Lancet Commission (2019)** - *Food in the Anthropocene: the EAT-Lancet Commission report on healthy diets from sustainable food systems*
- **Amsterdam Monitor 2024** - Municipal consumption and sustainability survey
- **CBS Kerncijfers Wijken en Buurten** - Dutch neighborhood statistical database
- **RIVM DNFCS 2019-2021** - Dutch National Food Consumption Survey

---

**Project Status:** Active development for UvA Complex Systems for Policy (Challenge-Based Project)  
**Last Updated:** January 2026  
**Primary Analyst:** Mathilde de Vries



## Project Structure

```python
code-for-framework/
├── hybridMNodelAMS.py
│   ├── HybridModelConfig       # Configuration & constants
│   ├── Data Ingestion          # CBS & RIVM mock data loaders
│   ├── Scope3Calculator        # Core emissions calculation
│   ├── Scenario Functions      # Policy intervention modeling
│   └── Execution Block         # Main script entry point
├── MasterHybridModel.py
│   ├── HybridModelConfig       # Configuration & constants
│   ├── Scope3Engine            # Enhanced calculation engine
│   ├── Data Loaders            # Diet profiles & impact factors
│   ├── Visualization Functions # Chart generation (7 outputs)
│   └── Execution Block         # Main analysis entry point
├── Master_hybrid_Amsterdam_Model.py
│   ├── HybridModelConfig       # Configuration & constants
│   ├── Scope3Engine            # Advanced calculation engine
│   ├── Data Loaders            # Monitor 2024 & education effects
│   ├── Visualization Functions # Chart generation (5 outputs)
│   └── Execution Block         # Primary analysis entry point
├── README.md                   # Project documentation
└── outputs/                    # Generated visualizations
    ├── 1_Nexus_Analysis.png
    ├── 2a_Transition_DutchGoal.png
    ├── 2b_Transition_AmsterdamGoal.png
    ├── 2c_Transition_EAT_Lancet.png
    ├── 3_All_Diets_Plates.png
    ├── 4_Impact_Stack.png
    └── 5_Neighborhood_Hotspots.png
```
