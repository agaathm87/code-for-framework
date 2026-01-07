# Hybrid Amsterdam Model (HAM)

## Overview

A Python framework for calculating **Scope 3 GHG emissions** from food consumption at the neighborhood level in Amsterdam. Integrates life cycle assessment (LCA) data with income-based consumption downscaling.

## Features

- **Income-Sensitive Consumption**: Adjusts national dietary baselines using neighborhood income levels
- **Food Category Analysis**: Tracks emissions across multiple food groups with elasticity factors
- **Waste Integration**: Accounts for upstream and retail waste via scaling coefficients
- **Scenario Modeling**: Policy simulation (e.g., protein transition interventions)
- **Hotspot Analysis**: Identifies high-impact neighborhoods

## Data Sources

- **CBS**: Neighborhood population & income (kerncijfers, wijken en buurten)
- **RIVM**: National food consumption & emission factors (DNFCS 2019-2021)

## Core Model
```
Emissions(i,n) = Consumption(national) × Beta(income, elasticity) × EF × WasteFactor
```

## Usage
```python
config = HybridModelConfig()
calculator = Scope3Calculator(config)
results = calculator.run_model(cbs_data, rivm_data)
```

## Requirements
- pandas
- numpy
    ```

## Project Structure
    ```
    hybridMNodelAMS.py
    ├── HybridModelConfig       # Configuration & constants
    ├── Data Ingestion          # CBS & RIVM mock data loaders
    ├── Scope3Calculator        # Core emissions calculation
    ├── Scenario Functions      # Policy intervention modeling
    └── Execution Block         # Main script entry point