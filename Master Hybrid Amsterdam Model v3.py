import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. CONFIGURATION
# ==========================================
class HybridModelConfig:
    def __init__(self):
        self.NATIONAL_AVG_INCOME = 32000
        self.SCALING_C1 = 0.8
        self.SCALING_C2 = 0.2
        self.WASTE_FACTOR = 1.15   # Supply chain loss
        self.POPULATION_TOTAL = 882000

# --- VISUALIZATION MAPPING ---
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
CAT_ORDER = ['Red Meat', 'Poultry', 'Dairy & Eggs', 'Fish', 'Plant Protein', 'Staples', 'Veg & Fruit', 'Ultra-Processed']
COLORS = ['#8B0000', '#F08080', '#FFD700', '#4682B4', '#2E8B57', '#DEB887', '#90EE90', '#A9A9A9']
COLOR_MAP = dict(zip(CAT_ORDER, COLORS))

# ==========================================
# 2. DATA INGESTION
# ==========================================
def load_impact_factors():
    """ Scope 3 Factors (CO2 kg/kg, Land m2/kg, Water L/kg) """
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
    """ Comparison Diets (Grams/Day) """
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
        }
    }
    return diets

def load_neighborhood_data():
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
    def __init__(self, config):
        self.cfg = config
        self.factors = load_impact_factors()

    def calculate_beta(self, row):
        """ Calculates Consumption Scaling Factor based on Income & Education """
        income_ratio = row['Avg_Income'] / self.cfg.NATIONAL_AVG_INCOME
        volume_beta = self.cfg.SCALING_C1 * np.exp(self.cfg.SCALING_C2 * income_ratio)
        
        # Education Modifier (Higher Edu = Less Meat)
        if row['High_Education_Pct'] > 0.5:
            meat_modifier = 0.85
            plant_modifier = 1.15
        else:
            meat_modifier = 1.1
            plant_modifier = 0.9
            
        return volume_beta, meat_modifier, plant_modifier

    def calculate_raw_impact(self, diet_profile):
        """ Calculates raw CO2, Land, Water per person/day """
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
    fig2, axes2 = plt.subplots(2, 4, figsize=(24, 12))
    axes2 = axes2.flatten()
    for i, (name, mass_dict) in enumerate(results_mass.items()):
        if i >= len(axes2): break
        ax = axes2[i]
        vals = [mass_dict[c] for c in CAT_ORDER]
        ax.pie(vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.add_artist(plt.Circle((0,0),0.65,fc='white'))
        ax.text(0, 0, "MASS", ha='center', va='center', fontsize=10, color='gray')
    for j in range(i+1, len(axes2)): axes2[j].axis('off')
    fig2.legend(CAT_ORDER, loc='lower center', ncol=8)
    plt.savefig('2_All_Plates_Mass.png')

    # 3. ALL EMISSIONS
    print("Generating 3_All_Emissions_Donuts.png...")
    fig3, axes3 = plt.subplots(2, 4, figsize=(24, 12))
    axes3 = axes3.flatten()
    for i, (name, co2_dict) in enumerate(results_co2.items()):
        if i >= len(axes3): break
        ax = axes3[i]
        vals = [co2_dict[c] for c in CAT_ORDER]
        ax.pie(vals, labels=None, autopct='%1.0f%%', startangle=90, pctdistance=0.85, colors=COLORS)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.add_artist(plt.Circle((0,0),0.65,fc='white'))
        total_t = sum(vals)
        ax.text(0, 0, f"{int(total_t/1000)}k\nTonnes", ha='center', va='center', fontsize=10, fontweight='bold')
    for j in range(i+1, len(axes3)): axes3[j].axis('off')
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

    # 6. TABLE VISUALIZATION (New Request)
    print("Generating 6_Table_Tonnage.png...")
    # Prepare Dataframe for Table
    table_data = []
    short_names = ["1.Monitor", "2.Theory", "3.Metro", "4.Meta", "5.DuGoal", "6.AmGoal", "7.EAT"]
    
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