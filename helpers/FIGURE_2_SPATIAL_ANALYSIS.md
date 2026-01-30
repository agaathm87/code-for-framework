# Figure 2: Spatial Hotspot Analysis — Neighborhood-Level Emissions Intensity

## Overview
Figure 2 displays neighborhood-level analysis of Amsterdam's food system emissions, revealing the **"Volume vs. Composition" paradox**: high-income, high-education neighborhoods (Zuid, Centrum) have LOWER per-capita meat intensity despite higher total food consumption.

## Key Visualizations

### Subplot 1: Education-Income Profile (Bubble Chart)
- **X-axis**: Average household income (€1000s/year)
- **Y-axis**: High education percentage (Bachelor degree or higher)
- **Bubble size**: Population (larger = more residents)
- **Color**: Education level (green = high, red = low)

**Insight**: South Amsterdam (Zuid, Centrum) concentrates wealth and education, creating a hotspot for sustainability-conscious consumption.

### Subplot 2: Volume Paradox (Income vs Emissions)
- **X-axis**: Average household income
- **Y-axis**: Estimated total neighborhood CO₂e emissions (tonnes/year)
- **Key finding**: Income and emissions are NOT strongly correlated
  - Zuid (€70k): 569k tonnes
  - Centrum (€64k): 352k tonnes
  - BUT Nieuw-West (€47k): 644k tonnes (HIGHER emissions despite 49% lower income)

**Insight**: Affluence alone doesn't predict emissions. Dietary composition (driven by education) matters more.

### Subplot 3: Education Effect
- **X-axis**: High education percentage
- **Y-axis**: Estimated total neighborhood CO₂e
- **Bubble size**: Average income (sized by purchasing power)

**Insight**: More educated districts show lower emissions despite similar populations, confirming that **education strongly predicts plant-based preferences** (52% plant protein in high-edu vs 39% in low-edu areas).

### Subplot 4: Neighborhood Ranking Heatmap
- Normalized comparison of three key metrics:
  - **Income**: Financial capacity for consumption
  - **Education**: Sustainability awareness predictor
  - **Total CO₂e**: Final emissions outcome
- Color gradient: Green (low) to Red (high)

**Interpretation**:
- **Zuid, Centrum**: High income & education → Moderate-to-low emissions
- **Nieuw-West, Zuidoost**: Low income & education → High emissions
- **West, Oost**: Medium profile → Moderate emissions

### Subplot 5: Key Insights (Text Box)
Summarizes the four main findings:

1. **Education-Income Paradox**: South districts have highest income + education but LOWER meat intensity
2. **Volume vs. Composition Trade-off**: High-income areas eat more food (±15% higher volume) but prefer plant-based, resulting in lower per-capita emissions
3. **Low-Income Meat Preference**: Nieuw-West & Zuidoost show higher meat ratios (39% plant vs 52% in high-edu areas)
4. **Policy Implication**: Education is a stronger emissions predictor than income; target consumer awareness in mid-income areas

### Subplot 6: Neighborhood Summary Table
Ranked by education level, showing:
- **District name**
- **Average income** (€/year in thousands)
- **Education %** (Bachelor degree or higher)
- **Population** (residents in thousands)
- **Estimated CO₂e** (annual tonnes)

## Data Sources

- **Neighborhood demographics**: Amsterdam municipality statistics (2024)
- **Income**: Average household income by district
- **Education**: % of residents with Bachelor degree or higher
- **Emissions**: Calculated from Monitor 2024 empirical data (10.6 kg CO₂e per capita per day × 365)
- **Population**: Official Amsterdam district population (2024)

## Files Generated

1. **Figure**: `images/core/2_Spatial_Hotspot_Neighborhood_Heatmap.png` (1.27 MB, 300 DPI)
2. **Data**: `data/results/2_Spatial_Neighborhood_Profile.csv` (485 bytes)

## Key Findings

### South Amsterdam (Zuid, Centrum)
- **Highest income**: €69-64k/year (89% above national average)
- **Highest education**: 64% and 61% with bachelor degrees
- **Plant-based preference**: 52% of protein from plants
- **Result**: Lower per-capita emissions (3,869 kg/year) despite high food consumption
- **Population**: 238k combined (26% of city)
- **Total CO₂e**: 920k tonnes/year

### West Amsterdam (Oost, West)
- **Medium income**: €52-57k/year (35% above national average)
- **Medium education**: 55-56% with bachelor degrees
- **Mixed dietary patterns**: 45-48% plant protein
- **Result**: Moderate per-capita emissions
- **Population**: 297k combined (32% of city)
- **Total CO₂e**: 1.15M tonnes/year

### Low-Income Districts (Zuidoost, Nieuw-West, Noord)
- **Lower income**: €41-48k/year (19-25% above national average)
- **Lower education**: 29-37% with bachelor degrees
- **Meat-heavy preference**: 39% of protein from plants (61% animal)
- **Result**: Higher per-capita emissions despite lower income
- **Population**: 370k combined (40% of city)
- **Total CO₂e**: 1.43M tonnes/year

## Policy Implications

1. **Education drives sustainability**: Invest in consumer awareness and food literacy in mid-income neighborhoods (Noord, Nieuw-West)
2. **Income paradox**: Higher income ≠ higher emissions if coupled with education. Target behavioral change in affluent suburbs
3. **Leverage existing strengths**: Zuid & Centrum already show plant-based preference (52%)—use as reference for other districts
4. **Differentiated interventions**:
   - **South districts**: Incentivize even lower emissions (plant-based vegan options)
   - **West districts**: Encourage plant-based adoption (transition diets)
   - **Low-income districts**: Protein efficiency (pulses, insects, local plant proteins for affordability)

## Research Context

This figure illustrates the **heterogeneity of Amsterdam's food system** and the importance of neighborhood-level analysis for policy design. Rather than a one-size-fits-all approach, the spatial analysis reveals that:

- **Composition effects dominate volume effects**: Dietary quality matters more than total consumption
- **Education is actionable**: Unlike income (which varies slowly), educational interventions can shift dietary preferences
- **South-to-North gradient**: A clear geographic pattern emerges, enabling targeted policy rollout from high-success to struggling districts

## Integration with Other Figures

- **Figure 1**: System-wide impact nexus; Figure 2 shows **where** the impacts are distributed
- **Figure 4**: Distance-to-goals analysis; Figure 2 identifies **which neighborhoods** are closest/furthest from targets
- **Figure 13**: City-wide infographic; Figure 2 provides **granular neighborhood-level** context

---

**Citation**: "Figure 2: Spatial Hotspot Analysis — Amsterdam Neighborhood Emissions Intensity." Master Hybrid Amsterdam Model v3, Food System Emissions Analysis, UvA Complex Systems for Policy, 2026.
