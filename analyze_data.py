import pandas as pd

df = pd.read_csv('Delhi_v2.csv')
print('Shape:', df.shape)
print('\nColumns:', df.columns.tolist())
print('\nData types:\n', df.dtypes)
print('\nMissing values:\n', df.isnull().sum())
print('\nSample data:')
print(df.head())
