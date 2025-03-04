import streamlit as st
import math

st.set_page_config(page_title="Calculadora Chat", layout="centered")

# CSS inline con estilo mejorado
chat_style = """
<style>
body {
    background-color: #e9ecef; /* Fondo gris claro */
}

/* Contenedor padre para centrar el chat y darle espacio superior */
.chat-page-container {
    max-width: 600px;
    margin: 3rem auto; /* 3rem de margen arriba y abajo, auto a los lados */
}

/* Título alineado al centro */
.chat-title {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #343a40;
    font-weight: 600;
    font-size: 1.5rem;
}

/* Contenedor principal del "chat" */
.chat-container {
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background-color: #fff;
    display: flex;
    flex-direction: column;
    height: 500px; /* altura fija */
    overflow: hidden;
}

/* Zona donde se muestran los mensajes */
.chat-window {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    background-color: #f8f9fa;
    display: flex;
    flex-direction: column; /* orden normal: de arriba a abajo */
    justify-content: flex-start; 
}

/* Burbujas de mensaje */
.message {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 10px;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 0.9rem;
}

.user {
    background-color: #d1e7dd; /* Verde claro */
    margin-left: auto;
    text-align: right;
    border-bottom-right-radius: 0;
}

.bot {
    background-color: #f8d7da; /* Rojo claro */
    margin-right: auto;
    text-align: left;
    border-bottom-left-radius: 0;
}

/* Barra inferior con el input y el botón */
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

# ----------- Manejo de estado -----------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chat_input" not in st.session_state:
    st.session_state["chat_input"] = ""

# ----------- Callback para enviar mensaje -----------
def enviar_mensaje():
    """Función que se llama al presionar el botón 'Enviar'."""
    user_text = st.session_state["chat_input"].strip()
    if not user_text:
        return  # No enviar si está vacío
    # Agregar mensaje del usuario
    st.session_state["messages"].append(("user", user_text))
    # Evaluar en Python
    allowed_names = {"math": math}
    try:
        result = eval(user_text, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        result = f"Error: {e}"
    # Agregar respuesta del "bot"
    st.session_state["messages"].append(("bot", str(result)))
    # Limpiar input
    st.session_state["chat_input"] = ""

# ----------- Estructura de la página -----------
st.markdown("<div class='chat-page-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='chat-title'>Calculadora Chat</h2>", unsafe_allow_html=True)

# Contenedor principal del chat
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Ventana de mensajes
st.markdown("<div class='chat-window'>", unsafe_allow_html=True)
for sender, text in st.session_state["messages"]:
    sender_class = "user" if sender == "user" else "bot"
    st.markdown(f"<div class='message {sender_class}'>{text}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input + Botón
input_col, btn_col = st.columns([4, 1])
with input_col:
    st.text_input(
        "Ingresa operación",
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Ej: 2+2, math.sqrt(9), etc."
    )
with btn_col:
    st.button("Enviar", on_click=enviar_mensaje)

st.markdown("</div>", unsafe_allow_html=True)  # Cierra .chat-container
st.markdown("</div>", unsafe_allow_html=True)  # Cierra .chat-page-container
