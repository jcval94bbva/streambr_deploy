import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import duckdb
import os

# Importa tus funciones personalizadas (ajusta a tu necesidad real)
from funciones_gen import (
    get_emojis,
    assigne_emoj,
    modelo,
    get_genders,
    centroide_ponderado,
    call_predict_function
)

def main():
    st.set_page_config(page_title="Recomendador Musical", layout="wide")

    # Ruta de la carpeta donde se ubican los datos
    carpeta_destino = 'Data_'
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Carga de datos
    data_centroides = pd.read_csv(os.path.join(carpeta_destino, 'centroides_generos.csv'))
    
    # Ejemplo de uso de funciones
    emoj = get_emojis()
    
    # Conexión a DuckDB (si la requieres)
    con = duckdb.connect(database=':memory:')
    con.register('data_bajio', data_centroides)
    
    # Carga del HTML
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    # Muestra el HTML en la aplicación
    # Ajusta la altura según lo necesites
    components.html(html_code, height=1500, scrolling=True)

    # =========================================
    # NOTA IMPORTANTE:
    #
    # Tal como está, el HTML y el JS trabajan de forma
    # independiente al código Python. Para que la lógica
    # de recomendación real (modelo, call_predict_function, etc.)
    # se ejecute en Python, necesitarás un mecanismo de
    # comunicación (ej: fetch a un endpoint, un custom
    # component, o recargar la página con query params).
    #
    # Esta estructura separa la interfaz (HTML) del backend
    # (Python), pero requiere más configuración si quieres
    # un flujo completamente integrado.
    # =========================================

if __name__ == '__main__':
    main()
