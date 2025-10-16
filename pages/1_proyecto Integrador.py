import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================
st.set_page_config(
    page_title="Incidentes viales Medellín",
    layout="wide",
    page_icon="🚦"
)

st.title("🚦 Análisis de víctimas en incidentes viales - Medellín")

# ==========================
# CARGA Y LIMPIEZA DE DATOS
# ==========================
@st.cache_data
def cargar_datos(ruta):
    """Carga el CSV en fragmentos y los combina en un solo DataFrame."""
    chunk_size = 10000
    chunks = pd.read_csv(ruta, encoding="utf-8", chunksize=chunk_size)
    df = pd.concat(chunks)

    # Conversión de tipos de datos
    df["Fecha_incidente"] = pd.to_datetime(df["Fecha_incidente"], errors="coerce")
    df["Edad"] = pd.to_numeric(df["Edad"], errors="coerce")

    # Eliminar filas sin fecha
    df = df.dropna(subset=["Fecha_incidente"])

    return df

# --- Cargar los datos ---
df = cargar_datos("data/Mede_Victimas_inci.csv")
st.success(f"✅ Datos cargados correctamente. Total de filas: {len(df):,}")

# Avisar si hay edades no válidas
edad_nulas = df["Edad"].isna().sum()
if edad_nulas > 0:
    st.warning(f"⚠️ Se encontraron {edad_nulas:,} valores de 'Edad' no válidos (convertidos a NaN).")

# ==========================
# FILTROS EN SIDEBAR
# ==========================
st.sidebar.header("Filtros de análisis")

años_disponibles = sorted(df["Fecha_incidente"].dt.year.dropna().unique())
año = st.sidebar.selectbox("Año del incidente", años_disponibles)

sexo = st.sidebar.multiselect(
    "Sexo",
    options=sorted(df["Sexo"].dropna().unique()),
    default=sorted(df["Sexo"].dropna().unique())
)

gravedad = st.sidebar.multiselect(
    "Gravedad víctima",
    options=sorted(df["Gravedad_victima"].dropna().unique()),
    default=sorted(df["Gravedad_victima"].dropna().unique())
)

# ==========================
# FILTRAR DATOS
# ==========================
df_filtrado = df[
    (df["Fecha_incidente"].dt.year == año)
    & (df["Sexo"].isin(sexo))
    & (df["Gravedad_victima"].isin(gravedad))
]

# ==========================
# ESTADÍSTICAS GENERALES
# ==========================
st.subheader(f"📅 Estadísticas para el año {año}")

col1, col2 = st.columns(2)
col1.metric("Total de víctimas", f"{len(df_filtrado):,}")

edad_promedio = (
    round(df_filtrado["Edad"].mean(), 1)
    if df_filtrado["Edad"].notna().sum() > 0 else "N/D"
)
col2.metric("Edad promedio", edad_promedio)



st.subheader("📊 Indicadores clave")

col_a, col_b, col_c = st.columns(3)

col_a.metric("🚦 Total incidentes", df_filtrado["Clase_incidente"].nunique())
col_b.metric("⚰️ Muertes", (df_filtrado["Gravedad_victima"] == "Muertos").sum())
col_c.metric("🏥 Heridos", (df_filtrado["Gravedad_victima"] == "Heridos").sum())


# ==========================
# GRÁFICOS PRINCIPALES
# ==========================
col1, col2 = st.columns(2)

# --- Distribución por sexo y gravedad ---
with col1:
    fig1 = px.histogram(
        df_filtrado,
        x="Sexo",
        color="Gravedad_victima",
        barmode="group",
        title="Distribución de víctimas por sexo y gravedad",
        labels={"Sexo": "Sexo", "count": "Cantidad de víctimas"}
    )
    st.plotly_chart(fig1, use_container_width=True)

# --- Tipos de incidentes ---
with col2:
    # Contar los tipos de incidentes
    tipos = (
        df_filtrado["Clase_incidente"]
        .value_counts()
        .reset_index()
    )

    # Renombrar columnas de forma segura
    tipos.columns = ["Tipo_incidente", "Cantidad"]

    # Crear el gráfico
    fig2 = px.bar(
        tipos,
        x="Tipo_incidente",
        y="Cantidad",
        title="Tipos de incidentes más comunes",
        labels={"Tipo_incidente": "Tipo de incidente", "Cantidad": "Número de víctimas"}
    )
    st.plotly_chart(fig2, use_container_width=True)


# ==========================
# DISTRIBUCIÓN DE EDADES
# ==========================
st.subheader("👶 Distribución de edades de las víctimas")
fig3 = px.histogram(
    df_filtrado,
    x="Edad",
    nbins=20,
    color="Gravedad_victima",
    title="Distribución de edades por gravedad de la víctima",
    labels={"Edad": "Edad (años)", "count": "Número de víctimas"}
)
st.plotly_chart(fig3, use_container_width=True)

# ==========================
# DISTRIBUCIÓN POR HORA
# ==========================

# --- Distribución por hora del día ---
st.subheader("🕒 Distribución de incidentes por hora del día")

# Convertir la hora a formato datetime y extraer solo la hora (0–23)
df_filtrado["Hora_incidente"] = pd.to_datetime(df_filtrado["Hora_incidente"], format="%H:%M:%S", errors="coerce").dt.hour

# Agrupar por hora
horas = df_filtrado.groupby("Hora_incidente").size().reset_index(name="Cantidad")

# Eliminar valores nulos o fuera de rango
horas = horas.dropna()
horas = horas[horas["Hora_incidente"].between(0, 23)]

# Gráfico
fig5 = px.line(
    horas,
    x="Hora_incidente",
    y="Cantidad",
    markers=True,
    title="Cantidad de víctimas según la hora del día",
    labels={"Hora_incidente": "Hora del incidente", "Cantidad": "Número de víctimas"}
)
st.plotly_chart(fig5, use_container_width=True)



# --- MAPA DE INCIDENTES EN MEDELLÍN ---
st.subheader("🗺️ Mapa de incidentes en Medellín")

# Limpiar coordenadas
df_filtrado["Latitud"] = (
    df_filtrado["Latitud"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.replace("Sin Inf", "", regex=False)
)
df_filtrado["Longitud"] = (
    df_filtrado["Longitud"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.replace("Sin Inf", "", regex=False)
)

# Convertir a números y eliminar nulos
df_filtrado["Latitud"] = pd.to_numeric(df_filtrado["Latitud"], errors="coerce")
df_filtrado["Longitud"] = pd.to_numeric(df_filtrado["Longitud"], errors="coerce")
df_mapa = df_filtrado.dropna(subset=["Latitud", "Longitud"])

# Verificar que haya datos válidos
if df_mapa.empty:
    st.warning("⚠️ No hay datos válidos de ubicación para mostrar en el mapa.")
else:
    fig_mapa = px.scatter_mapbox(
        df_mapa,
        lat="Latitud",
        lon="Longitud",
        hover_name="Clase_incidente",
        hover_data=["Barrio", "Fecha_incidente", "Gravedad_victima"],
        color="Clase_incidente",
        zoom=11,
        height=550
    )
    fig_mapa.update_layout(mapbox_style="carto-positron")
    fig_mapa.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_mapa, use_container_width=True)




    st.subheader("📈 Evolución mensual de víctimas")

df_filtrado["Mes"] = df_filtrado["Fecha_incidente"].dt.month
mensual = df_filtrado.groupby("Mes").size().reset_index(name="Cantidad")

fig_mes = px.line(
    mensual,
    x="Mes",
    y="Cantidad",
    markers=True,
    title="Evolución mensual de víctimas durante el año",
    labels={"Mes": "Mes", "Cantidad": "Número de víctimas"}
)
st.plotly_chart(fig_mes, use_container_width=True)




st.subheader("📅 Distribución por día de la semana")

df_filtrado["Día_semana"] = df_filtrado["Fecha_incidente"].dt.day_name()

dias = df_filtrado["Día_semana"].value_counts().reindex([
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]).reset_index()
dias.columns = ["Día_semana", "Cantidad"]

fig7 = px.bar(
    dias,
    x="Día_semana",
    y="Cantidad",
    title="Cantidad de víctimas por día de la semana",
    labels={"Día_semana": "Día", "Cantidad": "Número de víctimas"}
)
st.plotly_chart(fig7, use_container_width=True)


# ==========================
# 🧠 CONCLUSIONES AUTOMÁTICAS
# ==========================
st.subheader("🧠 Conclusiones automáticas")

try:
    if df_filtrado.empty:
        st.warning("⚠️ No hay datos disponibles con los filtros seleccionados.")
    else:
        incidente_comun = df_filtrado["Clase_incidente"].value_counts().idxmax()
        sexo_predominante = df_filtrado["Sexo"].value_counts().idxmax()
        grupo_edad = (
            df_filtrado["Grupo_edad"].value_counts().idxmax()
            if "Grupo_edad" in df_filtrado.columns and not df_filtrado["Grupo_edad"].dropna().empty
            else "Sin datos"
        )
        comuna_frecuente = (
            df_filtrado["Comuna"].value_counts().idxmax()
            if "Comuna" in df_filtrado.columns and not df_filtrado["Comuna"].dropna().empty
            else "Sin datos"
        )

        st.markdown(f"""
        📊 En el año **{año}**, el tipo de incidente más común fue **{incidente_comun}**.  
        🚻 El sexo más afectado fue **{sexo_predominante}**.  
        👶 El grupo de edad con más víctimas fue **{grupo_edad}**.  
        📍 La comuna con más incidentes fue **{comuna_frecuente}**.  
        """)
except Exception as e:
    st.error(f"No se pudieron generar conclusiones: {e}")
