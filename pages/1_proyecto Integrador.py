import pandas as pd
import streamlit as st
import requests

# Realizar petición GET a la API
response = requests.get('https://68d557d8e29051d1c0ae4638.mockapi.io/usuario')

# Verificar que la petición fue exitosa
if response.status_code == 200:
    # Convertir la respuesta JSON a DataFrame
    data = response.json()
    df = pd.DataFrame(data)

    st.dataframe(df)
else:
    print(f"Error en la petición: {response.status_code}")