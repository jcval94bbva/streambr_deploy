import streamlit as st
import pandas as pd
import numpy as np
import duckdb
import zipfile
import os
from sklearn.datasets import fetch_california_housing

def main():

    # -----Descompresión de datos-----
    archivo_zip = 'divisiones.zip'
    archivo_zip = 'Data_/divisiones.zip'
    
    # Ruta de la carpeta donde se descomprimirán los archivos
    carpeta_destino = 'Data_/divisiones_descomprimidas'
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Descomprimir el archivo ZIP
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        zip_ref.extractall(carpeta_destino)
    # -----Fin Descompresión de datos-----

    # Lectura de datos
    data_bajio = pd.read_csv(carpeta_destino+'/BAJIO/df_crm.csv')
    data_bajio = data_bajio[[x for x in data_bajio.columns if 'unnam' not in x.lower()]]
    
    # Cargar el conjunto de datos de viviendas de California
    housing = fetch_california_housing()

    # Crear un DataFrame de pandas con los datos
    data = pd.DataFrame(data=housing.data, columns=housing.feature_names)

    # Agregar la columna objetivo (target) al DataFrame
    data['MedHouseVal'] = housing.target

    # Inicializar una conexión DuckDB
    con = duckdb.connect(database=':memory:')
    # Cargar el DataFrame en DuckDB
    con.register('data', data)
    con.register('data_bajio', data_bajio)

    # Título de la aplicación
    st.title("Ficha de cliente Ideal")

    # Menú del lado izquierdo
    st.sidebar.title("Menú")

    # Nueva pestaña para la imagen
    st.sidebar.title("Pestañas")
    selected_tab = st.sidebar.radio("Selecciona una pestaña:", ["🧑‍🚀 Ficha de cliente", "🛠️ Soporte"])

    if selected_tab == "Ficha de cliente":
        # Agregar el inputbox
        input_text = st.text_input("Ingrese el No. de cliente (puedes omitir los 0's iniciales 00000123 ➡️ 123):", max_chars=8)
        input_text = input_text.zfill(8)

        if input_text:
            # Filtrar la columna 'cliente' basándonos en el input
            filtered_data_bajio = data_bajio[data_bajio['customer_id'].str.contains(input_text)]
            if len(filtered_data_bajio)>0:
                st.write("Información de tu cliente:")
                st.write(filtered_data_bajio)
            else:
                st.write("No se encuentra el cliente, se enviará un reporte al operador")

    elif selected_tab == "Soporte":
        # Pestaña para mostrar la imagen
        st.image("images/mi_imagen.png")

if __name__ == '__main__':
    main()
