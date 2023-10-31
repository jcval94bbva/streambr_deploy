import streamlit as st
import pandas as pd
import numpy as np
import duckdb
import zipfile
import os
from funciones_gen import get_emojis, assigne_emoj

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

    emoj = get_emojis()
    # Inicializar una conexión DuckDB
    con = duckdb.connect(database=':memory:')
    # Cargar el DataFrame en DuckDB
    con.register('data_bajio', data_bajio)

    # Menú del lado izquierdo
    st.sidebar.title("Menú")
    selected_tab = st.sidebar.radio("", ["🧑‍🚀 Ficha de cliente", "🛠️ Soporte"])

    if selected_tab == "🧑‍🚀 Ficha de cliente":
        # Crear dos columnas en una fila
        # Crear una fila con dos elementos
        left_column, right_column = st.columns(2)
        
        # Agregar la imagen a la columna izquierda
        
        input_text = left_column.text_input("Ingrese el No. de cliente (puedes omitir los 0's):", max_chars=8)
        input_text = input_text.zfill(8)
        
        # Agregar el input_text a la columna derecha
    
        if input_text:
            # Filtrar la columna 'cliente' basándonos en el input
            filtered_data_bajio = data_bajio[data_bajio['customer_id'].str.contains(input_text)].drop(columns=['customer_id','DIVISION'])
            # Definir una función para formatear las filas
            def formato_fila(fila):
                return ' \n'.join([f'{i+1}. {valor}' for i, valor in enumerate(fila)])
                
            filtered_data_bajio['formatted'] = filtered_data_bajio.apply(formato_fila, axis=1)
            
            if len(filtered_data_bajio) > 0:
                right_column.write("Información del cliente "+input_text+':')
                emoj_most__ = assigne_emoj(str(filtered_data_bajio['formatted'].values[0]),emoj)
                right_column.write(emoj_most__)
            else:
                right_column.write("No se encuentra el cliente, se enviará un reporte al operador")
            st.write("")
            try:
                prodo = str(filtered_data_bajio['MEJOR_PRODUCTO_1'].values[0])
            except:
                prodo = ''
            st.write('El mejor producto para este cliente es: '+prodo)
            
        # Agregar un inputbox para comentarios
        comentario = st.text_input("Añadir un comentario:")
        guardar_boton = st.button("Guardar")

        # Lista para almacenar los comentarios
        comentarios = []
        if guardar_boton and comentario:
            comentarios.append(comentario)
            st.write("Comentario guardado")
            # Limpiar el inputbox
            comentario = ""

    elif selected_tab == "🛠️ Soporte":
        # Pestaña para mostrar la imagen
        st.image("images/mi_imagen.png")

if __name__ == '__main__':
    main()
