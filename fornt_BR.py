import streamlit as st
import pandas as pd
import numpy as np
import duckdb
import zipfile
import os
from funciones_gen import get_emojis, assigne_emoj, modelo, get_genders
import plotly.express as px

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
    # selected_tab = st.sidebar.radio("", ["🧑‍🚀 Ficha de cliente", "🛠️ Soporte", "📊 Visualización de Datos"])
    selected_tab = st.sidebar.radio("", ["🎵 Selección de Géneros Musicales","📊 Visualización de Datos", ])

    if selected_tab == "🎵 Selección de Géneros Musicales":
        # Listado de géneros musicales
        generos = get_genders()
        # Permitir al usuario elegir hasta 3 géneros musicales
        generos_elegidos = st.multiselect("Elige 3 géneros musicales favoritos:", generos, default=None)
    
        # Validar que exactamente 3 géneros han sido elegidos
        if len(generos_elegidos) != 3:
            st.error("Debes seleccionar exactamente 3 géneros.")
        else:
            # Calificaciones para los géneros seleccionados
            calificaciones = {}
            st.write("Califica los géneros elegidos del 1 al 10:")
            for genero in generos_elegidos:
                calificaciones[genero] = st.slider(f"Calificación para {genero}:", 1, 10, 5)
    
            # Botón para obtener la recomendación
            if st.button("Obtener Recomendación"):
                # Supongamos que la función modelo genera una recomendación basada en los géneros y sus calificaciones
                recomendacion = modelo(calificaciones)
                st.write("Canción recomendada:", recomendacion)
    
            # Botón para mostrar las tres peores calificaciones
            if st.button("Mostrar Bottom 3"):
                # Ordenar calificaciones por valor y tomar las tres menores
                bottom_3 = sorted(calificaciones.items(), key=lambda x: x[1])[:3]
                st.write("Tres géneros con menor calificación:")
                for genero, calificacion in bottom_3:
                    st.write(f"{genero}: {calificacion}")

    elif selected_tab == "🧑‍🚀 Ficha de cliente":
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

    elif selected_tab == "📊 Visualización de Datos":
        # Cargar el conjunto de datos 'gapminder' con Plotly Express
        df = px.data.gapminder()
        
        # Permitir al usuario seleccionar un año para filtrar los datos
        year_options = df['year'].unique().tolist()
        year = st.selectbox('Which year would you like to see?', year_options, 0)
        # df_year_filtered = df[df['year'] == year]
        
        # Crear y mostrar un gráfico de dispersión con los datos filtrados
        fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                         hover_name="country", log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90],
                        animation_frame='year', animation_group='country')
        fig.update_layout(width=800)
        st.write(fig)
        
        # Leer datos de COVID-19 desde un CSV en línea
        covid_url = 'https://raw.githubusercontent.com/shinokada/covid-19-stats/master/data/daily-new-confirmed-cases-of-covid-19-tests-per-case.csv'
        covid = pd.read_csv(covid_url)
        covid.columns = ['Country', 'Code', 'Date', 'Confirmed', 'Days since confirmed']
        covid['Date'] = pd.to_datetime(covid['Date']).dt.strftime('%Y-%m-%d')
        
        # Permitir al usuario seleccionar una fecha y países para filtrar los datos de COVID-19
        date_options = covid['Date'].unique().tolist()
        date = st.selectbox('Which date would you like to see?', date_options, 100)
        country_options = covid['Country'].unique().tolist()
        country = st.multiselect('Which country would you like to see?', country_options, ['Brazil'])
        
        # Filtrar los datos de COVID-19 por país y fecha
        covid_filtered = covid[covid['Country'].isin(country)]
        # covid_filtered = covid_filtered[covid_filtered['Date'] == date]
        
        # Crear y mostrar un gráfico de barras con los datos filtrados de COVID-19
        fig2 = px.bar(covid_filtered, x="Confirmed", y="Country", color="Country", orientation='h', range_x=[0,35000],
                     animation_frame='Date', animation_group='Country')
        
        # fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
        # fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
        fig2.update_layout(width=800)
        st.write(fig2)

if __name__ == '__main__':
    main()
