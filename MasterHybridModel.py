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
        'Beef':      {'co2': 28.0, 'land': 25.0, 'water': 15400},
        'Pork':      {'co2': 5.0,  'land': 9.0,  'water': 6000},
        'Chicken':   {'co2': 3.5,  'land': 7.0,  'water': 4300},
        'Cheese':    {'co2': 10.0, 'land': 12.0, 'water': 5000},
        'Milk':      {'co2': 1.3,  'land': 1.5,  'water': 1000},
        'Fish':      {'co2': 3.5,  'land': 0.5,  'water': 2000},
        'Eggs':      {'co2': 2.2,  'land': 2.5,  'water': 3300},
        'Pulses':    {'co2': 0.9,  'land': 3.0,  'water': 4000},
        'Nuts':      {'co2': 0.3,  'land': 2.5,  'water': 9000},
        'Meat_Subs': {'co2': 2.5,  'land': 3.0,  'water': 200}, 
        'Grains':    {'co2': 1.1,  'land': 1.8,  'water': 1600},
        'Vegetables':{'co2': 0.6,  'land': 0.5,  'water': 320},
        'Fruits':    {'co2': 0.7,  'land': 0.6,  'water': 960},
        'Potatoes':  {'co2': 0.4,  'land': 0.3,  'water': 290},
        'Sugar':     {'co2': 2.0,  'land': 1.5,  'water': 200},
        'Processed': {'co2': 2.5,  'land': 1.5,  'water': 300}
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
        }
    }
    return diets

def load_neighborhood_data():
    """ 
    Load Amsterdam neighborhood socio-economic data.
    
    Data simulates CBS 'Kerncijfers wijken en buurten' statistics.
    Income differences drive consumption scaling via Valencia beta factors:
    - Higher income areas (Zuid, Centrum) have higher consumption volumes
    - Lower income areas consume closer to national average
    
    Returns:
        pd.DataFrame: Neighborhood data with columns:
            - Neighborhood: District name
            - Population: Resident count
            - Avg_Income: Average household income (EUR/year)
    """
    return pd.DataFrame({
        'Neighborhood': ['Centrum', 'Zuid', 'West', 'Noord', 'Zuidoost', 'Nieuw-West', 'Oost'],
        'Population': [87000, 145000, 145000, 99000, 89000, 160000, 135000],
        'Avg_Income': [48000, 56000, 34000, 29000, 24000, 26000, 36000] # Euros/year
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
    def calculate_beta(self, local_income):
        """ 
        Calculate consumption scaling factor using Valencia downscaling.
        
        Higher income neighborhoods consume more total food volume and
        have higher waste rates. Uses exponential scaling relationship:
        Beta = C1 * exp(C2 * income_ratio)
        
        Args:
            local_income (float): Average neighborhood income (EUR/year)
            
        Returns:
            float: Beta scaling factor (>1 for high income, <1 for low income)
                   Floor of 0.75 prevents unrealistic low consumption estimates
        """
        income_ratio = local_income / self.cfg.NATIONAL_AVG_INCOME
        # Valencia Formula: Beta = C1 * e^(C2 * ratio)
        beta = self.cfg.SCALING_C1 * np.exp(self.cfg.SCALING_C2 * income_ratio)
        return max(beta, 0.75) # Floor to prevent starvation modeling

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
        """
        results = []
        base_impact = self.calculate_raw_impact(diet_profile) # Per capita impact of base diet
        
        for _, row in neighborhoods.iterrows():
            beta = self.calculate_beta(row['Avg_Income'])
            
            # Apply Beta to the impact (Assuming impact scales with expenditure/volume)
            # In a full model, we'd scale only luxury foods, but scaling total is a valid proxy
            local_co2_per_capita = base_impact['co2'] * beta 
            
            # Total Neighborhood Tonnage
            total_tonnes = (local_co2_per_capita * 365 * row['Population']) / 1000
            
            results.append({
                'Neighborhood': row['Neighborhood'],
                'Population': row['Population'],
                'Income': row['Avg_Income'],
                'Beta': beta,
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

    # CHART 3: ALL DIETS PLATE
    print("Generating 3_All_Diets_Plates.png...")
    fig3, axes3 = plt.subplots(2, 3, figsize=(18, 10))
    axes3 = axes3.flatten()
    for i, (name, mass_dict) in enumerate(results_mass.items()):
        ax = axes3[i]
        vals = [mass_dict[c] for c in CAT_ORDER]
        ax.pie(vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax.set_title(name, fontsize=10, fontweight='bold')
        ax.add_artist(plt.Circle((0,0),0.70,fc='white'))
    fig3.legend(CAT_ORDER, loc='lower center', ncol=4)
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
    print("\n--- NEIGHBORHOOD HOTSPOT ANALYSIS (BASELINE) ---")
    print(df_spatial[['Neighborhood', 'Population', 'Beta', 'Total_CO2_Tonnes']].sort_values('Total_CO2_Tonnes', ascending=False).to_string(index=False))

if __name__ == "__main__":
    run_full_analysis()