import pandas as pd

df = pd.read_csv("data\medellin_20250911.csv")


# Eliminar o reemplazar caracteres no numéricos
df['Valor del Contrato'] = pd.to_numeric(df['Valor del Contrato'], errors='coerce')  # convierte no numéricos en NaN

# Luego convertir a entero (si hay nulos, usa 'Int64')
df['Valor del Contrato'] = df['Valor del Contrato'].astype('Int64')


df.info()