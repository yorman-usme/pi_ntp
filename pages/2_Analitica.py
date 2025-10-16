import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 🔷 CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(page_title="Análisis de Contratos Medellín", layout="wide")

# Título principal
st.title("📊 Análisis de Contratación Pública - Medellín")

# Descripción del proyecto
st.info("""
**Proyecto Integrador - Análisis de Contratación Pública en Medellín**  
Este dashboard permite visualizar y analizar la información de contratos públicos de la ciudad de Medellín.  
Debido al tiempo disponible, se decidió utilizar un archivo CSV como fuente de datos, en lugar de una API.
""")

# ==============================
# 📂 CARGA DE DATOS
# ==============================
try:
    df = pd.read_csv("data/medellin_20250911.csv")
    st.success("✅ Datos cargados correctamente.")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo CSV. Asegúrate de que esté en la carpeta 'data/'.")
    st.stop()

# ==============================
# 🧩 LIMPIEZA Y PREPARACIÓN
# ==============================
# Eliminar filas sin información clave
df = df.dropna(subset=["Nombre Entidad", "Tipo de Contrato", "Modalidad de Contratacion", "Ciudad"])

# Limpieza del valor del contrato
df["Valor_limpio"] = (
    df["Valor del Contrato"]
    .astype(str)
    .str.replace(r"[$,]", "", regex=True)
    .astype(float)
)

# ==============================
# 🔢 KPIs PRINCIPALES
# ==============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🏢 Entidades", df["Nombre Entidad"].nunique())
col2.metric("📜 Contratos totales", len(df))
col3.metric("💰 Valor total (COP)", f"{df['Valor_limpio'].sum():,.0f}")
col4.metric("🏙️ Ciudades únicas", df["Ciudad"].nunique())

st.divider()

# ==============================
# 📈 ANÁLISIS VISUAL
# ==============================
st.header("📈 Análisis visual")
# --- Top 10 entidades con más contratos ---
top_entidades = (
    df["Nombre Entidad"]
    .value_counts()
    .head(10)
    .reset_index()
)

# Renombrar correctamente las columnas
top_entidades.columns = ["Entidad", "Cantidad"]

# Crear gráfico de barras
fig1 = px.bar(
    top_entidades,
    x="Entidad",
    y="Cantidad",
    title="Top 10 entidades con más contratos",
    labels={"Entidad": "Entidad contratante", "Cantidad": "Número de contratos"},
)

# Mostrar gráfico
st.plotly_chart(fig1, use_container_width=True)

# ==============================
# 🔍 FILTROS INTERACTIVOS
# ==============================
st.header("🔍 Filtros interactivos")

# Filtro por tipo de contrato
tipos = sorted(df["Tipo de Contrato"].unique())
tipo_seleccionado = st.selectbox("Selecciona un Tipo de Contrato:", tipos)

# Filtrar
df_filtrado = df[df["Tipo de Contrato"] == tipo_seleccionado]

tab1, tab2 = st.tabs(["📊 Gráfica", "📋 Tabla"])

with tab1:
    conteo_entidad = df_filtrado["Nombre Entidad"].value_counts().head(10)
    st.subheader(f"Top entidades con más contratos de tipo '{tipo_seleccionado}'")
    st.bar_chart(conteo_entidad)

with tab2:
    st.subheader(f"Contratos de tipo '{tipo_seleccionado}'")
    st.write(f"Total: {len(df_filtrado)} registros")
    st.dataframe(df_filtrado)

st.divider()

# ==============================
# 🏙️ ANÁLISIS POR CIUDAD
# ==============================
st.header("🏙️ Análisis por Ciudad")

ciudades = sorted(df["Ciudad"].unique())
ciudad_seleccionada = st.selectbox("Selecciona una Ciudad:", ciudades)

df_ciudad = df[df["Ciudad"] == ciudad_seleccionada]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Modalidades más usadas en {ciudad_seleccionada}")
    conteo_modalidad = df_ciudad["Modalidad de Contratacion"].value_counts().head(10)
    st.bar_chart(conteo_modalidad)

with col2:
    st.subheader(f"Valor total de contratos por entidad en {ciudad_seleccionada}")
    valor_por_entidad = (
        df_ciudad.groupby("Nombre Entidad")["Valor_limpio"].sum().nlargest(10)
    )
    st.bar_chart(valor_por_entidad)

st.divider()

# ==============================
# 🧠 CONCLUSIONES AUTOMÁTICAS
# ==============================
st.header("🧠 Conclusiones automáticas")

total = len(df)
top_entidad = df["Nombre Entidad"].value_counts().idxmax()
top_tipo = df["Tipo de Contrato"].value_counts().idxmax()
ciudad_top = df["Ciudad"].value_counts().idxmax()

st.success(f"""
📍 **Entidad más contratante:** {top_entidad}  
📄 **Tipo de contrato más común:** {top_tipo}  
🏙️ **Ciudad con más contratos:** {ciudad_top}  
📊 **Total de contratos analizados:** {total:,}
""")

# ==============================
# 📎 PIE DE PÁGINA
# ==============================
st.divider()
st.caption("Proyecto desarrollado para análisis académico - Datos abiertos de contratación Medellín.")
