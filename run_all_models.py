#!/usr/bin/env python
"""
Master execution script to run all 4 models and compile results
"""
import os
import sys
import subprocess
import time

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

models = [
    ('MasterHybridModel.py', 'Base Model (6 diets)'),
    ('Master Hybrid Amsterdam Model v3.py', 'V3 Model (9 diets)'),
    ('Master_hybrid_Amsterdam_Model-v2.py', 'V2 Model (9 diets)'),
    ('Master_hybrid_Amsterdam_Model.py', 'Advanced Model (8 diets)')
]

print("=" * 80)
print("RUNNING ALL 4 MODELS SEQUENTIALLY")
print("=" * 80)

for model_file, model_name in models:
    if not os.path.exists(model_file):
        print(f"\n⚠ SKIPPING: {model_name} - File not found: {model_file}")
        continue
    
    print(f"\n{'='*80}")
    print(f"STARTING: {model_name}")
    print(f"{'='*80}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run the model
        result = subprocess.run(
            [sys.executable, model_file],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        # Print key outputs
        if result.stdout:
            # Print Monitor 2024 validation and chart generation messages
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Monitor 2024' in line or 'Generating' in line or 'saved' in line or 'Error' in line:
                    print(line)
        
        if result.returncode == 0:
            print(f"✓ {model_name} completed successfully")
        else:
            print(f"✗ {model_name} failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error output:\n{result.stderr[:500]}")
    
    except subprocess.TimeoutExpired:
        print(f"✗ {model_name} timed out after 10 minutes")
    except Exception as e:
        print(f"✗ {model_name} failed with exception: {e}")

print(f"\n{'='*80}")
print("ALL MODELS COMPLETE")
print(f"{'='*80}")

# List generated charts
print("\nGenerated chart files:")
for f in sorted(os.listdir('.')):
    if f.endswith('.png') and any(x in f for x in ['11b', '11c', '12_E', '13_']):
        size_kb = os.path.getsize(f) / 1024
        print(f"  {f} ({size_kb:.0f} KB)")
