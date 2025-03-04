import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="Calculadora Chat", layout="wide")
    
    # Carga del HTML
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    # Inyectar el HTML en la app
    # Ajusta la altura si necesitas más espacio
    components.html(html_code, height=700, scrolling=True)

if __name__ == '__main__':
    main()
