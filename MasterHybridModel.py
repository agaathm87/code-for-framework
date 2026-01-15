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
    Load dietary scenario profiles for comparison analysis.
    
    Each diet represents a different consumption pattern:
    1. Amsterdam Baseline: Current estimated average consumption
    2. Metropolitan: High-risk Western diet (high meat/processed)
    3. Metabolic Balance: Animal-based low-carb diet
    4. Dutch Goal (60:40): National policy target (60% plant, 40% animal protein)
    5. Amsterdam Goal (70:30): City policy target (70% plant, 30% animal protein)
    6. EAT-Lancet: Planetary health diet (global sustainability benchmark)
    
    Returns:
        dict: Dictionary of diet names to food consumption profiles (grams/day)
    """
    diets = {
        '1. Amsterdam Baseline': {
            'Beef': 12, 'Pork': 20, 'Chicken': 28, 'Cheese': 40, 'Milk': 260,
            'Fish': 10, 'Eggs': 25, 'Pulses': 8, 'Nuts': 10, 'Meat_Subs': 15,
            'Grains': 220, 'Vegetables': 150, 'Fruits': 130, 'Potatoes': 50,
            'Sugar': 40, 'Processed': 150 
        },
        '2. Metropolitan (High Risk)': {
            'Beef': 45, 'Pork': 25, 'Chicken': 60, 'Cheese': 50, 'Milk': 200,
            'Fish': 15, 'Eggs': 30, 'Pulses': 5, 'Nuts': 5, 'Meat_Subs': 5,
            'Grains': 180, 'Vegetables': 110, 'Fruits': 100, 'Potatoes': 80,
            'Sugar': 80, 'Processed': 200 
        },
        '3. Metabolic Balance (Animal)': {
            'Beef': 60, 'Pork': 40, 'Chicken': 80, 'Cheese': 50, 'Milk': 50,
            'Fish': 40, 'Eggs': 50, 'Pulses': 10, 'Nuts': 20, 'Meat_Subs': 0,
            'Grains': 50, 'Vegetables': 200, 'Fruits': 100, 'Potatoes': 0,
            'Sugar': 5, 'Processed': 10
        },
        '4. Dutch Goal (60:40)': {
            'Beef': 15, 'Pork': 15, 'Chicken': 25, 'Cheese': 35, 'Milk': 250,
            'Fish': 15, 'Eggs': 20, 'Pulses': 40, 'Nuts': 20, 'Meat_Subs': 25,
            'Grains': 225, 'Vegetables': 200, 'Fruits': 180, 'Potatoes': 90,
            'Sugar': 30, 'Processed': 80
        },
        '5. Amsterdam Goal (70:30)': {
            'Beef': 5, 'Pork': 5, 'Chicken': 10, 'Cheese': 20, 'Milk': 100,
            'Fish': 15, 'Eggs': 15, 'Pulses': 80, 'Nuts': 40, 'Meat_Subs': 40,
            'Grains': 250, 'Vegetables': 250, 'Fruits': 200, 'Potatoes': 80,
            'Sugar': 20, 'Processed': 50
        },
        '6. EAT-Lancet (Planetary)': {
            'Beef': 7, 'Pork': 7, 'Chicken': 29, 'Cheese': 0, 'Milk': 250,
            'Fish': 28, 'Eggs': 13, 'Pulses': 75, 'Nuts': 50, 'Meat_Subs': 0,
            'Grains': 232, 'Vegetables': 300, 'Fruits': 200, 'Potatoes': 50,
            'Sugar': 30, 'Processed': 0
        },
        '7. Schijf van 5 (Guideline)': {
            'Beef': 10, 'Pork': 10, 'Chicken': 25, 'Cheese': 30, 'Milk': 250,
            'Fish': 25, 'Eggs': 20, 'Pulses': 30, 'Nuts': 25, 'Meat_Subs': 20,
            'Grains': 240, 'Vegetables': 250, 'Fruits': 200, 'Potatoes': 70,
            'Sugar': 25, 'Processed': 60
        },
        '8. Mediterranean Diet': {
            'Beef': 8, 'Pork': 8, 'Chicken': 20, 'Cheese': 30, 'Milk': 200,
            'Fish': 35, 'Eggs': 18, 'Pulses': 60, 'Nuts': 30, 'Meat_Subs': 10,
            'Grains': 240, 'Vegetables': 300, 'Fruits': 220, 'Potatoes': 60,
            'Sugar': 20, 'Processed': 50
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
            tuple: (mass_dict, co2_dict)
                - mass_dict: Consumption mass by category (grams/day)
                - co2_dict: Annual city emissions by category (tonnes CO2e/year)
        """
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
    
    print("Running Scope 3 Engine for all diets...")
    for name, profile in diets.items():
        mass, co2 = engine.aggregate_visual_data(profile)
        results_mass[name] = mass
        results_co2[name] = co2

    # CHART 1: NEXUS ANALYSIS
    print("Generating 1_Nexus_Analysis.png...")
    nexus_data = []
    for name, profile in diets.items():
        res = engine.calculate_raw_impact(profile)
        res['Diet'] = name
        nexus_data.append(res)
    df_nexus = pd.DataFrame(nexus_data).set_index('Diet').sort_values('co2', ascending=False)
    
    fig1, axes = plt.subplots(1, 3, figsize=(18, 6))
    df_nexus['co2'].plot(kind='bar', ax=axes[0], color='#E74C3C', title='CO2 (kg/person/day)')
    df_nexus['land'].plot(kind='bar', ax=axes[1], color='#2ECC71', title='Land Use (m2/person/day)')
    df_nexus['water'].plot(kind='bar', ax=axes[2], color='#3498DB', title='Water Use (L/person/day)')
    plt.tight_layout()
    plt.savefig('1_Nexus_Analysis.png')

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

    plot_transition('1. Amsterdam Baseline', '4. Dutch Goal (60:40)', '2a_Transition_DutchGoal.png')
    plot_transition('1. Amsterdam Baseline', '5. Amsterdam Goal (70:30)', '2b_Transition_AmsterdamGoal.png')
    plot_transition('1. Amsterdam Baseline', '6. EAT-Lancet (Planetary)', '2c_Transition_EAT_Lancet.png')
    # New transitions for added diets
    plot_transition('1. Amsterdam Baseline', '7. Schijf van 5 (Guideline)', '2d_Transition_Schijf.png')
    plot_transition('1. Amsterdam Baseline', '8. Mediterranean Diet', '2e_Transition_Mediterranean.png')

    # CHART 3: ALL DIETS PLATE
    print("Generating 3_All_Diets_Plates.png...")
    n_diets = len(results_mass)
    cols3 = int(np.ceil(np.sqrt(n_diets)))
    rows3 = int(np.ceil(n_diets / cols3))
    fig3, axes3 = plt.subplots(rows3, cols3, figsize=(6 * cols3, 6 * rows3))
    axes3 = np.array(axes3).reshape(-1)
    for i, (name, mass_dict) in enumerate(results_mass.items()):
        if i >= len(axes3): break
        ax = axes3[i]
        vals = [mass_dict[c] for c in CAT_ORDER]
        ax.pie(vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax.set_title(name, fontsize=10, fontweight='bold')
        ax.add_artist(plt.Circle((0,0),0.70,fc='white'))
    for j in range(n_diets, len(axes3)): axes3[j].axis('off')
    fig3.legend(CAT_ORDER, loc='lower center', ncol=8)
    plt.savefig('3_All_Diets_Plates.png')

    # CHART 4: IMPACT STACK
    print("Generating 4_Impact_Stack.png...")
    fig4, ax4 = plt.subplots(figsize=(14, 8))
    diet_names = list(results_co2.keys())
    bottoms = np.zeros(len(diet_names))
    for i, cat in enumerate(CAT_ORDER):
        values = [results_co2[d][cat] for d in diet_names]
        ax4.bar(diet_names, values, bottom=bottoms, label=cat, color=COLORS[i], width=0.6)
        bottoms += np.array(values)
    ax4.set_title("The Carbon Fingerprint: Scope 3 Impact Comparison", fontsize=16)
    ax4.set_ylabel("Tonnes CO2e / Year")
    plt.xticks(rotation=15, ha='right')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('4_Impact_Stack.png')

    # ---------------------------------------------------------
    # PART D: Scope 1+2 vs Scope 3 Comparisons
    # ---------------------------------------------------------
    print("Generating 6_Scope12_vs_Scope3.png and 7_Scope3_Share.png...")
    factors = load_impact_factors()
    # Compute Scope 1+2 totals by diet (tonnes/year)
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
        # Convert to tonnes/year across population if available
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

    # Chart 6: All three scopes grouped bars
    ax6 = df_compare.plot(kind='bar', figsize=(14, 8), color=['#7f8c8d', '#e67e22', '#2c3e50'])
    ax6.set_title('Scope 1+2, Scope 3, and Total Food Emissions by Diet (Tonnes CO2e/Year)')
    ax6.set_ylabel('Tonnes CO2e / Year')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('6_Scope12_vs_Scope3_Total.png')

    # Chart 7: Share of each scope in total
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

    # Chart 8: Total Emissions Donuts (1+2+3 breakdown by category)
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

    # Console summary
    print("\nScope 1+2 vs Scope 3 vs Total Summary (Tonnes CO2e/Year):")
    for diet in df_compare.index:
        s12 = df_compare.loc[diet, 'Scope 1+2']
        s3 = df_compare.loc[diet, 'Scope 3']
        total = df_compare.loc[diet, 'Total']
        s3_share = (s3 / total * 100.0) if total > 0 else 0.0
        s12_share = (s12 / total * 100.0) if total > 0 else 0.0
        print(f"- {diet}: S1+2={s12:,.0f} ({s12_share:.1f}%), S3={s3:,.0f} ({s3_share:.1f}%), Total={total:,.0f}")

    # ---------------------------------------------------------
    # PART B: NEIGHBORHOOD HOTSPOTS (Spatial Analysis)
    # ---------------------------------------------------------
    print("Generating 5_Neighborhood_Hotspots.png...")
    # Run Simulation on Baseline Diet
    df_spatial = engine.run_spatial_simulation(neighborhoods, diets['1. Amsterdam Baseline'])
    
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