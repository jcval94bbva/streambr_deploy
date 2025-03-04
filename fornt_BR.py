import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="Calculadora Chat", layout="wide")
    
    # Cargar el archivo HTML desde la carpeta templates
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    # Inyectar el HTML en la aplicación Streamlit
    components.html(html_code, height=600, scrolling=True)

if __name__ == '__main__':
    main()
