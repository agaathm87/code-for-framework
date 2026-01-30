import pandas as pd

df = pd.read_csv('Database milieubelasting voedingsmiddelen - database versie 23 september 2024.csv', 
                 sep=';', skiprows=2, encoding='utf-8', nrows=3)

print('All columns in RIVM detailed database:')
print('='*80)
for i, col in enumerate(df.columns):
    print(f'{i:2d}. {col}')
