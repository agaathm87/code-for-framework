import pandas as pd

# Load RIVM
df = pd.read_csv('../datasets/Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv', 
                 skiprows=2, sep=';', encoding='utf-8')
df['CO2'] = pd.to_numeric(df.iloc[:, 3].astype(str).str.replace(',', '.'), errors='coerce')

# Find pasta products
pasta = df[df.iloc[:, 0].str.contains('pasta|macaroni|spaghetti|noodle|vermicelli', case=False, na=False)]

print('\n' + '='*80)
print('PASTA/NOODLE PRODUCTS IN RIVM DATABASE')
print('='*80 + '\n')

for i, row in pasta.iterrows():
    prod_name = row.iloc[0]
    co2_val = row['CO2']
    print(f'{prod_name[:75]:75} | CO2: {co2_val:.2f}')

print(f'\n✓ Found {len(pasta)} pasta/noodle products\n')

# Also search for rice (as alternative for noodles)
print('='*80)
print('RICE PRODUCTS IN RIVM DATABASE (Alternative for noodles)')
print('='*80 + '\n')

rice = df[df.iloc[:, 0].str.contains('rice|rijst', case=False, na=False)]
for i, row in rice.iterrows():
    prod_name = row.iloc[0]
    co2_val = row['CO2']
    print(f'{prod_name[:75]:75} | CO2: {co2_val:.2f}')

print(f'\n✓ Found {len(rice)} rice products\n')
