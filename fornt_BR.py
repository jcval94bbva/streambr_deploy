import streamlit as st
import pandas as pd
import numpy as np
import duckdb
import zipfile
import os
from funciones_gen import get_emojis, assigne_emoj, modelo, get_genders, centroide_ponderado, call_predict_function
import plotly.express as px

def main():
    
    # Ruta de la carpeta donde se descomprimirán los archivos
    carpeta_destino = 'Data_'
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # -----Fin Descompresión de datos-----

    # Lectura de datos
    data_centroides = pd.read_csv(carpeta_destino+'/centroides_generos.csv')
    

    emoj = get_emojis()
    # Inicializar una conexión DuckDB
    con = duckdb.connect(database=':memory:')
    # Cargar el DataFrame en DuckDB para que se puedan hacer consultas
    con.register('data_bajio', data_centroides)

    # Menú del lado izquierdo
    st.sidebar.title("Menú")
    
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
                calificaciones[genero] = st.slider(f"Calificación para {genero}:", 1, 10, 8)
    
            # Botón para obtener la recomendación
            if st.button("Obtener Recomendación"):
                # Supongamos que la función modelo genera una recomendación basada en los géneros y sus calificaciones
                recomendacion = modelo(calificaciones)
                st.write("A través de este diccionario", calificaciones)

                gg = [k for k, v in calificaciones.items()]
                pesos  = [v for k, v in calificaciones.items()]
                
                
                posicipon_espacio_cancion = centroide_ponderado(gg, pesos, data_centroides)

                st.write("Encontramos un punto en el espacio de las canciones", posicipon_espacio_cancion)

                st.write("Pero para que ese punto haga sentido, usaremos una API de GCP que nos diga todos sus secretos")

                st.write("[Notebook](https://colab.research.google.com/drive/1rnYxUtNQ1GesDJ1n3fqJ2dyQBdsLb7XR#scrollTo=kRTze_zl76-I)")

                recomendacion = call_predict_function(posicipon_espacio_cancion[0], posicipon_espacio_cancion[1])
                
                st.write("Canción recomendada:", recomendacion)
        
            # Botón para mostrar las tres peores calificaciones
            # if st.button("Mostrar Bottom 3"):
            #     # Ordenar calificaciones por valor y tomar las tres menores
            #     bottom_3 = sorted(calificaciones.items(), key=lambda x: x[1])[:3]
            #     st.write("Tres géneros con menor calificación:")
            #     for genero, calificacion in bottom_3:
            #         st.write(f"{genero}: {calificacion}")

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
