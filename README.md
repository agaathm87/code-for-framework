# Hybrid Amsterdam Model (HAM)

A Python framework for calculating **Scope 3 GHG emissions** from food consumption at the neighborhood level in Amsterdam. Integrates life cycle assessment (LCA) data with income-based consumption downscaling and provides comprehensive visualization of dietary impact scenarios.

## Overview

This project contains two complementary Python modules:

1. **hybridMNodelAMS.py** - Core hybrid model with spatial analysis and scenario modeling
2. **MasterHybridModel.py** - Enhanced analysis with 6 dietary scenarios and comprehensive visualizations

## Features

- **Income-Sensitive Consumption**: Adjusts national dietary baselines using neighborhood income levels (Valencia method)
- **Life Cycle Assessment**: Incorporates LCA data for CO2, land use, and water consumption
- **Multi-Metric Analysis**: Tracks three environmental indicators (carbon, land, water) across food categories
- **6 Dietary Scenarios**: Compares baseline, metropolitan, metabolic balance, Dutch goal, Amsterdam goal, and EAT-Lancet diets
- **Waste Integration**: Accounts for upstream and retail waste via waste factor coefficients (default 1.15 = 15% loss)
- **Scenario Modeling**: Policy simulation (protein transition, food waste reduction)
- **Spatial Hotspot Analysis**: Identifies high-impact neighborhoods and visualizes emissions by location
- **Comprehensive Visualizations**: Generates publication-ready charts (nexus analysis, plate comparisons, impact stacks)

## Files

### hybridMNodelAMS.py
Foundational hybrid model implementation with core logic and spatial simulation.

**Key Classes:**
- `HybridModelConfig` - Configuration parameters (income, waste factor, scaling constants)
- `Scope3Calculator` - Core emissions calculator with beta factor logic

**Functions:**
- `load_cbs_neighborhood_data()` - Loads neighborhood demographics
- `load_rivm_consumption_data()` - Loads food consumption and emission factors
- `run_protein_transition_scenario()` - Models meat reduction policy
- `run_food_waste_reduction_scenario()` - Models waste reduction policy

**Output:** DataFrame with per-neighborhood, per-food-category emissions

### MasterHybridModel.py
Advanced analysis module with 6 dietary scenarios and professional visualizations.

**Key Classes:**
- `HybridModelConfig` - Same configuration as hybridMNodelAMS
- `Scope3Engine` - Enhanced engine with aggregation and visualization logic

**Key Functions:**
- `load_diet_profiles()` - Returns 6 dietary scenarios (baseline to EAT-Lancet)
- `load_impact_factors()` - Multi-metric LCA data (CO2, land, water)
- `load_neighborhood_data()` - Amsterdam neighborhoods with population and income
- `run_spatial_simulation()` - Calculates emissions per neighborhood with income scaling

**Visualizations Generated:**
1. **1_Nexus_Analysis.png** - 3-panel comparison of CO2, land, and water across diets
2. **2a_Transition_DutchGoal.png** - Baseline vs Dutch Goal (60:40 animal:plant protein)
3. **2b_Transition_AmsterdamGoal.png** - Baseline vs Amsterdam Goal (70:30)
4. **2c_Transition_EAT_Lancet.png** - Baseline vs EAT-Lancet planetary diet
5. **3_All_Diets_Plates.png** - 6-panel plate composition for all diets
6. **4_Impact_Stack.png** - Stacked bar chart of emissions by food category
7. **5_Neighborhood_Hotspots.png** - Horizontal bar chart of emissions by neighborhood

## Data Sources

- **CBS (Centraal Bureau voor Statistiek)**: Neighborhood demographics (population, income)
- **RIVM (National Institute for Public Health)**: DNFCS 2019-2021 national diet and consumption patterns
- **LCA Sources**: Boyer/Blonk emission factors for food items (trans-boundary)

## Core Model Equation

```
Emissions(i,n) = Consumption(national) × Beta(local_income) × EF × WasteFactor
```

Where:
- `Beta` = Income elasticity adjustment (Valencia method)
- `EF` = Emission factor (kgCO2e per kg food)
- `WasteFactor` = Supply chain loss coefficient (1.15 = 15% waste)

## Diet Profiles

The model compares 6 dietary scenarios:

1. **Amsterdam Baseline** - Current Amsterdam consumption patterns
2. **Metropolitan (High Risk)** - High meat/processed food (worst case)
3. **Metabolic Balance (Animal)** - High-protein, low-carb variant
4. **Dutch Goal (60:40)** - 60% plant, 40% animal protein target
5. **Amsterdam Goal (70:30)** - 70% plant, 30% animal protein (municipal target)
6. **EAT-Lancet (Planetary)** - Planetary health diet recommended by EAT-Lancet Commission

## Requirements

- pandas
- numpy
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/agaathm87/code-for-framework.git
cd code-for-framework
```

2. Install dependencies:
```bash
pip install pandas numpy matplotlib
```

3. Run the analysis:
```bash
python MasterHybridModel.py
```

## Usage

### Basic Model (hybridMNodelAMS.py)
```python
from hybridMNodelAMS import HybridModelConfig, Scope3Calculator

config = HybridModelConfig()
calculator = Scope3Calculator(config)

cbs_data = load_cbs_neighborhood_data()
rivm_data = load_rivm_consumption_data()

results = calculator.run_model(cbs_data, rivm_data)
print(results)
```

### Full Analysis with Visualizations (MasterHybridModel.py)
```bash
python MasterHybridModel.py
```
This generates all 7 visualization PNG files and console output with:
- Complete tonnage report comparing all 6 diets
- Per-category emissions breakdown
- Neighborhood hotspot analysis with income-scaled impacts

### Scenario Analysis
```python
# Protein transition (50% meat reduction)
run_protein_transition_scenario(results, reduction_target=0.5)

# Food waste reduction (50% waste factor reduction)
run_food_waste_reduction_scenario(calculator, cbs_data, rivm_data, reduction_target=0.5)
```

## Configuration Parameters

Edit `HybridModelConfig` to adjust:

- `NATIONAL_AVG_INCOME` - Netherlands average income baseline (€32,000/year)
- `WASTE_FACTOR` - Supply chain loss multiplier (1.15 = 15% waste)
- `SCALING_C1, SCALING_C2` - Valencia income elasticity parameters
- `POPULATION_TOTAL` - Amsterdam total population (882,000)

## Output Examples

### Console Report
```
MASTER SCOPE 3 TONNAGE REPORT
CATEGORY          1.Bsline    2.Metro   3.Meta  4.DuGoal  5.AmGoal   6.EAT
Red Meat          125,450    185,600  250,000   85,000    35,000   42,500
Dairy & Eggs       95,300     78,900   42,000   72,000    48,000   65,000
...
TOTAL (Tonnes)    892,340  1,142,560  985,000  654,200   389,000  523,600
Change vs Baseline     +0%      +28%     +10%     -27%      -56%      -41%
```

### Neighborhood Hotspots
```
Neighborhood      Population       Beta  Total_CO2_Tonnes
Zuid               145,000       1.75        289,500
Centrum             87,000       1.50        130,500
...
```

## Contributing

For model improvements:
- Update LCA data in `load_impact_factors()` or `load_rivm_consumption_data()`
- Add new diets to `load_diet_profiles()`
- Modify scenario functions for new policy interventions
- Adjust visualization styles in `run_full_analysis()`

## References

- **Boyer et al.** - LCA methodology for food systems
- **Valencia Downscaling Method** - Income-based consumption adjustment
- **EAT-Lancet Commission (2019)** - Planetary health diet
- **CBS Kerncijfers** - Amsterdam neighborhood statistics
- **RIVM DNFCS** - Dutch National Food Consumption Survey

## License

MIT License

## Author

Mathilde de Vries | UvA Complex Systems for Policy



## Project Structure

```
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
