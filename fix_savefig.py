#!/usr/bin/env python3
"""
Quick script to replace all remaining 'images/' with directory paths
"""
import re

file_path = "Master Hybrid Amsterdam Model v3.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all remaining savefig calls
replacements = [
    ("plt.savefig('images/11_Emissions_vs_Protein.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '11_Emissions_vs_Protein.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '11_Emissions_vs_Protein.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/12_Diets_vs_Goals_MultiResource.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '12_Diets_vs_Goals_MultiResource.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '12_Diets_vs_Goals_MultiResource.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/12b_Emissions_vs_Reference_MultiGoal.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '12b_Emissions_vs_Reference_MultiGoal.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '12b_Emissions_vs_Reference_MultiGoal.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/9_CO2_vs_Mass_Share.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '9_CO2_vs_Mass_Share.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '9_CO2_vs_Mass_Share.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/10_Impact_by_Food_Type.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '10_Impact_by_Food_Type.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '10_Impact_by_Food_Type.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/14a_Delta_Analysis_Total_Emissions.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '14a_Delta_Analysis_Total_Emissions.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '14a_Delta_Analysis_Total_Emissions.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/14b_Delta_Analysis_By_Category.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '14b_Delta_Analysis_By_Category.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '14b_Delta_Analysis_By_Category.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/14c_Mass_vs_Emissions_Share.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '14c_Mass_vs_Emissions_Share.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '14c_Mass_vs_Emissions_Share.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/14d_Scope_Breakdown_Baseline_vs_Goals.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '14d_Scope_Breakdown_Baseline_vs_Goals.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '14d_Scope_Breakdown_Baseline_vs_Goals.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/15_Table_APA_Emissions.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '15_Table_APA_Emissions.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '15_Table_APA_Emissions.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/16_Sensitivity_Analysis_Tornado.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '16_Sensitivity_Analysis_Tornado.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '16_Sensitivity_Analysis_Tornado.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/17_Emissions_by_Category_vs_Reference.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '17_Emissions_by_Category_vs_Reference.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '17_Emissions_by_Category_vs_Reference.png'), dpi=300, bbox_inches='tight')"),
    
    ("plt.savefig('images/18_Dietary_Intake_vs_Reference.png', dpi=300, bbox_inches='tight')",
     "plt.savefig(os.path.join(core_dir, '18_Dietary_Intake_vs_Reference.png'), dpi=300, bbox_inches='tight')\n    plt.savefig(os.path.join(appendix_dir, '18_Dietary_Intake_vs_Reference.png'), dpi=300, bbox_inches='tight')"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Replaced: {old[:50]}...")
    else:
        print(f"✗ Not found: {old[:50]}...")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! All savefig paths updated.")
