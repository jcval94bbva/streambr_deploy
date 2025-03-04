import streamlit as st
import streamlit.components.v1 as components

# Declarar el custom component; se asume que el frontend del componente se encuentra en calc_chat_component/public
calc_chat = components.declare_component("calc_chat", path="./calc_chat_component/public")

def main():
    st.set_page_config(page_title="Calculadora Chat", layout="wide")

    # Inicializar historial de chat en la sesión
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Llamar al custom component pasando el historial actual como propiedad.
    # El componente devolverá, si el usuario ha enviado un mensaje, ese mensaje.
    new_message = calc_chat(chat_history=st.session_state.chat_history, default="")

    # Si se recibió un nuevo mensaje, se procesa en Python
    if new_message:
        st.write("Nuevo mensaje recibido:", new_message)
        try:
            # Evaluar la operación matemática.
            # Se usa eval con un entorno limitado (solo se permite acceder a math)
            import math
            # Nota: eval es peligroso si se le permite evaluar expresiones arbitrarias.
            # En un entorno real, se debe usar una función de evaluación segura.
            result = eval(new_message, {"__builtins__": {}}, {"math": math})
        except Exception as e:
            result = f"Error: {e}"
        # Agregar el mensaje del usuario y la respuesta del bot al historial
        st.session_state.chat_history.append({"sender": "user", "message": new_message})
        st.session_state.chat_history.append({"sender": "bot", "message": str(result)})

    # (Opcional) Mostrar el historial de chat en Streamlit para depuración
    st.write("Historial de chat:", st.session_state.chat_history)

if __name__ == '__main__':
    main()
