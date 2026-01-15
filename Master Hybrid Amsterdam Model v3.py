"""
Master Hybrid Amsterdam Model v3
Advanced Food Systems Scope 3 Emissions Analysis

This version extends the base model with enhanced features:
- 7 diet scenarios including empirical Amsterdam Monitor 2024 data
- Education-based meat consumption modifiers (behavioral factors)
- Enhanced visualization suite with table outputs
- Refined spatial analysis accounting for education levels
- Multi-dimensional impact assessment (CO2, land, water)

New in v3:
- Integration of Amsterdam Monitor 2024 empirical diet data (48% plant protein)
- Education level as behavioral modifier (high education = lower meat preference)
- Composite beta factors (volume effect + plant preference effect)
- Table visualization export (6_Table_Tonnage.png)
- Extended color palette and visual mapping

Outputs:
- 1_Nexus_Analysis.png: Multi-resource impact comparison
- 2a/b/c_Transition_*.png: Baseline to goal state transitions
- 3_All_Diets_Plates.png: 7-way diet composition comparison
- 4_Impact_Stack.png: Stacked emissions by category
- 5_Neighborhood_Hotspots.png: Spatial distribution with behavioral modifiers
- 6_Table_Tonnage.png: Tabular emissions data
- Console: Comprehensive tonnage report

Author: Challenge Based Project Team
Date: January 2026
Version: 3.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# ==========================================
# 1. CONFIGURATION
# ==========================================
class HybridModelConfig:
    """
    Configuration parameters for the hybrid food systems model v3.
    
    Attributes:
        NATIONAL_AVG_INCOME (int): Netherlands average household income (EUR/year)
        SCALING_C1 (float): Valencia volume scaling coefficient
        SCALING_C2 (float): Valencia income elasticity exponent
        WASTE_FACTOR (float): Supply chain loss multiplier (1.15 = 15% waste)
        POPULATION_TOTAL (int): Total Amsterdam metropolitan population
    """
    
    def __init__(self):
        self.NATIONAL_AVG_INCOME = 32000
        self.SCALING_C1 = 0.8
        self.SCALING_C2 = 0.2
        self.WASTE_FACTOR = 1.15   # Supply chain loss
        self.POPULATION_TOTAL = 882000

# --- VISUALIZATION MAPPING ---
# Extended mapping including additional food items (Lamb, Rice, Pasta, Bread, Drinks)
# Maps granular food items to 8 aggregated categories for visualization clarity
VISUAL_MAPPING = {
    'Beef': 'Red Meat', 'Pork': 'Red Meat', 'Lamb': 'Red Meat',
    'Chicken': 'Poultry', 'Poultry': 'Poultry',
    'Cheese': 'Dairy & Eggs', 'Milk': 'Dairy & Eggs', 'Eggs': 'Dairy & Eggs', 'Dairy': 'Dairy & Eggs',
    'Fish': 'Fish',
    'Pulses': 'Plant Protein', 'Nuts': 'Plant Protein', 'Meat_Subs': 'Plant Protein', 'Plant Protein': 'Plant Protein',
    'Grains': 'Staples', 'Potatoes': 'Staples', 'Staples': 'Staples', 'Rice': 'Staples', 'Pasta': 'Staples', 'Bread': 'Staples',
    'Vegetables': 'Veg & Fruit', 'Fruits': 'Veg & Fruit', 'Veg & Fruit': 'Veg & Fruit',
    'Sugar': 'Ultra-Processed', 'Processed': 'Ultra-Processed', 'Ultra-Processed': 'Ultra-Processed', 'Drinks': 'Ultra-Processed'
}

# --- COLOR PALETTE ---
# Consistent category ordering for all visualizations
CAT_ORDER = ['Red Meat', 'Poultry', 'Dairy & Eggs', 'Fish', 'Plant Protein', 'Staples', 'Veg & Fruit', 'Ultra-Processed']

# Color scheme: gradient from high-impact (dark red) to low-impact (light green)
COLORS = ['#8B0000', '#F08080', '#FFD700', '#4682B4', '#2E8B57', '#DEB887', '#90EE90', '#A9A9A9']

# Color mapping dictionary for easy lookup
COLOR_MAP = dict(zip(CAT_ORDER, COLORS))

# ==========================================
# 2. DATA INGESTION
# ==========================================
def load_impact_factors():
    """ 
    Load comprehensive Scope 3 environmental impact factors.
    
    Data sources:
    - CO2 factors: Trans-boundary LCA from Blonk Consultants
    - Land use: Global agricultural land footprint (Poore & Nemecek 2018)
    - Water: Blue water consumption (WaterFootprint Network)
    
    Returns:
        pd.DataFrame: Impact factors indexed by food item with columns:
            - co2: kg CO2e per kg product
            - land: m² per kg product
            - water: liters per kg product
    """
    factors = {
        'Beef':      {'co2': 28.0, 'land': 25.0, 'water': 15400, 'scope12': 0.5},
        'Pork':      {'co2': 5.0,  'land': 9.0,  'water': 6000,  'scope12': 0.4},
        'Chicken':   {'co2': 3.5,  'land': 7.0,  'water': 4300,  'scope12': 0.3},
        'Cheese':    {'co2': 10.0, 'land': 12.0, 'water': 5000,  'scope12': 0.2},
        'Milk':      {'co2': 1.3,  'land': 1.5,  'water': 1000,  'scope12': 0.1},
        'Fish':      {'co2': 3.5,  'land': 0.5,  'water': 2000,  'scope12': 0.4},
        'Eggs':      {'co2': 2.2,  'land': 2.5,  'water': 3300,  'scope12': 0.2},
        'Pulses':    {'co2': 0.9,  'land': 3.0,  'water': 4000,  'scope12': 0.1},
        'Nuts':      {'co2': 0.3,  'land': 2.5,  'water': 9000,  'scope12': 0.05},
        'Meat_Subs': {'co2': 2.5,  'land': 3.0,  'water': 200,   'scope12': 0.1}, 
        'Grains':    {'co2': 1.1,  'land': 1.8,  'water': 1600,  'scope12': 0.05},
        'Vegetables':{'co2': 0.6,  'land': 0.5,  'water': 320,   'scope12': 0.05},
        'Fruits':    {'co2': 0.7,  'land': 0.6,  'water': 960,   'scope12': 0.05},
        'Potatoes':  {'co2': 0.4,  'land': 0.3,  'water': 290,   'scope12': 0.05},
        'Sugar':     {'co2': 2.0,  'land': 1.5,  'water': 200,   'scope12': 0.05},
        'Processed': {'co2': 2.5,  'land': 1.5,  'water': 300,   'scope12': 0.1}
    }
    return pd.DataFrame.from_dict(factors, orient='index')

def load_diet_profiles():
    """ 
    Load 7 dietary scenario profiles for comprehensive comparison.
    
    Diet Scenarios:
    1. Monitor 2024 (Current): Empirical data from Amsterdam Food Monitor 2024
       - 48% plant protein / 52% animal protein
       - Reflects actual consumption patterns with higher plant-based uptake
       - Lower meat than national average (-20%)
       
    2. Amsterdam Theoretical: Pre-Monitor baseline estimate
       - Used for historical comparison
       
    3. Metropolitan (High Risk): Western high-meat diet
       - High red meat, processed foods, low vegetables
       - Represents unhealthy urban consumption pattern
       
    4. Metabolic Balance: Animal-based low-carb diet
       - High meat/fish/eggs, minimal grains
       - Keto/paleo style consumption
       
    5. Dutch Goal (60:40): National protein transition target
       - 60% plant protein, 40% animal protein
       - Moderate reduction pathway
       
    6. Amsterdam Goal (70:30): City protein transition target
       - 70% plant protein, 30% animal protein
       - Ambitious reduction pathway
       
    7. EAT-Lancet (Planetary): Global sustainability benchmark
       - Planetary health diet for 10 billion people
       - Maximum environmental sustainability
    
    Returns:
        dict: Dictionary mapping diet names to consumption profiles (grams/day per food item)
    """
    diets = {
        '1. Monitor 2024 (Current)': {
            'Beef': 10, 'Pork': 15, 'Chicken': 25, 'Cheese': 35, 'Milk': 220, 
            'Fish': 22, 'Eggs': 28, 'Pulses': 15, 'Nuts': 15, 'Meat_Subs': 20, 
            'Grains': 230, 'Vegetables': 160, 'Fruits': 145, 'Potatoes': 45,
            'Sugar': 35, 'Processed': 140 
        },
        '2. Amsterdam Theoretical': {
            'Beef': 12, 'Pork': 20, 'Chicken': 28, 'Cheese': 40, 'Milk': 260,
            'Fish': 10, 'Eggs': 25, 'Pulses': 8, 'Nuts': 10, 'Meat_Subs': 15,
            'Grains': 220, 'Vegetables': 150, 'Fruits': 130, 'Potatoes': 50,
            'Sugar': 40, 'Processed': 150 
        },
        '3. Metropolitan (High Risk)': {
            'Beef': 45, 'Pork': 25, 'Chicken': 60, 'Cheese': 50, 'Milk': 200,
            'Fish': 15, 'Eggs': 30, 'Pulses': 5, 'Nuts': 5, 'Meat_Subs': 5,
            'Grains': 180, 'Vegetables': 110, 'Fruits': 100, 'Potatoes': 80,
            'Sugar': 80, 'Processed': 200 
        },
        '4. Metabolic Balance': {
            'Beef': 60, 'Pork': 40, 'Chicken': 80, 'Cheese': 50, 'Milk': 50,
            'Fish': 40, 'Eggs': 50, 'Pulses': 10, 'Nuts': 20, 'Meat_Subs': 0,
            'Grains': 50, 'Vegetables': 200, 'Fruits': 100, 'Potatoes': 0,
            'Sugar': 5, 'Processed': 10
        },
        '5. Dutch Goal (60:40)': {
            'Beef': 15, 'Pork': 15, 'Chicken': 25, 'Cheese': 35, 'Milk': 250,
            'Fish': 15, 'Eggs': 20, 'Pulses': 40, 'Nuts': 20, 'Meat_Subs': 25,
            'Grains': 225, 'Vegetables': 200, 'Fruits': 180, 'Potatoes': 90,
            'Sugar': 30, 'Processed': 80
        },
        '6. Amsterdam Goal (70:30)': {
            'Beef': 5, 'Pork': 5, 'Chicken': 10, 'Cheese': 20, 'Milk': 100,
            'Fish': 15, 'Eggs': 15, 'Pulses': 80, 'Nuts': 40, 'Meat_Subs': 40,
            'Grains': 250, 'Vegetables': 250, 'Fruits': 200, 'Potatoes': 80,
            'Sugar': 20, 'Processed': 50
        },
        '7. EAT-Lancet (Planetary)': {
            'Beef': 7, 'Pork': 7, 'Chicken': 29, 'Cheese': 0, 'Milk': 250,
            'Fish': 28, 'Eggs': 13, 'Pulses': 75, 'Nuts': 50, 'Meat_Subs': 0,
            'Grains': 232, 'Vegetables': 300, 'Fruits': 200, 'Potatoes': 50,
            'Sugar': 30, 'Processed': 0
        },
        '8. Schijf van 5 (Guideline)': {
            'Beef': 10, 'Pork': 10, 'Chicken': 25, 'Cheese': 30, 'Milk': 250,
            'Fish': 25, 'Eggs': 20, 'Pulses': 30, 'Nuts': 25, 'Meat_Subs': 20,
            'Grains': 240, 'Vegetables': 250, 'Fruits': 200, 'Potatoes': 70,
            'Sugar': 25, 'Processed': 60
        },
        '9. Mediterranean Diet': {
            'Beef': 8, 'Pork': 8, 'Chicken': 20, 'Cheese': 30, 'Milk': 200,
            'Fish': 35, 'Eggs': 18, 'Pulses': 60, 'Nuts': 30, 'Meat_Subs': 10,
            'Grains': 240, 'Vegetables': 300, 'Fruits': 220, 'Potatoes': 60,
            'Sugar': 20, 'Processed': 50
        }
    }
    return diets

def load_neighborhood_data():
    """ 
    Load Amsterdam neighborhood socio-economic and behavioral data.
    
    NEW IN V3: Added 'High_Education_Pct' column
    
    Behavioral Insight from Monitor:
    - High education neighborhoods (Zuid, Centrum) eat 52% plant protein
    - Low education neighborhoods eat 39% plant protein
    - This creates a counter-intuitive pattern: wealthy areas have LOWER meat 
      consumption despite higher overall food expenditure
    
    Key Neighborhoods:
    - Zuid & Centrum: Highest income + education = Lower meat intensity
    - Nieuw-West & Zuidoost: Lower income = Higher meat preference
    - Noord & Oost: Middle-income mixed patterns
    
    Returns:
        pd.DataFrame: Neighborhood data with columns:
            - Neighborhood: District name
            - Population: Resident count (2024)
            - Avg_Income: Average household income (EUR/year)
            - High_Education_Pct: Fraction with bachelor degree or higher
    """
    return pd.DataFrame({
        'Neighborhood': ['Centrum', 'Zuid', 'West', 'Noord', 'Zuidoost', 'Nieuw-West', 'Oost'],
        'Population': [87000, 145000, 145000, 99000, 89000, 160000, 135000],
        'Avg_Income': [48000, 56000, 34000, 29000, 24000, 26000, 36000],
        'High_Education_Pct': [0.65, 0.70, 0.60, 0.40, 0.30, 0.35, 0.55] 
    })

# ==========================================
# 3. CORE ENGINE
# ==========================================
class Scope3Engine:
    """
    Advanced Scope 3 emissions calculator with behavioral modifiers.
    
    NEW IN V3: Composite beta calculation
    - Volume Beta: Income-driven total consumption scaling
    - Meat/Plant Modifiers: Education-driven dietary preferences
    
    This creates a two-factor model:
    1. Wealthier neighborhoods buy MORE food overall (volume effect)
    2. Higher education neighborhoods choose LESS meat (preference effect)
    
    Attributes:
        cfg (HybridModelConfig): Model configuration parameters
        factors (pd.DataFrame): Environmental impact factors database
    """
    
    def __init__(self, config):
        """
        Initialize the enhanced Scope3 calculation engine.
        
        Args:
            config (HybridModelConfig): Configuration object
        """
        self.cfg = config
        self.factors = load_impact_factors()

    # --- 3A. REFINED BETA FACTOR (The Monitor Logic) ---
    def calculate_beta(self, row):
        """
        Calculate composite consumption scaling factors.
        
        NEW IN V3: Returns THREE values instead of one
        
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

    # --- 3B. Raw Impact Calculation (Per Capita Per Day) ---
    def calculate_raw_impact(self, diet_profile):
        """
        Calculate total environmental impact for a diet profile.
        
        Args:
            diet_profile (dict): Food items and daily consumption (grams)
            
        Returns:
            dict: Daily per-capita impacts (co2, land, water)
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

    def aggregate_visual_data(self, diet_profile):
        """ Aggregates diet into 8 Visual Categories """
        agg_mass = {k: 0.0 for k in CAT_ORDER}
        agg_co2 = {k: 0.0 for k in CAT_ORDER}
        
        for food, grams in diet_profile.items():
            if food not in self.factors.index: continue
            category = VISUAL_MAPPING.get(food, 'Other')
            if category not in agg_mass: continue
            
            kg_consumed_yr = (grams / 1000) * 365
            kg_produced_yr = kg_consumed_yr * self.cfg.WASTE_FACTOR
            f = self.factors.loc[food]
            co2_tonnes = (kg_produced_yr * f['co2'] * self.cfg.POPULATION_TOTAL) / 1000
            
            agg_mass[category] += grams
            agg_co2[category] += co2_tonnes
        return agg_mass, agg_co2

    def run_spatial_simulation(self, neighborhoods, diet_profile):
        results = []
        base_impact = self.calculate_raw_impact(diet_profile)
        for _, row in neighborhoods.iterrows():
            vol_beta, meat_mod, plant_mod = self.calculate_beta(row)
            local_scaling = (0.4 * meat_mod + 0.1 * plant_mod + 0.5 * 1.0) * vol_beta
            local_co2_per_capita = base_impact['co2'] * local_scaling
            total_tonnes = (local_co2_per_capita * 365 * row['Population']) / 1000
            
            results.append({
                'Neighborhood': row['Neighborhood'],
                'Population': row['Population'],
                'Total_CO2_Tonnes': total_tonnes
            })
        return pd.DataFrame(results)

# ==========================================
# 4. VISUALIZATION SUITE
# ==========================================
def run_full_analysis():
    cfg = HybridModelConfig()
    engine = Scope3Engine(cfg)
    diets = load_diet_profiles()
    neighborhoods = load_neighborhood_data()
    
    print("Calculating impacts for all diets...")
    results_mass = {}
    results_co2 = {}
    total_footprints = {}
    
    for name, profile in diets.items():
        mass, co2 = engine.aggregate_visual_data(profile)
        results_mass[name] = mass
        results_co2[name] = co2
        total_footprints[name] = sum(co2.values())

    # 1. NEXUS COMPARISON
    print("Generating 1_Nexus_Analysis.png...")
    nexus_data = []
    for name, profile in diets.items():
        res = engine.calculate_raw_impact(profile)
        res['Diet'] = name
        nexus_data.append(res)
    df_nexus = pd.DataFrame(nexus_data).set_index('Diet').sort_values('co2', ascending=False)
    
    fig1, axes = plt.subplots(1, 3, figsize=(20, 6))
    df_nexus['co2'].plot(kind='bar', ax=axes[0], color='#E74C3C', title='Carbon Footprint (kg CO2e/day)')
    df_nexus['land'].plot(kind='bar', ax=axes[1], color='#2ECC71', title='Land Use (m2/day)')
    df_nexus['water'].plot(kind='bar', ax=axes[2], color='#3498DB', title='Water Use (L/day)')
    plt.tight_layout()
    plt.savefig('1_Nexus_Analysis.png')

    # 2. ALL PLATES
    print("Generating 2_All_Plates_Mass.png...")
    n_diets = len(results_mass)
    cols2 = int(np.ceil(np.sqrt(n_diets)))
    rows2 = int(np.ceil(n_diets / cols2))
    fig2, axes2 = plt.subplots(rows2, cols2, figsize=(6 * cols2, 6 * rows2))
    axes2 = np.array(axes2).reshape(-1)
    for i, (name, mass_dict) in enumerate(results_mass.items()):
        if i >= len(axes2): break
        ax = axes2[i]
        vals = [mass_dict[c] for c in CAT_ORDER]
        ax.pie(vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.add_artist(plt.Circle((0,0),0.65,fc='white'))
        ax.text(0, 0, "MASS", ha='center', va='center', fontsize=10, color='gray')
    for j in range(n_diets, len(axes2)): axes2[j].axis('off')
    fig2.legend(CAT_ORDER, loc='lower center', ncol=8)
    plt.savefig('2_All_Plates_Mass.png')

    # 3. ALL EMISSIONS
    print("Generating 3_All_Emissions_Donuts.png...")
    n_diets3 = len(results_co2)
    cols3 = int(np.ceil(np.sqrt(n_diets3)))
    rows3 = int(np.ceil(n_diets3 / cols3))
    fig3, axes3 = plt.subplots(rows3, cols3, figsize=(6 * cols3, 6 * rows3))
    axes3 = np.array(axes3).reshape(-1)
    for i, (name, co2_dict) in enumerate(results_co2.items()):
        if i >= len(axes3): break
        ax = axes3[i]
        vals = [co2_dict[c] for c in CAT_ORDER]
        ax.pie(vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.add_artist(plt.Circle((0,0),0.65,fc='white'))
        total_t = sum(vals)
        ax.text(0, 0, f"{int(total_t/1000)}k\nTonnes", ha='center', va='center', fontsize=10, fontweight='bold')
    for j in range(n_diets3, len(axes3)): axes3[j].axis('off')
    fig3.legend(CAT_ORDER, loc='lower center', ncol=8)
    plt.savefig('3_All_Emissions_Donuts.png')

    # 4. DISTANCE TO GOALS
    print("Generating 4_Distance_To_Goals.png...")
    goals = ['5. Dutch Goal (60:40)', '6. Amsterdam Goal (70:30)', '7. EAT-Lancet (Planetary)']
    baselines = ['1. Monitor 2024 (Current)', '3. Metropolitan (High Risk)', '4. Metabolic Balance']
    data_matrix = []
    for base in baselines:
        row = []
        base_val = total_footprints[base]
        for goal in goals:
            goal_val = total_footprints[goal]
            reduction_needed = (base_val - goal_val) / base_val * 100
            row.append(reduction_needed)
        data_matrix.append(row)
    df_matrix = pd.DataFrame(data_matrix, index=baselines, columns=goals)
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_matrix, annot=True, fmt=".1f", cmap="Reds", cbar_kws={'label': '% Reduction Needed'})
    plt.title("Distance to Target: % Reduction Required", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('4_Distance_To_Goals.png')

    # ---------------------------------------------
    # NEW: Scope 1+2 vs Scope 3 Comparison & Shares
    # ---------------------------------------------
    print("Generating 6_Scope12_vs_Scope3.png and 7_Scope3_Share.png...")
    factors = load_impact_factors()
    results_scope12 = {}
    for name, profile in diets.items():
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
        results_scope12[name] = cat_totals

    scope3_totals = {diet: sum(results_co2.get(diet, {}).values()) for diet in results_co2}
    scope12_totals = {diet: sum(results_scope12.get(diet, {}).values()) for diet in results_scope12}
    total_totals = {diet: scope12_totals.get(diet, 0.0) + scope3_totals.get(diet, 0.0) for diet in results_co2}
    
    df_compare = pd.DataFrame({
        'Scope 1+2': pd.Series(scope12_totals),
        'Scope 3': pd.Series(scope3_totals),
        'Total': pd.Series(total_totals)
    }).fillna(0.0)

    ax6 = df_compare.plot(kind='bar', figsize=(14, 8), color=['#7f8c8d', '#e67e22', '#2c3e50'])
    ax6.set_title('Scope 1+2, Scope 3, and Total Food Emissions by Diet (Tonnes CO2e/Year)')
    ax6.set_ylabel('Tonnes CO2e / Year')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('6_Scope12_vs_Scope3_Total.png')

    total_emissions = df_compare['Total']
    share_s12 = (df_compare['Scope 1+2'] / total_emissions).replace([np.inf, np.nan], 0.0) * 100.0
    share_s3 = (df_compare['Scope 3'] / total_emissions).replace([np.inf, np.nan], 0.0) * 100.0
    
    fig7, ax7 = plt.subplots(figsize=(14, 6))
    x = np.arange(len(share_s12))
    ax7.bar(x, share_s12, label='Scope 1+2', color='#7f8c8d', width=0.4)
    ax7.bar(x, share_s3, bottom=share_s12, label='Scope 3', color='#e67e22', width=0.4)
    ax7.set_title('Share of Scope 1+2 and Scope 3 in Total Food CO2')
    ax7.set_ylabel('% of Total Emissions')
    ax7.set_xticks(x)
    ax7.set_xticklabels(df_compare.index, rotation=15, ha='right')
    ax7.legend()
    plt.tight_layout()
    plt.savefig('7_Scope_Shares.png')

    print("Generating 8_All_Total_Emissions_Donuts.png...")
    results_total = {}
    for name, profile in diets.items():
        cat_totals = {cat: 0.0 for cat in CAT_ORDER}
        for item, grams_day in profile.items():
            if item not in factors.index:
                continue
            kg_day = grams_day / 1000.0
            kg_year_person = kg_day * 365.0
            scope3_intensity = factors.loc[item, 'co2'] if 'co2' in factors.columns else 0.0
            scope12_intensity = factors.loc[item, 'scope12'] if 'scope12' in factors.columns else 0.0
            total_intensity = scope3_intensity + scope12_intensity
            co2_total_person_year = kg_year_person * total_intensity
            cat = VISUAL_MAPPING.get(item, item)
            if cat in cat_totals:
                cat_totals[cat] += co2_total_person_year
            else:
                cat_totals[cat] = co2_total_person_year
        try:
            pop = cfg.POPULATION_TOTAL
        except AttributeError:
            pop = None
        if pop:
            for cat in cat_totals:
                cat_totals[cat] = (cat_totals[cat] * pop) / 1000.0
        results_total[name] = cat_totals

    n_diets8 = len(results_total)
    cols8 = int(np.ceil(np.sqrt(n_diets8)))
    rows8 = int(np.ceil(n_diets8 / cols8))
    fig8, axes8 = plt.subplots(rows8, cols8, figsize=(6 * cols8, 6 * rows8))
    axes8 = np.array(axes8).reshape(-1)
    
    for i, (name, total_dict) in enumerate(results_total.items()):
        if i >= len(axes8): break
        ax = axes8[i]
        vals = [total_dict[c] for c in CAT_ORDER]
        ax.pie(vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.add_artist(plt.Circle((0,0),0.65,fc='white'))
        total_t = sum(vals)
        ax.text(0, 0, f"{int(total_t/1000)}k\\nTonnes\\n(1+2+3)", ha='center', va='center', fontsize=9, fontweight='bold')
    
    for j in range(n_diets8, len(axes8)): axes8[j].axis('off')
    fig8.legend(CAT_ORDER, loc='lower center', ncol=8)
    plt.suptitle('Total Emissions (Scope 1+2+3) by Category', fontsize=16, fontweight='bold', y=0.995)
    plt.savefig('8_All_Total_Emissions_Donuts.png')

    print("\nScope 1+2 vs Scope 3 vs Total Summary (Tonnes CO2e/Year):")
    for diet in df_compare.index:
        s12 = df_compare.loc[diet, 'Scope 1+2']
        s3 = df_compare.loc[diet, 'Scope 3']
        total = df_compare.loc[diet, 'Total']
        s3_share = (s3 / total * 100.0) if total > 0 else 0.0
        s12_share = (s12 / total * 100.0) if total > 0 else 0.0
        print(f"- {diet}: S1+2={s12:,.0f} ({s12_share:.1f}%), S3={s3:,.0f} ({s3_share:.1f}%), Total={total:,.0f}")

    # 5. TRANSITIONS (One per goal)
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
        ax2 = fig.add_subplot(grid[0, 1])
        ax2.pie(g_mass, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax2.set_title(f"{goal_key} (Mass)", fontweight='bold')
        ax3 = fig.add_subplot(grid[1, :])
        x = np.arange(len(CAT_ORDER))
        ax3.bar(x - 0.2, b_co2, 0.4, label='Baseline', color='#d9534f')
        ax3.bar(x + 0.2, g_co2, 0.4, label='Goal', color='#5cb85c')
        ax3.set_xticks(x)
        ax3.set_xticklabels(CAT_ORDER, rotation=15)
        ax3.set_title(f"Scope 3 Impact Gap: {baseline_key} vs {goal_key}", fontweight='bold')
        ax3.legend()
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    plot_transition('1. Monitor 2024 (Current)', '5. Dutch Goal (60:40)', '5a_Transition_Dutch.png')
    plot_transition('1. Monitor 2024 (Current)', '6. Amsterdam Goal (70:30)', '5b_Transition_Amsterdam.png')
    plot_transition('1. Monitor 2024 (Current)', '7. EAT-Lancet (Planetary)', '5c_Transition_EAT.png')
    # New transitions for added diets
    plot_transition('1. Monitor 2024 (Current)', '8. Schijf van 5 (Guideline)', '5d_Transition_Schijf.png')
    plot_transition('1. Monitor 2024 (Current)', '9. Mediterranean Diet', '5e_Transition_Mediterranean.png')

    # 6. TABLE VISUALIZATION (New Request)
    print("Generating 6_Table_Tonnage.png...")
    # Prepare Dataframe for Table
    table_data = []
    short_names = ["1.Monitor", "2.Theory", "3.Metro", "4.Meta", "5.DuGoal", "6.AmGoal", "7.EAT", "8.Schijf", "9.Med"]
    
    for cat in CAT_ORDER:
        row = [cat]
        for d in diets.keys():
            val = results_co2[d][cat]
            row.append(f"{val:,.0f}")
        table_data.append(row)
    
    # Add Total Row
    total_row = ["TOTAL"]
    for d in diets.keys():
        t = sum(results_co2[d].values())
        total_row.append(f"{t:,.0f}")
    table_data.append(total_row)

    # Create Plot for Table
    fig_table, ax_table = plt.subplots(figsize=(14, 6))
    ax_table.axis('off')
    col_labels = ["Category"] + short_names
    
    the_table = ax_table.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.scale(1, 1.5)
    
    # Highlight Header and Total Row
    for (row, col), cell in the_table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#404040')
        elif row == len(table_data):
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#e0e0e0')

    plt.title("Master Scope 3 Tonnage Report (Tonnes CO2e/Year)", fontweight='bold', y=1.05)
    plt.savefig('6_Table_Tonnage.png')

    # ---------------------------------------------------------
    # CONSOLE OUTPUT
    # ---------------------------------------------------------
    print("\nMaster Analysis Complete. All images generated.")
    print("Table data printed to '6_Table_Tonnage.png'.")

if __name__ == "__main__":
    run_full_analysis()