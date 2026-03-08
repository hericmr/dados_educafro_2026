import pandas as pd
import os

df1 = pd.read_csv('/home/hericmr/Documentos/dados_educafro_2026/entrevistas_rows_atualizada_8-3-2026.csv')
df2 = pd.read_csv('/home/hericmr/Documentos/dados_educafro_2026/entrevistas_educafro_consolidated_20260228.csv')

# First let's print the shapes and columns to understand the data
print("DF1 shape:", df1.shape)
print("DF2 shape:", df2.shape)
print("\nDF1 columns:", df1.columns.tolist())
print("\nDF2 columns:", df2.columns.tolist())

# It seems ID is the common key
# We want to merge these two together. The user says "gerar a tabela mais consolidada com a maior quantidade de dados, todos os dados juntos."
# Let's see if one is just newer rows or if they have different columns

# We can concatenate them and then drop duplicates by 'id', keeping the last one (assuming newer is better, though we need to check timestamps)
# DF1 seems to have more columns or DF2 has more columns? We'll check.
