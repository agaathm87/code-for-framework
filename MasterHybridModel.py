"""
Master Hybrid Amsterdam Food Systems Model

This model provides a comprehensive analysis of Amsterdam's food system emissions
through multi-scenario diet comparisons and spatial impact analysis.

Key Features:
- Compares 6 diet scenarios from current baseline to planetary health diets
- Calculates Scope 3 emissions across CO2, land use, and water footprints
- Generates visual outputs (pie charts, stacked bars, transition diagrams)
- Performs neighborhood-level hotspot analysis with income-based scaling
- Supports policy scenario testing and impact quantification

Outputs:
- 1_Nexus_Analysis.png: Multi-dimensional impact comparison
- 2_Transition_*.png: Baseline vs goal state visualizations
- 3_All_Diets_Plates.png: Comparative diet composition
- 4_Impact_Stack.png: Stacked emissions by category
- 5_Neighborhood_Hotspots.png: Spatial emission distribution
- Console: Detailed tonnage report and comparative statistics

Author: Challenge Based Project Team
Date: January 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. CONFIGURATION
# ==========================================
class HybridModelConfig:
    """
    Configuration parameters for the hybrid food systems model.
    
    Attributes:
        NATIONAL_AVG_INCOME (int): Netherlands average household income (EUR/year)
        SCALING_C1 (float): Valencia scaling coefficient (base multiplier)
        SCALING_C2 (float): Valencia scaling exponent (income sensitivity)
        WASTE_FACTOR (float): Supply chain loss multiplier (1.15 = 15% waste)
        POPULATION_TOTAL (int): Total Amsterdam population
    """
    
    def __init__(self):
        self.NATIONAL_AVG_INCOME = 32000  # EUR/year - CBS national average
        self.SCALING_C1 = 0.8  # Valencia base scaling coefficient
        self.SCALING_C2 = 0.2  # Valencia income elasticity exponent
        self.WASTE_FACTOR = 1.15  # 15% supply chain loss (AEB/Boyer)
        self.POPULATION_TOTAL = 882000  # Amsterdam metro population

# --- VISUALIZATION MAPPING ---
# Maps individual food items to aggregated categories for cleaner visualizations
VISUAL_MAPPING = {
    'Beef': 'Red Meat', 'Pork': 'Red Meat',
    'Chicken': 'Poultry', 'Poultry': 'Poultry',
    'Cheese': 'Dairy & Eggs', 'Milk': 'Dairy & Eggs', 'Eggs': 'Dairy & Eggs', 'Dairy': 'Dairy & Eggs',
    'Fish': 'Fish',
    'Pulses': 'Plant Protein', 'Nuts': 'Plant Protein', 'Meat_Subs': 'Plant Protein', 'Plant Protein': 'Plant Protein',
    'Grains': 'Staples', 'Potatoes': 'Staples', 'Staples': 'Staples',
    'Vegetables': 'Veg & Fruit', 'Fruits': 'Veg & Fruit', 'Veg & Fruit': 'Veg & Fruit',
    'Sugar': 'Ultra-Processed', 'Processed': 'Ultra-Processed', 'Ultra-Processed': 'Ultra-Processed'
}

# --- VISUALIZATION CONSTANTS ---
# Order of food categories for consistent chart display
CAT_ORDER = ['Red Meat', 'Poultry', 'Dairy & Eggs', 'Fish', 'Plant Protein', 'Staples', 'Veg & Fruit', 'Ultra-Processed']

# Color palette for food categories (high to low environmental impact)
COLORS = ['#8B0000', '#F08080', '#FFD700', '#4682B4', '#2E8B57', '#DEB887', '#90EE90', '#A9A9A9']

# ==========================================
# 2. DATA INGESTION
# ==========================================
def load_impact_factors():
    """ 
    Load Scope 3 environmental impact factors for food items.
    
    Based on trans-boundary LCA data from Blonk Consultants and Boyer et al.
    
    Returns:
        pd.DataFrame: Impact factors with columns:
            - co2: kg CO2e per kg product (climate impact)
            - land: m² per kg product (land use)
            - water: liters per kg product (blue water consumption)
            - scope12: kg CO2e per kg consumed (complete system boundary)
    """
    # FULL FOOD SYSTEM Scope 1+2 factors (kgCO2e/kg consumed) - CALIBRATED TO MONITOR 1750 KTON
    # Includes: Production + Retail + Food Service + Household (cooking/refrigeration) + Waste Management
    # System boundary verified against Amsterdam Monitor 2024 (1750 kton total Scope 1+2)
    # All 22 food items explicitly modeled for transparency
    factors = {
        'Beef':       {'co2': 28.0,  'land': 25.0,  'water': 15400, 'scope12': 16.67},
        'Pork':       {'co2': 5.0,   'land': 9.0,   'water': 6000,  'scope12': 13.34},
        'Chicken':    {'co2': 3.5,   'land': 7.0,   'water': 4300,  'scope12': 10.00},
        'Cheese':     {'co2': 10.0,  'land': 12.0,  'water': 5000,  'scope12': 6.67},
        'Milk':       {'co2': 1.3,   'land': 1.5,   'water': 1000,  'scope12': 3.33},
        'Fish':       {'co2': 3.5,   'land': 0.5,   'water': 2000,  'scope12': 12.00},
        'Eggs':       {'co2': 2.2,   'land': 2.5,   'water': 3300,  'scope12': 5.34},
        'Pulses':     {'co2': 0.9,   'land': 3.0,   'water': 4000,  'scope12': 2.67},
        'Nuts':       {'co2': 0.3,   'land': 2.5,   'water': 9000,  'scope12': 1.33},
        'Meat_Subs':  {'co2': 2.5,   'land': 3.0,   'water': 200,   'scope12': 3.33},
        'Grains':     {'co2': 1.1,   'land': 1.8,   'water': 1600,  'scope12': 1.67},
        'Vegetables': {'co2': 0.6,   'land': 0.5,   'water': 320,   'scope12': 1.33},
        'Fruits':     {'co2': 0.7,   'land': 0.6,   'water': 960,   'scope12': 1.33},
        'Potatoes':   {'co2': 0.4,   'land': 0.3,   'water': 290,   'scope12': 1.33},
        'Sugar':      {'co2': 2.0,   'land': 1.5,   'water': 200,   'scope12': 1.33},
        'Processed':  {'co2': 2.5,   'land': 1.5,   'water': 300,   'scope12': 3.33},
        'Coffee':     {'co2': 2.8,   'land': 0.8,   'water': 140,   'scope12': 23.34},
        'Tea':        {'co2': 0.4,   'land': 0.2,   'water': 300,   'scope12': 8.00},
        'Alcohol':    {'co2': 1.2,   'land': 0.5,   'water': 500,   'scope12': 13.34},
        'Oils':       {'co2': 1.0,   'land': 1.0,   'water': 200,   'scope12': 5.34},
        'Snacks':     {'co2': 2.0,   'land': 1.5,   'water': 300,   'scope12': 10.00},
        'Condiments': {'co2': 0.8,   'land': 0.4,   'water': 100,   'scope12': 4.00}
    }
    return pd.DataFrame.from_dict(factors, orient='index')

def load_diet_profiles():
    """ 
    Load dietary scenario profiles for comparison analysis.
    
    Each diet represents a different consumption pattern:
    1. Monitor 2024: Amsterdam empirical data (48% plant protein, 52% animal)
    2. Schijf van 5: Dutch dietary guidelines (reference baseline)
    3. EAT-Lancet: Planetary health diet (global sustainability benchmark)
    4. Dutch Goal (60:40): National policy target (60% plant, 40% animal protein)
    5. Amsterdam Goal (70:30): City policy target (70% plant, 30% animal protein)
    6. Metropolitan: High-risk Western diet (comparison scenario)
    
    Returns:
        dict: Dictionary of diet names to food consumption profiles (grams/day)
    """
    diets = {
        '1. Monitor 2024 (Current)': {
            'Beef': 10, 'Pork': 15, 'Chicken': 25, 'Cheese': 35, 'Milk': 220, 
            'Fish': 22, 'Eggs': 28, 'Pulses': 15, 'Nuts': 15, 'Meat_Subs': 20, 
            'Grains': 230, 'Vegetables': 160, 'Fruits': 145, 'Potatoes': 45,
            'Sugar': 35, 'Processed': 140,
            'Coffee': 12, 'Tea': 3, 'Alcohol': 25, 'Oils': 25, 'Snacks': 45, 'Condiments': 20
        },
        '2. Schijf van 5 (Guideline)': {
            'Beef': 10, 'Pork': 10, 'Chicken': 25, 'Cheese': 30, 'Milk': 250,
            'Fish': 25, 'Eggs': 20, 'Pulses': 30, 'Nuts': 25, 'Meat_Subs': 20,
            'Grains': 240, 'Vegetables': 250, 'Fruits': 200, 'Potatoes': 70,
            'Sugar': 25, 'Processed': 60,
            'Coffee': 10, 'Tea': 4, 'Alcohol': 15, 'Oils': 20, 'Snacks': 30, 'Condiments': 15
        },
        '3. EAT-Lancet (Planetary)': {
            'Beef': 7, 'Pork': 7, 'Chicken': 29, 'Cheese': 0, 'Milk': 250,
            'Fish': 28, 'Eggs': 13, 'Pulses': 75, 'Nuts': 50, 'Meat_Subs': 0,
            'Grains': 232, 'Vegetables': 300, 'Fruits': 200, 'Potatoes': 50,
            'Sugar': 30, 'Processed': 0,
            'Coffee': 8, 'Tea': 5, 'Alcohol': 10, 'Oils': 18, 'Snacks': 15, 'Condiments': 12
        },
        '4. Dutch Goal (60:40)': {
            'Beef': 15, 'Pork': 15, 'Chicken': 25, 'Cheese': 35, 'Milk': 250,
            'Fish': 15, 'Eggs': 20, 'Pulses': 40, 'Nuts': 20, 'Meat_Subs': 25,
            'Grains': 225, 'Vegetables': 200, 'Fruits': 180, 'Potatoes': 90,
            'Sugar': 30, 'Processed': 80,
            'Coffee': 10, 'Tea': 4, 'Alcohol': 20, 'Oils': 22, 'Snacks': 35, 'Condiments': 15
        },
        '5. Amsterdam Goal (70:30)': {
            'Beef': 5, 'Pork': 5, 'Chicken': 10, 'Cheese': 20, 'Milk': 100,
            'Fish': 15, 'Eggs': 15, 'Pulses': 80, 'Nuts': 40, 'Meat_Subs': 40,
            'Grains': 250, 'Vegetables': 250, 'Fruits': 200, 'Potatoes': 80,
            'Sugar': 20, 'Processed': 50,
            'Coffee': 9, 'Tea': 5, 'Alcohol': 12, 'Oils': 20, 'Snacks': 25, 'Condiments': 12
        },
        '6. Metropolitan (High Risk)': {
            'Beef': 45, 'Pork': 25, 'Chicken': 60, 'Cheese': 50, 'Milk': 200,
            'Fish': 15, 'Eggs': 30, 'Pulses': 5, 'Nuts': 5, 'Meat_Subs': 5,
            'Grains': 180, 'Vegetables': 110, 'Fruits': 100, 'Potatoes': 80,
            'Sugar': 80, 'Processed': 200,
            'Coffee': 15, 'Tea': 2, 'Alcohol': 35, 'Oils': 30, 'Snacks': 70, 'Condiments': 25
        },
        '7. Schijf van 5 (Guideline)': {
            'Beef': 10, 'Pork': 10, 'Chicken': 25, 'Cheese': 30, 'Milk': 250,
            'Fish': 25, 'Eggs': 20, 'Pulses': 30, 'Nuts': 25, 'Meat_Subs': 20,
            'Grains': 240, 'Vegetables': 250, 'Fruits': 200, 'Potatoes': 70,
            'Sugar': 25, 'Processed': 60,
            'Coffee': 12, 'Tea': 3, 'Alcohol': 20, 'Oils': 25, 'Snacks': 35, 'Condiments': 18
        },
        '8. Mediterranean Diet': {
            'Beef': 8, 'Pork': 8, 'Chicken': 20, 'Cheese': 30, 'Milk': 200,
            'Fish': 35, 'Eggs': 18, 'Pulses': 60, 'Nuts': 30, 'Meat_Subs': 10,
            'Grains': 240, 'Vegetables': 300, 'Fruits': 220, 'Potatoes': 60,
            'Sugar': 20, 'Processed': 50,
            'Coffee': 8, 'Tea': 5, 'Alcohol': 30, 'Oils': 30, 'Snacks': 25, 'Condiments': 15
        },
        '9. Amsterdam Theoretical': {
            'Beef': 12, 'Pork': 20, 'Chicken': 28, 'Cheese': 40, 'Milk': 260,
            'Fish': 10, 'Eggs': 25, 'Pulses': 8, 'Nuts': 10, 'Meat_Subs': 15,
            'Grains': 220, 'Vegetables': 150, 'Fruits': 130, 'Potatoes': 50,
            'Sugar': 40, 'Processed': 150,
            'Coffee': 12, 'Tea': 4, 'Alcohol': 30, 'Oils': 30, 'Snacks': 50, 'Condiments': 25
        }
    }
    return diets

def load_neighborhood_data():
    """ 
    Load Amsterdam neighborhood socio-economic data.
    
    Data simulates CBS 'Kerncijfers wijken en buurten' statistics.
    
    TWO BEHAVIORAL DRIVERS:
    1. Income effect: Higher income → higher total food consumption volume
    2. Education effect: Higher education → plant-based preference (lower meat, higher plant protein)
    
    These are INDEPENDENT and MULTIPLICATIVE:
    - Wealthy, educated (Zuid, Centrum): High volume × Low meat = Moderate meat total
    - Lower-income (Zuidoost): Low volume × High meat = Lower meat absolute
    
    Monitor finding: High education (52% plant) vs Low education (39% plant)
    
    Returns:
        pd.DataFrame: Neighborhood data with columns:
            - Neighborhood: District name
            - Population: Resident count
            - Avg_Income: Average household income (EUR/year)
            - High_Education_Pct: Fraction with bachelor degree or higher
    """
    return pd.DataFrame({
        'Neighborhood': ['Centrum', 'Zuid', 'West', 'Noord', 'Zuidoost', 'Nieuw-West', 'Oost'],
        'Population': [87000, 145000, 145000, 99000, 89000, 160000, 135000],
        'Avg_Income': [48000, 56000, 34000, 29000, 24000, 26000, 36000], # Euros/year
        'High_Education_Pct': [0.65, 0.70, 0.60, 0.40, 0.30, 0.35, 0.55] # From Monitor insights
    })

# ==========================================
# 3. CORE ENGINE
# ==========================================
class Scope3Engine:
    """
    Core calculation engine for Scope 3 food system emissions.
    
    Integrates:
    - Boyer LCA methodology for emission factors
    - Valencia spatial downscaling for neighborhood-level estimates
    - Multi-dimensional impact assessment (CO2, land, water)
    
    Attributes:
        cfg (HybridModelConfig): Model configuration parameters
        factors (pd.DataFrame): Environmental impact factors per food item
    """
    
    def __init__(self, config):
        """
        Initialize the Scope3 calculation engine.
        
        Args:
            config (HybridModelConfig): Configuration object with model parameters
        """
        self.cfg = config
        self.factors = load_impact_factors()

    # --- 3A. Beta Factor Logic (The "Hybrid" part) ---
    def calculate_beta(self, row):
        """ 
        Calculate composite consumption scaling factors with dual behavioral drivers.
        
        The Amsterdam Monitor revealed that:
        1. Higher income = MORE total food volume (wealthier people waste more)
        2. Higher education = LESS meat proportion (behavioral preference)
        
        These effects are INDEPENDENT and MULTIPLICATIVE:
        - A wealthy, educated person (Zuid) = High volume × Low meat = Moderate meat total
        - A lower-income person (Zuidoost) = Lower volume × High meat = Moderate meat total
        
        Args:
            row (pd.Series): Neighborhood data row with Avg_Income and High_Education_Pct
            
        Returns:
            tuple: (volume_beta, meat_modifier, plant_modifier)
                - volume_beta: Overall consumption scaling (0.8 to 1.2)
                - meat_modifier: Meat consumption adjustment (0.85 or 1.1)
                - plant_modifier: Plant consumption adjustment (1.15 or 0.9)
        """
        # 1. Volume Effect: Wealthier neighborhoods consume more total food
        income_ratio = row['Avg_Income'] / self.cfg.NATIONAL_AVG_INCOME
        volume_beta = self.cfg.SCALING_C1 * np.exp(self.cfg.SCALING_C2 * income_ratio)
        
        # 2. Education Effect: Higher education correlates with plant-based preference
        # Monitor data: 52% plant (high edu) vs 39% plant (low edu)
        if row['High_Education_Pct'] > 0.5:
            meat_modifier = 0.85   # Eat 15% less meat than average
            plant_modifier = 1.15  # Eat 15% more plant foods than average
        else:
            meat_modifier = 1.1    # Eat 10% more meat than average
            plant_modifier = 0.9   # Eat 10% less plant foods than average
            
        return volume_beta, meat_modifier, plant_modifier

    # --- 3B. Standard Impact Calculation (Per Capita Per Day) ---
    def calculate_raw_impact(self, diet_profile):
        """
        Calculate total environmental impact for a given diet profile.
        
        Sums impacts across all food items, accounting for:
        - Consumption amounts (grams/day)
        - Production losses (waste factor)
        - Environmental impact factors (CO2, land, water)
        
        Args:
            diet_profile (dict): Food items and daily consumption (grams)
            
        Returns:
            dict: Total daily per-capita impacts:
                - co2: kg CO2e per person per day
                - land: m² per person per day
                - water: liters per person per day
        """
        res = {'co2': 0, 'land': 0, 'water': 0}
        for food, grams in diet_profile.items():
            if food not in self.factors.index: continue
            kg_produced = (grams / 1000) * self.cfg.WASTE_FACTOR
            f = self.factors.loc[food]
            res['co2'] += kg_produced * f['co2']
            res['land'] += kg_produced * f['land']
            res['water'] += kg_produced * f['water']
        return res

    # --- 3C. Data Aggregation for Visualization ---
    def aggregate_visual_data(self, diet_profile):
        """
        Aggregate food items into broader categories for visualization.
        
        Converts individual food items (e.g., Beef, Pork, Chicken) into
        aggregated categories (e.g., Red Meat, Poultry) for clearer charts.
        Scales to city-wide annual emissions.
        
        Args:
            diet_profile (dict): Food items and daily consumption (grams)
            
        Returns:
            tuple: (mass_dict, co2_dict, scope12_dict, land_dict, water_dict)
                - mass_dict: Consumption mass by category (grams/day)
                - co2_dict: Annual city Scope 3 emissions by category (tonnes CO2e/year)
                - scope12_dict: Annual city Scope 1+2 emissions by category (tonnes CO2e/year)
                - land_dict: Annual city land use by category (m²/year)
                - water_dict: Annual city water use by category (liters/year)
        """
        agg_mass = {k: 0.0 for k in CAT_ORDER}
        agg_co2 = {k: 0.0 for k in CAT_ORDER}
        agg_scope12 = {k: 0.0 for k in CAT_ORDER}
        agg_land = {k: 0.0 for k in CAT_ORDER}
        agg_water = {k: 0.0 for k in CAT_ORDER}
        
        for food, grams in diet_profile.items():
            if food not in self.factors.index: continue
            category = VISUAL_MAPPING.get(food, 'Other')
            if category not in agg_mass: continue
            
            kg_consumed_yr = (grams / 1000) * 365
            kg_produced_yr = kg_consumed_yr * self.cfg.WASTE_FACTOR
            f = self.factors.loc[food]
            
            co2_tonnes = (kg_produced_yr * f['co2'] * self.cfg.POPULATION_TOTAL) / 1000
            scope12_tonnes = (kg_consumed_yr * f['scope12'] * self.cfg.POPULATION_TOTAL) / 1000
            land_m2 = kg_produced_yr * f['land'] * self.cfg.POPULATION_TOTAL
            water_l = kg_produced_yr * f['water'] * self.cfg.POPULATION_TOTAL
            
            agg_mass[category] += grams
            agg_co2[category] += co2_tonnes
            agg_scope12[category] += scope12_tonnes
            agg_land[category] += land_m2
            agg_water[category] += water_l
            
        return agg_mass, agg_co2, agg_scope12, agg_land, agg_water

    # --- 3D. Spatial Simulation (Hotspots) ---
    def run_spatial_simulation(self, neighborhoods, diet_profile):
        """
        Runs the model per neighborhood, scaling consumption by Beta.
        Returns DataFrame with 'Total_CO2_Tonnes' per neighborhood.
        
        NEW: Applies both volume_beta (income effect) and education modifiers
        (meat_modifier, plant_modifier) to neighborhood-specific consumption.
        """
        results = []
        base_impact = self.calculate_raw_impact(diet_profile) # Per capita impact of base diet
        
        for _, row in neighborhoods.iterrows():
            vol_beta, meat_mod, plant_mod = self.calculate_beta(row)
            
            # Weighted scaling: 40% meat modifier, 10% plant modifier, 50% neutral (dairy/other)
            local_scaling = (0.4 * meat_mod + 0.1 * plant_mod + 0.5 * 1.0) * vol_beta
            local_co2_per_capita = base_impact['co2'] * local_scaling
            
            # Total Neighborhood Tonnage
            total_tonnes = (local_co2_per_capita * 365 * row['Population']) / 1000
            
            results.append({
                'Neighborhood': row['Neighborhood'],
                'Population': row['Population'],
                'Income': row['Avg_Income'],
                'Education_Pct': row['High_Education_Pct'],
                'Vol_Beta': vol_beta,
                'Meat_Modifier': meat_mod,
                'Plant_Modifier': plant_mod,
                'Per_Capita_Daily_CO2': local_co2_per_capita,
                'Total_CO2_Tonnes': total_tonnes
            })
        return pd.DataFrame(results)

# ==========================================
# 4. EXECUTION & VISUALIZATION
# ==========================================
def run_full_analysis():
    cfg = HybridModelConfig()
    engine = Scope3Engine(cfg)
    diets = load_diet_profiles()
    neighborhoods = load_neighborhood_data()
    
    # ---------------------------------------------------------
    # PART A: DIET COMPARISONS (The Goals)
    # ---------------------------------------------------------
    results_mass = {}
    results_co2 = {}
    results_scope12 = {}
    results_land = {}
    results_water = {}
    
    print("Running Scope 3 Engine for all diets...")
    for name, profile in diets.items():
        mass, co2, scope12, land, water = engine.aggregate_visual_data(profile)
        results_mass[name] = mass
        results_co2[name] = co2
        results_scope12[name] = scope12
        results_land[name] = land
        results_water[name] = water

    # CHART 1: NEXUS ANALYSIS (All 6 Diets - Total Scope 1+2+3)
    print("Generating 1_Nexus_Analysis.png...")
    nexus_data = []
    for name in diets.keys():
        # Total CO2 = Scope 1+2 + Scope 3
        co2_total = (sum(results_scope12[name].values()) + sum(results_co2[name].values())) / cfg.POPULATION_TOTAL / 365
        land_total = sum(results_land[name].values()) / cfg.POPULATION_TOTAL / 365
        water_total = sum(results_water[name].values()) / cfg.POPULATION_TOTAL / 365
        nexus_data.append({
            'Diet': name.split('(')[0].strip(), 
            'co2': co2_total, 
            'land': land_total, 
            'water': water_total
        })
    df_nexus = pd.DataFrame(nexus_data).set_index('Diet').sort_values('co2', ascending=False)
    
    fig1, axes = plt.subplots(1, 3, figsize=(20, 6))
    df_nexus['co2'].plot(kind='bar', ax=axes[0], color='#E74C3C', title='Total CO2 (Scope 1+2+3) - kg/person/day', fontsize=11)
    df_nexus['land'].plot(kind='bar', ax=axes[1], color='#2ECC71', title='Land Use - m²/person/day', fontsize=11)
    df_nexus['water'].plot(kind='bar', ax=axes[2], color='#3498DB', title='Water Use - L/person/day', fontsize=11)
    for ax in axes:
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('1_Nexus_Analysis.png', dpi=300, bbox_inches='tight')

    # CHART 2: PROTEIN TRANSITION (For EVERY Goal)
    def plot_transition(baseline_key, goal_key, filename):
        print(f"Generating {filename}...")
        fig = plt.figure(figsize=(16, 10))
        grid = plt.GridSpec(2, 2)
        b_mass = [results_mass[baseline_key][c] for c in CAT_ORDER]
        g_mass = [results_mass[goal_key][c] for c in CAT_ORDER]
        b_co2 = [results_co2[baseline_key][c] for c in CAT_ORDER]
        g_co2 = [results_co2[goal_key][c] for c in CAT_ORDER]
        
        ax1 = fig.add_subplot(grid[0, 0])
        ax1.pie(b_mass, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax1.set_title(f"{baseline_key} (Mass)", fontweight='bold')
        ax1.add_artist(plt.Circle((0,0),0.70,fc='white'))
        
        ax2 = fig.add_subplot(grid[0, 1])
        ax2.pie(g_mass, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax2.set_title(f"{goal_key} (Mass)", fontweight='bold')
        ax2.add_artist(plt.Circle((0,0),0.70,fc='white'))

        ax3 = fig.add_subplot(grid[1, :])
        x = np.arange(len(CAT_ORDER))
        ax3.bar(x - 0.2, b_co2, 0.4, label='Baseline Emissions', color='#d9534f')
        ax3.bar(x + 0.2, g_co2, 0.4, label='Goal Emissions', color='#5cb85c')
        ax3.set_xticks(x)
        ax3.set_xticklabels(CAT_ORDER, rotation=15)
        ax3.set_ylabel("Tonnes CO2e / Year")
        ax3.set_title(f"Scope 3 Impact Gap: {baseline_key} vs {goal_key}", fontweight='bold')
        ax3.legend()
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    plot_transition('1. Monitor 2024 (Current)', '4. Dutch Goal (60:40)', '2a_Transition_DutchGoal.png')
    plot_transition('1. Monitor 2024 (Current)', '5. Amsterdam Goal (70:30)', '2b_Transition_AmsterdamGoal.png')
    plot_transition('1. Monitor 2024 (Current)', '3. EAT-Lancet (Planetary)', '2c_Transition_EAT_Lancet.png')

    # CHART 3: ALL DIETS PLATE (3x3 Grid for 9 Diets)
    print("Generating 3_All_Diets_Plates.png...")
    fig3, axes3 = plt.subplots(3, 3, figsize=(24, 18))
    axes3 = axes3.flatten()
    
    for i, (name, mass_dict) in enumerate(results_mass.items()):
        if i >= 9: break
        ax = axes3[i]
        vals = [mass_dict[c] for c in CAT_ORDER]
        total_mass = sum(vals)
        wedges, texts, autotexts = ax.pie(
            vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, 
            colors=COLORS, textprops={'fontsize': 9, 'weight': 'bold'}
        )
        ax.set_title(f"{name.split('(')[0].strip()}\nTotal: {total_mass:.0f} g/day", 
                    fontsize=12, fontweight='bold', pad=10)
        ax.add_artist(plt.Circle((0,0),0.70,fc='white'))
    
    fig3.legend(CAT_ORDER, loc='lower center', ncol=5, fontsize=10, frameon=True,
               bbox_to_anchor=(0.5, -0.02))
    plt.tight_layout()
    plt.savefig('3_All_Diets_Plates.png', dpi=300, bbox_inches='tight')

    # CHART 4: IMPACT STACK (Total Emissions: Scope 1+2+3)
    print("Generating 4_Impact_Stack.png...")
    fig4, ax4 = plt.subplots(figsize=(16, 9))
    diet_names = list(results_co2.keys())
    diet_labels = [d.split('(')[0].strip() for d in diet_names]
    x4 = np.arange(len(diet_names))
    bottoms = np.zeros(len(diet_names))
    
    for i, cat in enumerate(CAT_ORDER):
        # Total emissions = Scope 1+2 + Scope 3
        values = [results_scope12[d][cat] + results_co2[d][cat] for d in diet_names]
        ax4.bar(x4, values, bottom=bottoms, label=cat, color=COLORS[i], alpha=0.9, edgecolor='white', linewidth=0.5)
        bottoms += np.array(values)
    
    ax4.set_xticks(x4)
    ax4.set_xticklabels(diet_labels, rotation=45, ha='right', fontsize=10)
    ax4.set_ylabel('Total Emissions (tonnes CO2e/year)', fontsize=12, fontweight='bold')
    ax4.set_title('Total Emissions by Category (Scope 1+2+3) - All 9 Diets', fontsize=14, fontweight='bold', pad=15)
    ax4.legend(loc='upper left', ncol=2, fontsize=9, frameon=True)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('4_Impact_Stack.png', dpi=300, bbox_inches='tight')

    # ---------------------------------------------------------
    # PART D: Scope 1+2 vs Scope 3 Comparisons (All 6 Diets)
    # ---------------------------------------------------------
    print("Generating 6_Scope12_vs_Scope3.png and 7_Scope3_Share.png...")
    
    # We already have results_scope12 from engine.aggregate_visual_data()
    scope3_totals = {diet: sum(results_co2[diet].values()) for diet in results_co2}
    scope12_totals = {diet: sum(results_scope12[diet].values()) for diet in results_scope12}
    total_totals = {diet: scope12_totals[diet] + scope3_totals[diet] for diet in results_co2}
    
    # Chart 6: Scope 1+2 (Local) vs Scope 3 (Supply Chain) grouped bars
    fig6, ax6 = plt.subplots(figsize=(16, 8))
    diet_names = list(results_co2.keys())
    diet_labels = [d.split('(')[0].strip() for d in diet_names]
    x6 = np.arange(len(diet_names))
    width = 0.25
    
    scope12_vals = [scope12_totals[d] for d in diet_names]
    scope3_vals = [scope3_totals[d] for d in diet_names]
    total_vals = [total_totals[d] for d in diet_names]
    
    bars1 = ax6.bar(x6 - width, scope12_vals, width, label='Scope 1+2 (Local)', color='#F39C12', alpha=0.9, edgecolor='black', linewidth=0.5)
    bars2 = ax6.bar(x6, scope3_vals, width, label='Scope 3 (Supply Chain)', color='#3498DB', alpha=0.9, edgecolor='black', linewidth=0.5)
    bars3 = ax6.bar(x6 + width, total_vals, width, label='Total (1+2+3)', color='#95A5A6', alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax6.set_xticks(x6)
    ax6.set_xticklabels(diet_labels, rotation=45, ha='right', fontsize=10)
    ax6.set_ylabel('Emissions (tonnes CO2e/year)', fontsize=12, fontweight='bold')
    ax6.set_title('Scope Breakdown Comparison - All 6 Diets', fontsize=14, fontweight='bold', pad=15)
    ax6.legend(loc='upper left', fontsize=10, frameon=True)
    ax6.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('6_Scope12_vs_Scope3.png', dpi=300, bbox_inches='tight')
    
    # Chart 7: Scope Share Analysis (Stacked 100%)
    fig7, ax7 = plt.subplots(figsize=(14, 7))
    scope12_share = [(scope12_totals[d]/total_totals[d]*100) for d in diet_names]
    scope3_share = [(scope3_totals[d]/total_totals[d]*100) for d in diet_names]
    
    bars_s12 = ax7.bar(x6, scope12_share, label='Scope 1+2 (Local)', color='#F39C12', alpha=0.9)
    bars_s3 = ax7.bar(x6, scope3_share, bottom=scope12_share, label='Scope 3 (Supply Chain)', color='#3498DB', alpha=0.9)
    
    # Add percentage labels
    for i, (s12, s3) in enumerate(zip(scope12_share, scope3_share)):
        ax7.text(i, s12/2, f'{s12:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        ax7.text(i, s12 + s3/2, f'{s3:.1f}%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    ax7.set_xticks(x6)
    ax7.set_xticklabels(diet_labels, rotation=45, ha='right', fontsize=10)
    ax7.set_ylabel('Share of Total Emissions (%)', fontsize=12, fontweight='bold')
    ax7.set_title('Scope Distribution Across Diets', fontsize=14, fontweight='bold', pad=15)
    ax7.set_ylim(0, 100)
    ax7.legend(loc='upper right', fontsize=10, frameon=True)
    ax7.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('7_Scope3_Share.png', dpi=300, bbox_inches='tight')
    plt.close('all')

    # Chart 8: Total Emissions Donuts (Scope 1+2+3 breakdown by category - All 9 Diets)
    print("Generating 8_All_Total_Emissions_Donuts.png...")
    
    fig8, axes8 = plt.subplots(3, 3, figsize=(24, 18))
    axes8 = axes8.flatten()
    
    for i, diet_name in enumerate(results_co2.keys()):
        if i >= 9: break
        # Total emissions = Scope 1+2 + Scope 3
        total_values = [results_scope12[diet_name][c] + results_co2[diet_name][c] for c in CAT_ORDER]
        total_emissions = sum(total_values)
        
        wedges, texts, autotexts = axes8[i].pie(
            total_values, 
            labels=None, 
            autopct='%1.0f%%',
            colors=COLORS, 
            startangle=90,
            pctdistance=0.85,
            textprops={'fontsize': 9, 'weight': 'bold'}
        )
        title_text = diet_name.split('(')[0].strip() + f"\\nTotal: {total_emissions:.0f} tonnes CO2e/year (S1+2+3)"
        axes8[i].set_title(title_text, fontsize=12, fontweight='bold', pad=10)
        axes8[i].add_artist(plt.Circle((0,0),0.65,fc='white'))
        center_text = f"{int(total_emissions/1000)}k\\ntonnes"
        axes8[i].text(0, 0, center_text, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Add legend at bottom
    fig8.legend(CAT_ORDER, loc='lower center', ncol=5, fontsize=10, frameon=True,
               bbox_to_anchor=(0.5, -0.02))
    plt.suptitle('Total Emissions (Scope 1+2+3) by Category - All 9 Diets', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('8_All_Total_Emissions_Donuts.png', dpi=300, bbox_inches='tight')

    # Console summary with clarified scope labels
    print("\\n" + "="*80)
    print("SCOPE BREAKDOWN SUMMARY (Tonnes CO2e/Year) - All 9 Diets")
    print("="*80)
    for diet_name in results_co2.keys():
        s12 = scope12_totals[diet_name]
        s3 = scope3_totals[diet_name]
        total = total_totals[diet_name]
        s12_share = (s12 / total * 100.0) if total > 0 else 0.0
        s3_share = (s3 / total * 100.0) if total > 0 else 0.0
        print(diet_name + ":")
        print(f"  Scope 1+2 (Local):      {s12:>10,.0f} tonnes ({s12_share:>5.1f}%)")
        print(f"  Scope 3 (Supply Chain): {s3:>10,.0f} tonnes ({s3_share:>5.1f}%)")
        print(f"  Total (1+2+3):          {total:>10,.0f} tonnes")
        print()
    print("="*80 + "\\n")
    # ---------------------------------------------------------
    # PART B: NEIGHBORHOOD HOTSPOTS (Spatial Analysis)
    # ---------------------------------------------------------
    print("Generating 5_Neighborhood_Hotspots.png...")
    # Run Simulation on Baseline Diet
    df_spatial = engine.run_spatial_simulation(neighborhoods, diets['1. Monitor 2024 (Current)'])
    
    # Sort for visualization
    df_spatial = df_spatial.sort_values('Total_CO2_Tonnes', ascending=True)
    
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    bars = ax5.barh(df_spatial['Neighborhood'], df_spatial['Total_CO2_Tonnes'], color='#d35400')
    ax5.set_xlabel("Total Scope 3 Emissions (Tonnes CO2e/Year)")
    ax5.set_title("Neighborhood Hotspots: Where is the Impact?", fontsize=14, fontweight='bold')
    
    # Annotate bars
    for bar in bars:
        width = bar.get_width()
        ax5.text(width + 1000, bar.get_y() + bar.get_height()/2, 
                 f'{int(width):,}', va='center', fontsize=9)
                 
    plt.tight_layout()
    plt.savefig('5_Neighborhood_Hotspots.png')

    # ---------------------------------------------------------
    # CHART 9: SHARE IN CO2 VS SHARE IN CONSUMPTION (All 9 Diets)
    # ---------------------------------------------------------
    print("Generating 9_CO2_vs_Mass_Share.png...")
    
    fig9, axes = plt.subplots(3, 3, figsize=(24, 18))
    axes = axes.flatten()
    
    for idx, diet_name in enumerate(results_co2.keys()):
        if idx >= 9: break
        ax = axes[idx]
        mass_data = results_mass[diet_name]
        # Total emissions = Scope 1+2 + Scope 3
        co2_data = {c: results_scope12[diet_name][c] + results_co2[diet_name][c] for c in CAT_ORDER}
        
        total_mass = sum(mass_data.values())
        total_co2 = sum(co2_data.values())
        mass_pct = {cat: (mass_data[cat] / total_mass * 100) for cat in CAT_ORDER}
        co2_pct = {cat: (co2_data[cat] / total_co2 * 100) for cat in CAT_ORDER}
        
        # Sort by CO2 impact
        sorted_cats = sorted(CAT_ORDER, key=lambda c: co2_pct[c], reverse=True)
        y_pos = np.arange(len(sorted_cats))
        width = 0.35
        
        bars1 = ax.barh(y_pos - width/2, [co2_pct[c] for c in sorted_cats], width, 
                        label='Share in Total CO2 (S1+2+3)', color='#E74C3C', alpha=0.85)
        bars2 = ax.barh(y_pos + width/2, [mass_pct[c] for c in sorted_cats], width,
                        label='Share in consumption (mass)', color='#3498DB', alpha=0.85)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(sorted_cats, fontsize=9)
        ax.set_xlabel('Percentage (%)', fontsize=10, fontweight='bold')
        title_text = diet_name.split('(')[0].strip() + f"\\nTotal: {total_co2:.0f} tonnes CO2e/year"
        ax.set_title(title_text, fontsize=11, fontweight='bold', pad=10)
        ax.legend(loc='lower right', fontsize=8, frameon=True)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_xlim(0, max(max(co2_pct.values()), max(mass_pct.values())) * 1.1)
    
    plt.suptitle('CO2 Impact vs Mass Consumption - All 9 Diets', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('9_CO2_vs_Mass_Share.png', dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # CHART 10: ENVIRONMENTAL IMPACT BY FOOD TYPE (Monitor Figure 4 Style)
    # ---------------------------------------------------------
    print("Generating 10_Impact_by_Food_Type.png...")
    FOOD_TYPE_MAP = {
        'Red Meat': 'Animal', 'Poultry': 'Animal', 'Fish': 'Animal',
        'Dairy & Eggs': 'Mixed (Dairy/Eggs)',
        'Plant Protein': 'Plant-based', 'Veg & Fruit': 'Plant-based', 'Staples': 'Plant-based',
        'Ultra-Processed': 'Processed'
    }
    
    fig10, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    comparison_diets_4 = ['1. Monitor 2024 (Current)', '4. Dutch Goal (60:40)', 
                          '5. Amsterdam Goal (70:30)', '3. EAT-Lancet (Planetary)']
    
    for idx, diet_name in enumerate(comparison_diets_4):
        ax = axes[idx]
        type_totals = {'Plant-based': 0, 'Animal': 0, 'Mixed (Dairy/Eggs)': 0, 'Processed': 0}
        for cat in CAT_ORDER:
            food_type = FOOD_TYPE_MAP[cat]
            type_totals[food_type] += results_co2[diet_name][cat]
        total = sum(type_totals.values())
        type_pct = {k: (v/total*100) for k, v in type_totals.items()}
        categories = ['Climate\nChange', 'Land Use', 'Water Use']
        plant_vals = [type_pct['Plant-based']] * 3
        animal_vals = [type_pct['Animal']] * 3
        mixed_vals = [type_pct['Mixed (Dairy/Eggs)']] * 3
        processed_vals = [type_pct['Processed']] * 3
        x = np.arange(len(categories))
        width = 0.6
        p1 = ax.bar(x, plant_vals, width, label='Plant-based', color='#2ECC71')
        p2 = ax.bar(x, animal_vals, width, bottom=plant_vals, label='Animal', color='#E74C3C')
        p3 = ax.bar(x, mixed_vals, width, bottom=np.array(plant_vals)+np.array(animal_vals), 
                    label='Mixed (Dairy/Eggs)', color='#F39C12')
        p4 = ax.bar(x, processed_vals, width, 
                    bottom=np.array(plant_vals)+np.array(animal_vals)+np.array(mixed_vals),
                    label='Processed', color='#95A5A6')
        ax.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
        ax.set_title(diet_name.split('(')[0].strip(), fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        for i, rect in enumerate(p1):
            height = rect.get_height()
            if height > 3:
                ax.text(rect.get_x() + rect.get_width()/2., height/2,
                       f'{height:.0f}%', ha='center', va='center', fontsize=9, fontweight='bold')
        for i, rect in enumerate(p2):
            height = rect.get_height()
            bottom = plant_vals[i]
            if height > 3:
                ax.text(rect.get_x() + rect.get_width()/2., bottom + height/2,
                       f'{height:.0f}%', ha='center', va='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig('10_Impact_by_Food_Type.png', dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # CHART 11: CONSUMPTION VS PROTEIN CONTRIBUTION (Monitor Figure 2 Style)
    # ---------------------------------------------------------
    print("Generating 11_Mass_vs_Protein.png...")
    PROTEIN_CONTENT = {
        'Red Meat': 0.20, 'Poultry': 0.25, 'Fish': 0.20, 'Dairy & Eggs': 0.12,
        'Plant Protein': 0.20, 'Staples': 0.10, 'Veg & Fruit': 0.02, 'Ultra-Processed': 0.05
    }
    
    # Use all 6 diets for Chart 11
    comparison_diets_11 = list(diet_names)
    
    fig11, axes = plt.subplots(2, 3, figsize=(22, 14))
    axes = axes.flatten()
    
    for idx, diet_name in enumerate(comparison_diets_11):
        if idx >= 6: break
        ax = axes[idx]
        mass_data = results_mass[diet_name]
        total_mass = sum(mass_data.values())
        protein_data = {cat: mass_data.get(cat, 0) * PROTEIN_CONTENT.get(cat, 0) for cat in CAT_ORDER}
        total_protein = sum(protein_data.values())
        mass_pct = {cat: (mass_data[cat] / total_mass * 100) for cat in CAT_ORDER}
        protein_pct = {cat: (protein_data[cat] / total_protein * 100) for cat in CAT_ORDER}
        sorted_cats = sorted(CAT_ORDER, key=lambda c: protein_pct[c], reverse=True)
        y_pos = np.arange(len(sorted_cats))
        width = 0.35
        bars1 = ax.barh(y_pos - width/2, [mass_pct[c] for c in sorted_cats], width,
                        label='Share in consumption (mass)', color='#3498DB', alpha=0.8)
        bars2 = ax.barh(y_pos + width/2, [protein_pct[c] for c in sorted_cats], width,
                        label='Share in protein intake', color='#2ECC71', alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(sorted_cats, fontsize=10)
        ax.set_xlabel('Percentage (%)', fontsize=11, fontweight='bold')
        ax.set_title(diet_name.split('(')[0].strip(), fontsize=12, fontweight='bold')
        ax.legend(loc='lower right', fontsize=9)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.axvline(x=0, color='black', linewidth=0.8)
        plant_protein = sum([protein_data[c] for c in ['Plant Protein', 'Staples', 'Veg & Fruit']])
        animal_protein = sum([protein_data[c] for c in ['Red Meat', 'Poultry', 'Fish', 'Dairy & Eggs']])
        plant_pct_total = plant_protein / (plant_protein + animal_protein) * 100
        ax.text(0.98, 0.98, f'Plant protein: {plant_pct_total:.0f}%\nAnimal protein: {100-plant_pct_total:.0f}%',
               transform=ax.transAxes, ha='right', va='top', fontsize=10, 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout()
    plt.savefig('11_Mass_vs_Protein.png', dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # NEW: CHANGE OF SYSTEM-WIDE ENVIRONMENTAL IMPACTS
    # Monitor 2024 baseline vs Goal Diets (CO2, Land, Water)
    # ---------------------------------------------------------
    print("Generating 11a_Change_System_Wide_Impacts.png...")
    baseline = '1. Monitor 2024 (Current)'
    targets = ['4. Dutch Goal (60:40)', '5. Amsterdam Goal (70:30)', '3. EAT-Lancet (Planetary)', '2. Schijf van 5 (Guideline)']
    targets = [d for d in targets if d in diet_names]

    if baseline in diet_names and len(targets) > 0:
        # Helper to sum totals
        def totals_for(dname):
            tot_co2 = sum(results_scope12[dname].values()) + sum(results_co2[dname].values())
            tot_land = sum(results_land[dname].values())
            tot_water = sum(results_water[dname].values())
            return tot_co2, tot_land, tot_water

        b_co2, b_land, b_water = totals_for(baseline)

        # Compute percent change for each target diet
        changes = []  # list of dicts {diet, co2_pct, land_pct, water_pct}
        for d in targets:
            t_co2, t_land, t_water = totals_for(d)
            co2_pct = (t_co2 - b_co2) / b_co2 * 100 if b_co2 else 0
            land_pct = (t_land - b_land) / b_land * 100 if b_land else 0
            water_pct = (t_water - b_water) / b_water * 100 if b_water else 0
            changes.append({
                'diet': d.split('(')[0].strip(),
                'co2': co2_pct,
                'land': land_pct,
                'water': water_pct
            })

        # Plot style inspired by ES&T system-wide impacts figure
        metrics = ['GHG (CO2e)', 'Land', 'Water']
        fig11a, axes = plt.subplots(len(metrics), 1, figsize=(10, 8), sharex=True)
        colors_m = ['#E74C3C', '#2ECC71', '#3498DB']

        # X-range symmetrical around zero for clarity
        # Determine dynamic limits from data (pad by 5%)
        all_vals = []
        for c in changes:
            all_vals.extend([c['co2'], c['land'], c['water']])
        xlim = max(20, min(60, max(abs(v) for v in all_vals) + 5)) if all_vals else 30

        for i, metric in enumerate(metrics):
            ax = axes[i]
            vals = [ch['co2'] if metric.startswith('GHG') else ch['land'] if metric == 'Land' else ch['water'] for ch in changes]
            y = np.arange(len(changes))
            ax.barh(y, vals, color=colors_m[i], alpha=0.85)
            ax.set_yticks(y)
            ax.set_yticklabels([ch['diet'] for ch in changes], fontsize=10)
            ax.set_xlim(-xlim, xlim)
            ax.axvline(0, color='black', linewidth=1)
            ax.set_xlabel('% change vs Monitor 2024', fontsize=11, fontweight='bold')
            ax.set_title(metric, fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            for yi, v in enumerate(vals):
                if abs(v) > 1:
                    ax.text(v + (2 if v>=0 else -2), yi, f'{v:+.1f}%', va='center', ha='left' if v>=0 else 'right', fontsize=9)

        plt.suptitle('Change of System-Wide Environmental Impacts\nMonitor 2024 baseline vs Goal Diets', fontsize=14, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.savefig('11a_Change_System_Wide_Impacts.png', dpi=300, bbox_inches='tight')
        plt.close()

    # ---------------------------------------------------------
    # NEW: ALL DIETS VS GOAL DIETS - SCOPE BREAKDOWN
    # Compares all available diets (Monitor 2024, Metropolitan, etc) to 4 goal diets
    # Scope 1+2 = Local (production + retail + waste)
    # Scope 3 = Supply Chain (indirect emissions through consumption)
    # ---------------------------------------------------------
    print("Generating 11b_Amsterdam_Monitor_vs_Goals_Scope.png...")
    # Show Monitor 2024 as primary baseline, plus other important diets and goals
    all_comparison_diets = ['1. Monitor 2024 (Current)', '6. Metropolitan (High Risk)', 
                           '2. Schijf van 5 (Guideline)', '3. EAT-Lancet (Planetary)', 
                           '4. Dutch Goal (60:40)', '5. Amsterdam Goal (70:30)']
    available_diets = [d for d in all_comparison_diets if d in diet_names]
    
    if len(available_diets) >= 2:
        # Create grid: 2 rows for all 6 diets
        n_cols = min(3, len(available_diets))
        n_rows = int(np.ceil(len(available_diets) / n_cols))
        fig11b, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
        axes = np.array(axes).reshape(-1) if len(available_diets) > 1 else np.array([axes])
        
        for idx, diet_name in enumerate(available_diets):
            ax = axes[idx]
            scope12_data = results_scope12[diet_name]
            scope3_data = results_co2[diet_name]  # Scope 3 = supply chain indirect emissions
            total_data = {cat: scope12_data[cat] + scope3_data[cat] for cat in CAT_ORDER}
            sorted_cats = sorted(CAT_ORDER, key=lambda c: total_data[c], reverse=True)[:8]
            
            y_pos = np.arange(len(sorted_cats))
            scope12_vals = [scope12_data[c] / 1000 for c in sorted_cats]
            scope3_vals = [scope3_data[c] / 1000 for c in sorted_cats]
            
            bars1 = ax.barh(y_pos, scope12_vals, 0.7, label='Scope 1+2 (Local)', color='#F39C12', alpha=0.9)
            bars2 = ax.barh(y_pos, scope3_vals, 0.7, left=scope12_vals, label='Scope 3 (Supply Chain)', color='#3498DB', alpha=0.9)
            
            ax.set_yticks(y_pos)
            ax.set_yticklabels(sorted_cats, fontsize=9)
            ax.set_xlabel('Emissions (kton CO2e/year)', fontsize=10, fontweight='bold')
            diet_label = diet_name.split('(')[0].strip()
            for prefix in ['1. ', '2. ', '3. ', '4. ', '5. ', '6. ']:
                diet_label = diet_label.replace(prefix, '')
            total_ktons = sum(total_data.values())/1000
            scope12_pct = sum(scope12_vals)*100/total_ktons if total_ktons > 0 else 0
            ax.set_title(f'{diet_label}\nTotal: {total_ktons:.0f} kton | S1+2: {scope12_pct:.1f}%', fontsize=11, fontweight='bold')
            if idx == 0:
                ax.legend(loc='lower right', fontsize=8)
            ax.grid(axis='x', alpha=0.3)
        
        # Hide extra subplots
        for idx in range(len(available_diets), len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle('Amsterdam Food System: All Diets vs Goal Diets - Scope 1+2 vs Supply Chain Emissions', fontsize=13, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig('11b_Amsterdam_Monitor_vs_Goals_Scope.png', dpi=300, bbox_inches='tight')
        plt.close()

    # ---------------------------------------------------------
    # NEW: MULTI-RESOURCE IMPACT METRICS - ALL DIETS VS GOALS
    # Shows three independent environmental footprints:
    # - CO2: Scope 1+2+3 combined (complete emissions)
    # - Land Use: Agricultural land footprint (separate metric)
    # - Water: Blue water consumption footprint (separate metric)
    # ---------------------------------------------------------
    print("Generating 11c_Amsterdam_Multi_Resource_Impact.png...")
    # Compare all diets to goal diets
    all_diets_multi = ['1. Monitor 2024 (Current)', '6. Metropolitan (High Risk)',
                       '2. Schijf van 5 (Guideline)', '3. EAT-Lancet (Planetary)', 
                       '4. Dutch Goal (60:40)', '5. Amsterdam Goal (70:30)']
    available_diets_multi = [d for d in all_diets_multi if d in diet_names]
    
    # Food type aggregation mapping
    FOOD_TYPE_MAP = {
        'Red Meat': 'Animal Products', 'Poultry': 'Animal Products', 
        'Dairy & Eggs': 'Animal Products', 'Fish': 'Animal Products',
        'Plant Protein': 'Plant-Based', 'Staples': 'Plant-Based', 
        'Veg & Fruit': 'Plant-Based',
        'Ultra-Processed': 'Processed/Other'
    }
    
    if len(available_diets_multi) >= 2:
        n_cols = 3
        n_rows = int(np.ceil(len(available_diets_multi) / n_cols))
        fig11c, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5*n_rows))
        axes = np.array(axes).reshape(-1) if len(available_diets_multi) > 1 else np.array([axes])
        
        for idx, diet_name in enumerate(available_diets_multi):
            ax = axes[idx]
            scope12_data = results_scope12[diet_name]
            scope3_data = results_co2[diet_name]  # Scope 3 = supply chain emissions
            land_data = results_land[diet_name]   # Land use (separate metric)
            water_data = results_water[diet_name] # Water footprint (separate metric)
            
            # Aggregate to food types
            type_co2_total = {}
            type_land = {}
            type_water = {}
            
            for cat in CAT_ORDER:
                food_type = FOOD_TYPE_MAP.get(cat, 'Processed/Other')
                type_co2_total[food_type] = type_co2_total.get(food_type, 0) + (scope12_data[cat] + scope3_data[cat])
                type_land[food_type] = type_land.get(food_type, 0) + land_data[cat]
                type_water[food_type] = type_water.get(food_type, 0) + water_data[cat]
            
            # Calculate totals and percentages
            total_co2 = sum(type_co2_total.values())
            total_land = sum(type_land.values())
            total_water = sum(type_water.values())
            
            type_order = ['Animal Products', 'Plant-Based', 'Processed/Other']
            co2_pcts = [100 * type_co2_total.get(t, 0) / total_co2 if total_co2 > 0 else 0 for t in type_order]
            land_pcts = [100 * type_land.get(t, 0) / total_land if total_land > 0 else 0 for t in type_order]
            water_pcts = [100 * type_water.get(t, 0) / total_water if total_water > 0 else 0 for t in type_order]
            
            colors_type = ['#E74C3C', '#2ECC71', '#95A5A6']
            diet_label = diet_name.split('(')[0].strip()
            for prefix in ['1. ', '2. ', '3. ', '4. ', '5. ', '6. ']:
                diet_label = diet_label.replace(prefix, '')
            
            # CO2 bar chart
            ax.barh([0], [sum(co2_pcts)], left=0, color='white', edgecolor='none')
            x_pos = 0
            for i, pct in enumerate(co2_pcts):
                ax.barh([0], [pct], left=x_pos, color=colors_type[i], alpha=0.85)
                if pct > 5:
                    ax.text(x_pos + pct/2, 0, f'{pct:.0f}%', ha='center', va='center', 
                           fontsize=9, color='white', fontweight='bold')
                x_pos += pct
            
            ax.set_ylim(-0.5, 0.5)
            ax.set_xlim(0, 100)
            ax.set_yticks([])
            ax.set_xlabel('')
            ax.set_title(f'{diet_label}', fontsize=11, fontweight='bold', pad=10)
            
            # Add values below chart
            co2_text = f'CO2: {total_co2/1000:.0f} kt'
            land_text = f'Land: {total_land/1e6:.1f} km²'
            water_text = f'Water: {total_water/1e6:.1f} ML'
            ax.text(0.5, -0.35, f'{co2_text}\\n{land_text}\\n{water_text}', 
                   ha='center', va='top', fontsize=9, transform=ax.transData, fontweight='bold')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
        
        # Hide extra subplots
        for idx in range(len(available_diets_multi), len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle('Amsterdam Food System: Multi-Resource Footprints (CO2, Land, Water) - All Diets vs Goals\\nColor: Red=Animal | Green=Plant | Gray=Processed', 
                    fontsize=12, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig('11c_Amsterdam_Multi_Resource_Impact.png', dpi=300, bbox_inches='tight')
        plt.close()

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # CHART 12: ALL DIETS VS GOAL REFERENCE
    # Shows total emissions (Scope 1+2+3) compared to Schijf van 5 reference
    # Includes Monitor 2024, other diets, and all goal diets
    # ---------------------------------------------------------
    print("Generating 12_Emissions_vs_Reference.png...")
    reference_diet = '2. Schijf van 5 (Guideline)' if '2. Schijf van 5 (Guideline)' in diet_names else next((d for d in diet_names if 'Schijf' in d or 'EAT' in d), diet_names[0])
    # Show all diets with emphasis on goals
    all_diets_chart12 = ['1. Monitor 2024 (Current)', '6. Metropolitan (High Risk)',
                         '2. Schijf van 5 (Guideline)', '3. EAT-Lancet (Planetary)', 
                         '4. Dutch Goal (60:40)', '5. Amsterdam Goal (70:30)']
    comparison_diets_ref = [d for d in all_diets_chart12 if d in diet_names]
    
    fig12, ax = plt.subplots(figsize=(14, 8))
    ref_emissions = {cat: results_scope12[reference_diet][cat] + results_co2[reference_diet][cat] for cat in CAT_ORDER}
    sorted_cats = sorted(CAT_ORDER, key=lambda c: ref_emissions[c], reverse=True)
    
    y_pos = np.arange(len(sorted_cats))
    width = 0.13
    colors_diets = ['#3498DB', '#E67E22', '#2ECC71', '#9B59B6', '#E74C3C', '#1ABC9C']
    
    for idx, diet_name in enumerate(comparison_diets_ref[:6]):
        diet_emissions = {cat: results_scope12[diet_name][cat] + results_co2[diet_name][cat] for cat in CAT_ORDER}
        pct_of_ref = [(diet_emissions[cat] / ref_emissions[cat] * 100) if ref_emissions[cat] > 0 else 0 for cat in sorted_cats]
        offset = (idx - len(comparison_diets_ref[:6])/2 + 0.5) * width
        bars = ax.barh(y_pos + offset, pct_of_ref, width, 
                      label=diet_name.split('(')[0].strip()[:20], 
                      color=colors_diets[idx % len(colors_diets)], alpha=0.85)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_cats, fontsize=10)
    ax.set_xlabel('Total emissions versus Schijf van 5 reference (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Total Food System Emissions (Scope 1+2+3) - All Diets vs Schijf van 5 Reference', 
                fontsize=13, fontweight='bold', pad=20)
    ax.axvline(x=100, color='black', linewidth=2.5, linestyle='--', label='Schijf van 5 (100%)')
    ax.legend(loc='lower right', fontsize=9, ncol=2)
    ax.grid(axis='x', alpha=0.3)
    ax.set_xlim(0, 300)
    
    total_ref = sum(ref_emissions.values())
    info_text = f'Reference Diet (Schijf van 5):\nTotal: {total_ref/1000:.0f} kton CO2e\n(Scope 1+2 + Scope 3 supply chain)'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, ha='left', va='top', fontsize=10, 
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('12_Emissions_vs_Reference.png', dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # CHART 13: SYSTEM-WIDE IMPACT CHANGE FROM MONITOR 2024 TO GOAL DIETS
    # ---------------------------------------------------------
    print("Generating 13_System_Wide_Impact_Change.png...")
    baseline_diet = '1. Monitor 2024 (Current)'
    goal_comparison_diets = ['2. Schijf van 5 (Guideline)', '3. EAT-Lancet (Planetary)', 
                            '4. Dutch Goal (60:40)', '5. Amsterdam Goal (70:30)']
    goal_comparison_diets = [d for d in goal_comparison_diets if d in diet_names]
    
    if baseline_diet in diet_names and len(goal_comparison_diets) >= 2:
        # Calculate baseline total impacts
        baseline_ghg = sum(results_scope12[baseline_diet].values()) + sum(results_co2[baseline_diet].values())
        baseline_water = sum(results_water[baseline_diet].values())
        baseline_land = sum(results_land[baseline_diet].values())
        
        fig13, ax = plt.subplots(figsize=(14, 8))
        
        x_pos = np.arange(len(goal_comparison_diets))
        width = 0.25
        
        ghg_changes = []
        water_changes = []
        land_changes = []
        
        for diet_name in goal_comparison_diets:
            goal_ghg = sum(results_scope12[diet_name].values()) + sum(results_co2[diet_name].values())
            goal_water = sum(results_water[diet_name].values())
            goal_land = sum(results_land[diet_name].values())
            
            ghg_pct_change = ((goal_ghg - baseline_ghg) / baseline_ghg) * 100
            water_pct_change = ((goal_water - baseline_water) / baseline_water) * 100
            land_pct_change = ((goal_land - baseline_land) / baseline_land) * 100
            
            ghg_changes.append(ghg_pct_change)
            water_changes.append(water_pct_change)
            land_changes.append(land_pct_change)
        
        # Create bars
        bars1 = ax.bar(x_pos - width, ghg_changes, width, label='GHG Emissions', color='#C0392B', alpha=0.85)
        bars2 = ax.bar(x_pos, water_changes, width, label='Water Use', color='#3498DB', alpha=0.85)
        bars3 = ax.bar(x_pos + width, land_changes, width, label='Land Use', color='#27AE60', alpha=0.85)
        
        # Add zero line
        ax.axhline(y=0, color='black', linewidth=2, linestyle='-')
        
        # Formatting
        ax.set_ylabel('% Change from Monitor 2024', fontsize=12, fontweight='bold')
        ax.set_title('System-Wide Environmental Impact Change:\\nMonitor 2024 vs Goal Diets', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels([d.split('(')[0].strip().replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '') 
                           for d in goal_comparison_diets], fontsize=11)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(min(min(ghg_changes), min(water_changes), min(land_changes)) - 5, 
                    max(max(ghg_changes), max(water_changes), max(land_changes)) + 5)
        
        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%',
                       ha='center', va='bottom' if height > 0 else 'top', fontsize=9, fontweight='bold')
        
        # Add legend text box with baseline values
        textstr = f'Monitor 2024 Baseline:\\nGHG: {baseline_ghg/1000:.0f} kton CO2e\\nWater: {baseline_water/1e6:.1f} ML\\nLand: {baseline_land/1e6:.2f} km²'
        ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=10,
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('13_System_Wide_Impact_Change.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Chart 13 saved: 13_System_Wide_Impact_Change.png")

    # ---------------------------------------------------------
    # PART C: CONSOLE REPORT
    # ---------------------------------------------------------
    print("\n" + "="*90)
    print(f"{'MASTER SCOPE 3 TONNAGE REPORT':^90}")
    print("="*90)
    
    short_names = ["1.Bsline", "2.Metro", "3.Meta", "4.DuGoal", "5.AmGoal", "6.EAT"]
    row_fmt = "{:<22}" + "{:>11}" * len(short_names)
    print(row_fmt.format("CATEGORY", *short_names))
    print("-" * 100)
    
    for cat in CAT_ORDER:
        vals = [results_co2[d][cat] for d in diet_names]
        f_vals = [f"{v:,.0f}" for v in vals]
        print(row_fmt.format(cat, *f_vals))
        
    print("-" * 100)
    totals = [sum(results_co2[d].values()) for d in diet_names]
    f_totals = [f"{t:,.0f}" for t in totals]
    print(row_fmt.format("TOTAL (Tonnes)", *f_totals))
    
    base = totals[0]
    reds = [f"{(t-base)/base*100:+.1f}%" for t in totals]
    print(row_fmt.format("Change vs Baseline", *reds))
    print("="*90)
    
    # Hotspot Report
    print("\n--- NEIGHBORHOOD HOTSPOT ANALYSIS (BASELINE WITH EDUCATION MODIFIERS) ---")
    print(df_spatial[['Neighborhood', 'Population', 'Education_Pct', 'Meat_Modifier', 'Total_CO2_Tonnes']].sort_values('Total_CO2_Tonnes', ascending=False).to_string(index=False))

if __name__ == "__main__":
    run_full_analysis()