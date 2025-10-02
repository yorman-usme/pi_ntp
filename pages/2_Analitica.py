import streamlit as st
import pandas as pd
import numpy as np


# Título
st.title("Análisis de datos CSV - Medellín")


df = pd.read_csv("data/medellin_20250911.csv")


# Información general
st.write("Número de filas y columnas:", df.shape)
st.write("Columnas disponibles:", df.columns.tolist())

# Vista previa
st.dataframe(df.head(20))

st.header("Contratos por Tipo de Contrato")

# Asegurarse que la columna no tenga valores nulos
df = df.dropna(subset=["Tipo de Contrato"])

# Obtener valores únicos para el selectbox
tipos = sorted(df["Tipo de Contrato"].unique())
tipo_seleccionado = st.selectbox("Selecciona un Tipo de Contrato:", tipos)

# Filtrar datos según selección
df_filtrado = df[df["Tipo de Contrato"] == tipo_seleccionado]

# Crear pestañas
tab1, tab2 = st.tabs(["📈 Gráfica", "📋 Tabla"])

# TAB 1: Gráfica - número de contratos por entidad para el tipo seleccionado
tab1.subheader(f"Número de contratos de tipo '{tipo_seleccionado}' por entidad")
conteo_por_entidad = df_filtrado["Nombre Entidad"].value_counts()
tab1.bar_chart(conteo_por_entidad)

# TAB 2: Tabla con contratos filtrados
tab2.subheader(f"Contratos de tipo '{tipo_seleccionado}'")
tab2.write(f"{len(df_filtrado)} contratos encontrados")
tab2.dataframe(df_filtrado)



st.title("📑 Contratos por Modalidad de Contratación")

# Asegurar que no haya valores nulos en la columna clave
df = df.dropna(subset=["Modalidad de Contratacion"])

# Selector de modalidad (fuera de las tabs para mejor UX)
modalidades = sorted(df["Modalidad de Contratacion"].unique())
modalidad_seleccionada = st.selectbox("Selecciona una modalidad:", modalidades)

# Filtrar dataframe según modalidad seleccionada
df_filtrado = df[df["Modalidad de Contratacion"] == modalidad_seleccionada]

# Crear tabs
tab1, tab2 = st.tabs(["📊 Gráfica", "📋 Tabla filtrada"])

with tab1:
    st.subheader(f"Distribución de contratos para modalidad: {modalidad_seleccionada}")
    # Para la gráfica puedes mostrar la cantidad de contratos por alguna otra variable, 
    # por ejemplo por "Nombre Entidad"
    conteo_por_entidad = df_filtrado["Nombre Entidad"].value_counts()
    st.bar_chart(conteo_por_entidad)

with tab2:
    st.subheader(f"Contratos para modalidad: {modalidad_seleccionada}")
    st.write(f"{len(df_filtrado)} contratos encontrados")
    st.dataframe(df_filtrado)



st.header("Análisis por Ciudad")

# Selección de ciudad
ciudades = sorted(df["Ciudad"].dropna().unique())
ciudad_seleccionada = st.selectbox("Selecciona una ciudad:", ciudades)

# Filtrar datos por ciudad seleccionada
df_filtrado = df[df["Ciudad"] == ciudad_seleccionada]

# Crear pestañas
tab1, tab2 = st.tabs(["📊 Contratos por Modalidad", "📋 Tabla de contratos"])

with tab1:
    st.subheader(f"Cantidad de contratos por modalidad en {ciudad_seleccionada}")
    conteo_modalidad = df_filtrado["Modalidad de Contratacion"].value_counts()
    st.bar_chart(conteo_modalidad)

with tab2:
    st.subheader(f"Contratos en {ciudad_seleccionada}")
    st.write(f"{len(df_filtrado)} contratos encontrados")
    st.dataframe(df_filtrado)



st.title("Contratos por Estado")

# Asegurar que la columna "Estado Contrato" no tenga valores nulos
df = df.dropna(subset=["Estado Contrato"])

# Obtener los valores únicos para el selectbox
estados = sorted(df["Estado Contrato"].unique())
estado_seleccionado = st.selectbox("Selecciona un Estado de Contrato:", estados)

# Filtrar los datos según el estado seleccionado
df_filtrado = df[df["Estado Contrato"] == estado_seleccionado]

# Crear pestañas
tab1, tab2 = st.tabs(["📈 Gráfica", "📋 Tabla"])

# TAB 1: Gráfica (por ejemplo, número de contratos por entidad)
tab1.subheader(f"Número de contratos en estado '{estado_seleccionado}' por entidad")
conteo_por_entidad = df_filtrado["Nombre Entidad"].value_counts()
tab1.bar_chart(conteo_por_entidad)

# TAB 2: Tabla de contratos filtrados
tab2.subheader(f"Contratos en estado '{estado_seleccionado}'")
tab2.write(f"{len(df_filtrado)} contratos encontrados")
tab2.dataframe(df_filtrado)




# Luego convertir a entero (si hay nulos, usa 'Int64')
# df['Valor del Contrato'] = df['Valor del Contrato'].astype('Int64')
df['Valor_limpio'] = (
    df['Valor del Contrato']
    .str.replace(r'[$,]', '', regex=True)  # quitar '$' y ','
    .astype(int)                           # convertir a entero
)


filtro_ciudad=df["Ciudad"].unique()
ciudades = st.multiselect(
    "Ciudades", filtro_ciudad,
    default=filtro_ciudad
)

filtro_1= df[["Ciudad", "Valor_limpio"]]
filtro_c= filtro_1[filtro_1['Ciudad'].isin(ciudades)]

# st.dataframe(filtro_c)

# Graficar el DataFrame con un gráfico de barras
st.bar_chart(filtro_c.set_index('Ciudad'))

