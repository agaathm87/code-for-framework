"""
Hybrid Amsterdam Food Scope 3 Model

This module implements a hybrid modeling approach combining:
- Boyer's Life Cycle Assessment (LCA) methodology for emission factors
- Valencia's spatial downscaling technique for neighborhood-level analysis

The model estimates Scope 3 food-related emissions across Amsterdam neighborhoods
by integrating national consumption data with local socio-economic indicators.

Main components:
1. Configuration: Model parameters and constants
2. Data Ingestion: CBS neighborhood data and RIVM consumption data
3. Core Logic: Scope 3 calculation engine with Valencia downscaling
4. Scenario Analysis: Policy intervention simulations (protein transition, waste reduction)

Author: Challenge Based Project Team
Date: 2026
"""

import pandas as pd
import numpy as np

# ==========================================
# 1. MODEL CONFIGURATION & CONSTANTS
# ==========================================
class HybridModelConfig:
    """
    Configuration for the Hybrid Amsterdam Model.
    Integrates parameters from Boyer (LCA) and Valencia (Downscaling).
    """
    def __init__(self):
        # National Average Income (Netherland) - Placeholder for CBS data
        self.NATIONAL_AVG_INCOME = 32000  # Euros/year
        
        # Waste Coefficient (W) - Derived from AEB/Boyer logic
        # Represents upstream + retail waste not captured in consumption surveys
        self.WASTE_FACTOR = 1.15  # 15% added buffer for waste
        
        # Valencia Scaling Constants (C1, C2)
        # These define the sensitivity of consumption to income.
        # In a real scenario, these are derived from regression analysis.
        # Beta = C1 * exp(C2 * Income_Normalized)
        self.SCALING_C1 = 0.8
        self.SCALING_C2 = 0.2

# ==========================================
# 2. DATA INGESTION (MOCK DATA GENERATORS)
# ==========================================
def load_cbs_neighborhood_data():
    """
    Simulates loading CBS 'Kerncijfers wijken en buurten'.
    Variables: Neighborhood Name, Population, Average Income.
    """
    data = {
        'neighborhood_id':,
        'neighborhood_name':,
        'population': ,
        'avg_income':  # Variable In from Valencia
    }
    return pd.DataFrame(data)

def load_rivm_consumption_data():
    """
    Simulates loading RIVM DNFCS 2019-2021 (National Diet).
    Variables: Food Category, kg/capita/year, Emission Factor (LCA).
    """
    data = {
        'food_category':,
        'national_kg_per_capita': [15.4, 95.0, 120.0, 80.0, 5.0],
        # EF: kgCO2e per kg product (Trans-boundary LCA from Blonk/Boyer)
        'emission_factor': [25.0, 3.2, 0.4, 0.5, 1.2], 
        # Elasticity: Does consumption rise with income? (1=Yes, 0=Neutral, -1=Inferior)
        'income_elasticity': [1.2, 1.0, 1.1, 0.9, 1.5] 
    }
    return pd.DataFrame(data)

# ==========================================
# 3. CORE LOGIC: THE HYBRID CALCULATOR
# ==========================================
class Scope3Calculator:
    """
    Core calculation engine for Scope 3 food emissions.
    
    Combines national consumption data with local socio-economic factors
    to estimate neighborhood-level food system emissions.
    
    Attributes:
        cfg (HybridModelConfig): Configuration object with model parameters
    """
    
    def __init__(self, config):
        """
        Initialize the calculator with a configuration object.
        
        Args:
            config (HybridModelConfig): Model configuration and parameters
        """
        self.cfg = config

    def calculate_beta_factor(self, local_income, elasticity):
        """
        Implements the Valencia Downscaling Function.
        
        Adjusts national average consumption based on local income deviation.
        Uses the power-law relationship: Beta = (Local_Income / National_Income) ^ Elasticity
        
        Args:
            local_income (float): Average income in the neighborhood (Euros/year)
            elasticity (float): Income elasticity of demand for the food category
                - >1: Luxury goods (consumption increases faster than income)
                - =1: Proportional (consumption matches income)
                - <1: Necessity goods (consumption increases slower than income)
        
        Returns:
            float: Beta scaling factor (multiplier for national consumption)
        """
        # Normalized income ratio
        income_ratio = local_income / self.cfg.NATIONAL_AVG_INCOME
        
        # If income data is missing (NaN), assume national average (Beta = 1.0)
        if pd.isna(local_income):
            return 1.0
            
        # Apply elasticity: 
        # Luxury goods (Beef) increase faster with income (>1)
        # Staples (Grains) might decrease or stay flat (<1)
        beta = np.power(income_ratio, elasticity)
        return beta

    def run_model(self, df_cbs, df_rivm):
        """
        Executes the full Hybrid Model calculation.
        
        Performs a double iteration:
        1. Iterates through neighborhoods (spatial dimension - 'Who')
        2. Iterates through food groups (consumption dimension - 'What')
        3. Calculates total Scope 3 emissions combining both dimensions
        
        The model applies:
        - Valencia downscaling (beta factor) for local consumption estimation
        - Boyer LCA emission factors for environmental impact
        - Waste factors for supply chain losses
        
        Args:
            df_cbs (pd.DataFrame): CBS neighborhood data with columns:
                - neighborhood_name, population, avg_income
            df_rivm (pd.DataFrame): RIVM consumption data with columns:
                - food_category, national_kg_per_capita, emission_factor, income_elasticity
        
        Returns:
            pd.DataFrame: Results table with emissions per neighborhood per food category
        """
        results =

        print("--- Starting Hybrid Model Simulation ---")
        
        for _, buurt in df_cbs.iterrows():
            buurt_name = buurt['neighborhood_name']
            population = buurt['population']
            income = buurt['avg_income']
            
            for _, food in df_rivm.iterrows():
                category = food['food_category']
                national_consumption = food['national_kg_per_capita']
                ef_origin = food['emission_factor']
                elasticity = food['income_elasticity']
                
                # STEP 1: Calculate Scale Factor (Beta)
                # Valencia Method: "Shadow Inventory" based on socio-economics
                beta = self.calculate_beta_factor(income, elasticity)
                
                # STEP 2: Estimate Local Consumption
                # C(i,n) = C(national) * Beta
                local_consumption_per_capita = national_consumption * beta
                total_consumption_volume = local_consumption_per_capita * population
                
                # STEP 3: Apply Emission Factors & Waste
                # E = Consumption * EF * WasteFactor
                total_emissions_tCO2e = (
                    total_consumption_volume * 
                    ef_origin * 
                    self.cfg.WASTE_FACTOR
                ) / 1000 # Convert kg to tonnes
                
                results.append({
                    'Neighborhood': buurt_name,
                    'Food_Category': category,
                    'Population': population,
                    'Beta_Factor': round(beta, 3),
                    'Est_Consumption_Tonnes': round(total_consumption_volume / 1000, 2),
                    'Total_Scope3_tCO2e': round(total_emissions_tCO2e, 2)
                })
        
        return pd.DataFrame(results)

# ==========================================
# 4. SCENARIO ANALYSIS (INTERVENTION LEVERS)
# ==========================================
def run_protein_transition_scenario(df_results, reduction_target=0.5):
    """
    Simulates the 'Protein Transition' policy intervention.
    
    Models the impact of shifting from animal-based to plant-based proteins
    by reducing meat/dairy consumption and replacing with plant alternatives.
    
    This scenario reflects Amsterdam's protein transition goals where
    citizens reduce animal protein intake in favor of legumes, nuts, and
    plant-based meat substitutes.
    
    Args:
        df_results (pd.DataFrame): Baseline emission results from run_model()
        reduction_target (float): Fraction of meat/dairy to reduce (0.5 = 50% reduction)
    
    Prints:
        - Baseline total emissions
        - Scenario total emissions
        - Absolute and relative emission savings
    """
    print(f"\n--- Running Scenario: {reduction_target*100}% Meat Reduction ---")
    
    # Filter for baseline
    baseline_emissions = df_results.sum()
    
    # Apply logic
    df_scenario = df_results.copy()
    
    # Identify meat rows
    is_meat = df_scenario['Food_Category'].isin()
    
    # Reduce Meat Emissions
    df_scenario.loc *= (1 - reduction_target)
    
    # Calculate savings
    new_emissions = df_scenario.sum()
    savings = baseline_emissions - new_emissions
    
    print(f"Baseline Emissions: {baseline_emissions:,.0f} tCO2e")
    print(f"Scenario Emissions: {new_emissions:,.0f} tCO2e")
    print(f"Total Reduction: {savings:,.0f} tCO2e (-{(savings/baseline_emissions)*100:.1f}%)")
    
def run_food_waste_reduction_scenario(calculator, df_cbs, df_rivm, reduction_target=0.5):
    """
    Simulates the 'Circular Food System' policy intervention.
    
    Models the impact of reducing food waste across the supply chain
    (upstream production, retail losses, and consumer waste).
    
    The waste factor represents the additional food that must be produced
    to account for losses. Reducing this factor simulates better:
    - Supply chain efficiency
    - Retail inventory management
    - Consumer behavior change (less household waste)
    
    This aligns with Amsterdam's 2030 circular economy goals.
    
    Args:
        calculator (Scope3Calculator): The calculator instance to modify
        df_cbs (pd.DataFrame): CBS neighborhood data
        df_rivm (pd.DataFrame): RIVM consumption data
        reduction_target (float): Fraction of waste to eliminate (0.5 = 50% waste reduction)
    
    Returns:
        pd.DataFrame: Updated emission results after waste reduction
    
    Prints:
        - Original and new waste factors
        - Baseline vs scenario emissions
        - Emission savings achieved
    """
    # 1. Capture Baseline State
    # Run the model with the default configuration (e.g., Waste Factor 1.15)
    baseline_results = calculator.run_model(df_cbs, df_rivm)
    baseline_total = baseline_results.sum()
    
    # 2. Modify the WASTE_FACTOR
    # Logic: The factor 1.15 implies 15% waste. We want to reduce that 0.15 portion.
    original_factor = calculator.cfg.WASTE_FACTOR
    waste_portion = original_factor - 1.0
    new_waste_portion = waste_portion * (1.0 - reduction_target)
    new_factor = 1.0 + new_waste_portion
    
    print(f"\n--- Running Scenario: {reduction_target*100}% Food Waste Reduction ---")
    print(f"Adjusting Waste Factor: {original_factor} -> {new_factor:.3f}")
    
    # Apply new factor to the calculator's config
    calculator.cfg.WASTE_FACTOR = new_factor
    
    # 3. Re-Run Model with New Factor
    scenario_results = calculator.run_model(df_cbs, df_rivm)
    scenario_total = scenario_results.sum()
    
    # 4. Calculate & Print Impact
    savings = baseline_total - scenario_total
    print(f"Baseline Emissions: {baseline_total:,.0f} tCO2e")
    print(f"Scenario Emissions: {scenario_total:,.0f} tCO2e")
    print(f"Total Reduction: {savings:,.0f} tCO2e (-{(savings/baseline_total)*100:.1f}%)")
    
    # 5. Reset Config (Important!)
    # Restore the original factor so subsequent runs aren't affected
    calculator.cfg.WASTE_FACTOR = original_factor
    
    return scenario_results

# ==========================================
# 5. EXECUTION
# ==========================================
if __name__ == "__main__":
    """
    Main execution block.
    
    Workflow:
    1. Initialize model configuration
    2. Load neighborhood and consumption data
    3. Run baseline emission calculations
    4. Perform hotspot analysis to identify high-impact areas
    5. Simulate policy scenarios (protein transition, waste reduction)
    """
    
    # Initialize configuration and calculator
    config = HybridModelConfig()
    calculator = Scope3Calculator(config)
    
    # Load Data
    cbs_data = load_cbs_neighborhood_data()
    rivm_data = load_rivm_consumption_data()
    
    # Run Baseline Model
    impact_data = calculator.run_model(cbs_data, rivm_data)
    
    # Show "Hotspot" Analysis (Top 5 High Impact Areas)
    print("\n--- Neighborhood Hotspot Analysis (Top 5) ---")
    hotspots = impact_data.groupby('Neighborhood').sum().sort_values(ascending=False)
    print(hotspots.head())
    
    # Run Policy Scenario
    # Run Protein Transition Scenario
    run_protein_transition_scenario(impact_data)

    # Run Food Waste Reduction Scenario (New)
    # Note: We pass the calculator object itself to allow config modification
    run_food_waste_reduction_scenario(calculator, cbs_data, rivm_data, reduction_target=0.5)