#!/usr/bin/env python3
"""
Quick test of spatial visualization function only
"""
import sys
import importlib.util
sys.path.insert(0, '.')

# Load module with spaces in filename
spec = importlib.util.spec_from_file_location("model", "Master Hybrid Amsterdam Model v3.py")
model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_module)

load_diet_profiles = model_module.load_diet_profiles
load_neighborhood_data = model_module.load_neighborhood_data
create_neighborhood_heatmap = model_module.create_neighborhood_heatmap

print("Loading data...")
neighborhoods = load_neighborhood_data()
diets = load_diet_profiles()

print(f"✓ Neighborhoods: {len(neighborhoods)} districts")
print(f"✓ Diets: {len(diets)} scenarios")

print("\nGenerating spatial hotspot visualization...")
try:
    create_neighborhood_heatmap(neighborhoods, diets, diet_name='1. Monitor 2024 (Current)', output_dir='images/core')
    print("✓ Spatial visualization complete!")
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
