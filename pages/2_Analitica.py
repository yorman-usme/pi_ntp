import streamlit as st
import pandas as pd

# Título
st.title("Análisis de datos CSV - Medellín")


df = pd.read_csv("data/medellin_20250911.csv")


# Información general
st.write("Número de filas y columnas:", df.shape)
st.write("Columnas disponibles:", df.columns.tolist())

# Vista previa
st.dataframe(df.head(20))

st.header("Contratos por tipo")
contratos_tipo = df['Tipo de Contrato'].value_counts()
st.bar_chart(contratos_tipo)


st.header("Contratos por modalidad")
modalidad = df['Modalidad de Contratacion'].value_counts()
st.bar_chart(modalidad)



st.header("Top 10 proveedores por valor total")
top_proveedores = df.groupby('Proveedor Adjudicado')['Valor del Contrato'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_proveedores)



st.header("Distribución de contratos por ciudad")
ciudades = df['Ciudad'].value_counts()
st.bar_chart(ciudades)
