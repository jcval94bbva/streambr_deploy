import streamlit as st
import streamlit.components.v1 as components
import math

# Declaramos el custom component, apuntando a la carpeta "public" dentro de "chat_component"
chat_component = components.declare_component(
    "chat_component",
    path="./chat_component/public"
)

def evaluate_expression(expression: str) -> str:
    """
    Evalúa la expresión matemática usando solo funciones del módulo 'math'.
    Retorna un string con el resultado o un mensaje de error.
    """
    allowed_names = {"math": math}
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def main():
    st.set_page_config(page_title="Calculadora Chat", layout="centered")
    
    # Manejo del historial de mensajes en la sesión
    if "messages" not in st.session_state:
        # Guardamos cada mensaje como una tupla (sender, texto)
        st.session_state["messages"] = []

    # Llamamos al componente, pasándole el historial actual
    user_input = chat_component(messages=st.session_state["messages"])
    # user_input será un string si el usuario escribió algo,
    # o None si no hay nuevo input

    if user_input:
        # El usuario envió un nuevo mensaje
        st.session_state["messages"].append(("user", user_input))
        # Procesamos la expresión en Python
        result = evaluate_expression(user_input)
        # Guardamos la respuesta del "bot"
        st.session_state["messages"].append(("bot", result))

    # (Opcional) Mostrar el historial para depuración
    st.write("Historial de chat:", st.session_state["messages"])

if __name__ == "__main__":
    main()
