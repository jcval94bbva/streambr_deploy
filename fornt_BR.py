import streamlit as st
import streamlit.components.v1 as components
import math

# 1. Registrar el Custom Component
#    path debe apuntar a la carpeta "public" de tu componente
my_chat_component = components.declare_component(
    "my_chat_component",
    path="./chat_component/public"
)

# 2. Manejo del historial de chat
if "messages" not in st.session_state:
    # Guardamos una lista de tuplas (sender, text), ej. ("user", "2+2")
    st.session_state["messages"] = []

def process_message(user_input: str) -> str:
    """
    Procesa la operación matemática en Python usando eval
    con un entorno muy limitado. Retorna el resultado como string.
    """
    allowed_names = {"math": math}  # Solo exponemos 'math'
    try:
        result = eval(user_input, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        result = f"Error: {e}"
    return str(result)

def main():
    st.title("Calculadora Chat con Custom Component")

    # 3. Llamar al componente, pasando el historial como propiedad
    new_message = my_chat_component(chat_history=st.session_state["messages"])

    # 4. Si el usuario ha enviado un mensaje nuevo
    if new_message:
        # Agregamos el mensaje del usuario
        st.session_state["messages"].append(("user", new_message))
        # Procesamos la operación en Python
        response = process_message(new_message)
        # Agregamos la respuesta del "bot"
        st.session_state["messages"].append(("bot", response))

    # (Opcional) Mostrar el historial en la app para depuración
    st.write("Historial de chat:", st.session_state["messages"])

if __name__ == "__main__":
    main()
