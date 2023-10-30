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
    st.title("Cliente Ideal")

    # Menú del lado izquierdo
    st.sidebar.title("Menú")

    # Nueva pestaña para la imagen
    st.sidebar.title("Pestañas")
    selected_tab = st.sidebar.radio("Selecciona una pestaña:", ["Exploración de Datos", "Imagen"])

    if selected_tab == "Exploración de Datos":
        # Muestra del conjunto de datos
        st.subheader("Muestra del conjunto de datos bajio")
        st.write(data_bajio.head())

        # Agregar el inputbox
        input_text = st.text_input("Ingrese hasta 8 caracteres:", max_chars=8)

        if input_text:
            # Filtrar la columna 'cliente' basándonos en el input
            filtered_data_bajio = data_bajio[data_bajio['customer_id'].str.contains(input_text)]
            st.write("Resultados filtrados:")
            st.write(filtered_data_bajio)

        # Seleccionar una columna para visualizar
        columna_seleccionada = st.selectbox("Selecciona una columna:", data.columns)

        # Campo de entrada de texto para la consulta SQL
        consulta_sql = st.text_area("Introduce tu consulta SQL:", value='SELECT * FROM data WHERE MedHouseVal > 1')

        # Botón para ejecutar la consulta SQL
        if st.button("Ejecutar Consulta SQL"):
            if consulta_sql:
                try:
                    # Ejecutar una consulta SQL en el DataFrame
                    result = con.execute(consulta_sql)
                    # Obtener el resultado como un DataFrame de Pandas
                    result_df = result.fetchdf()
                    st.write("Resultado de la consulta:")
                    st.write(result_df)
                except Exception as e:
                    st.write("Ocurrió un error al ejecutar la consulta:", e)

        # Estadísticas descriptivas
        st.subheader("Estadísticas descriptivas")
        st.write(data.describe())

        # Filtrar y mostrar datos específicos
        st.subheader("Filtrar datos")
        filtro = st.slider("Filtrar por precio (target):", float(data[target].min()), float(data[target].max()))
        filtered_data = data[data[target] < filtro]
        st.write(filtered_data)

    elif selected_tab == "Imagen":
        # Pestaña para mostrar la imagen
        st.image("images/mi_imagen.png")

if __name__ == '__main__':
    main()
