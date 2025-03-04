import streamlit as st
import math

st.set_page_config(page_title="Calculadora Chat", layout="centered")

# CSS inline para el estilo "chat"
chat_style = """
<style>
.chat-container {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background-color: #fff;
    display: flex;
    flex-direction: column;
    height: 550px;
    overflow: hidden;
}

.chat-window {
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    background-color: #f8f9fa;
}

.message {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 10px;
    max-width: 75%;
    word-wrap: break-word;
}

.user {
    background-color: #d1e7dd; /* Verde claro */
    margin-left: auto;
    margin-right: 0;
    text-align: right;
    border-bottom-right-radius: 0;
}

.bot {
    background-color: #f8d7da; /* Rojo claro */
    margin-right: auto;
    margin-left: 0;
    text-align: left;
    border-bottom-left-radius: 0;
}

.input-area {
    display: flex;
    padding: 10px;
    border-top: 1px solid #dee2e6;
    background-color: #ffffff;
}

.input-text {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.send-button {
    padding: 10px 20px;
    font-size: 16px;
    margin-left: 10px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: #fff;
    cursor: pointer;
}

.send-button:hover {
    background-color: #0056b3;
}
</style>
"""

st.markdown(chat_style, unsafe_allow_html=True)


# ------------------ Manejo de estado ------------------
if "messages" not in st.session_state:
    # Lista de tuplas (sender, text)
    st.session_state["messages"] = []

if "chat_input" not in st.session_state:
    # Contenido actual del cuadro de texto
    st.session_state["chat_input"] = ""


# ------------------ Función Callback ------------------
def enviar_mensaje():
    """Se llama cuando el usuario hace clic en 'Enviar'."""
    # Obtener texto que el usuario escribió
    user_text = st.session_state["chat_input"].strip()
    if not user_text:
        return  # No hacer nada si la entrada está vacía

    # Agregar mensaje del usuario al historial
    st.session_state["messages"].append(("user", user_text))

    # Intentar evaluar la operación en un entorno limitado
    allowed_names = {"math": math}
    try:
        result = eval(user_text, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        result = f"Error: {e}"

    # Agregar respuesta al historial
    st.session_state["messages"].append(("bot", str(result)))

    # Limpiar el contenido del input
    st.session_state["chat_input"] = ""


# ------------------ Interfaz del Chat ------------------
# Contenedor del Chat: abrimos con HTML
st.markdown("""
<div class="chat-container">
    <div class="chat-window" id="chat-window">
""", unsafe_allow_html=True)

# Mostrar los mensajes
for sender, text in st.session_state["messages"]:
    sender_class = "user" if sender == "user" else "bot"
    st.markdown(f'<div class="message {sender_class}">{text}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # cierra .chat-window

# Input y botón en la misma "fila"
# Usamos label= para dar un nombre accesible, y label_visibility="collapsed" para ocultarlo visualmente
st.text_input(
    "Ingresar operación",
    key="chat_input",
    label_visibility="collapsed",
    placeholder="Ej: 2+2, math.sqrt(9), etc."
)
st.button("Enviar", on_click=enviar_mensaje)

# Cerramos el .chat-container
st.markdown("</div>", unsafe_allow_html=True)
