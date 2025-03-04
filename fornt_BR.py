import streamlit as st
import streamlit.components.v1 as components

# Declaramos el componente con un nombre cualquiera ("calc_chat")
# y la ruta relativa a la carpeta "public" de tu componente.
calc_chat = components.declare_component(
    "calc_chat",
    path="./chat_component/public"
)

def main():
    st.set_page_config(page_title="Calculadora Chat", layout="centered")

    st.write("Hola desde la app principal")

    # Llamamos al componente y recogemos lo que retorne (texto escrito por el usuario)
    user_input = calc_chat()  
    # Si el usuario envía algo, lo mostramos
    if user_input:
        st.write(f"El usuario envió: {user_input}")

if __name__ == "__main__":
    main()
