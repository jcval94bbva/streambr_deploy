import streamlit as st
import math

st.set_page_config(page_title="Calculadora Chat", layout="centered")

# CSS para simular chat
chat_style = """
<style>
body {
    background-color: #e9ecef; 
    font-family: Arial, sans-serif;
}
.chat-page-container {
    max-width: 600px;
    margin: 3rem auto; /* margen arriba y auto a los lados */
}
.chat-title {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #343a40;
    font-weight: 600;
    font-size: 1.5rem;
}
.chat-container {
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background-color: #fff;
    display: flex;
    flex-direction: column;
    /* NO altura fija para permitir que crezca con los mensajes */
    padding: 15px;
}
.chat-window {
    /* Ocupa todo el espacio vertical posible menos lo que ocupe el input-area */
    margin-bottom: 1rem;
}
.message {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 10px;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 0.9rem;
}
.user {
    background-color: #d1e7dd; 
    margin-left: auto;
    text-align: right;
    border-bottom-right-radius: 0;
}
.bot {
    background-color: #f8d7da;
    margin-right: auto;
    text-align: left;
    border-bottom-left-radius: 0;
}
/* Ajustes al input y botón */
.input-area {
    display: flex;
    gap: 0.5rem;
}
</style>
"""

st.markdown(chat_style, unsafe_allow_html=True)

# ----------- Manejo de estado -----------
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_input" not in st.session_state:
    st.session_state["chat_input"] = ""

# ----------- Callback -----------
def enviar_mensaje():
    """Función que se llama al presionar el botón 'Enviar'."""
    texto_usuario = st.session_state["chat_input"].strip()
    if not texto_usuario:
        return

    # Agregamos el mensaje del usuario
    st.session_state["messages"].append(("user", texto_usuario))

    # Intentar evaluación en Python (cuidado con eval en producción)
    entorno_permitido = {"math": math}
    try:
        respuesta = eval(texto_usuario, {"__builtins__": {}}, entorno_permitido)
    except Exception as e:
        respuesta = f"Error: {e}"

    # Agregamos la respuesta del "bot"
    st.session_state["messages"].append(("bot", str(respuesta)))
    # Limpiamos el campo de entrada
    st.session_state["chat_input"] = ""

# ----------- Layout principal -----------
st.markdown("<div class='chat-page-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='chat-title'>Calculadora Chat</h2>", unsafe_allow_html=True)

# Contenedor del chat
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Ventana de mensajes
st.markdown("<div class='chat-window'>", unsafe_allow_html=True)
for sender, text in st.session_state["messages"]:
    sender_class = "user" if sender == "user" else "bot"
    st.markdown(f"<div class='message {sender_class}'>{text}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # cierra .chat-window

# Área de entrada + botón
# Usamos st.empty() como “marco” donde inyectamos HTML, para colocar el text_input y button en la misma fila
input_area = st.empty()
with input_area.container():
    st.markdown("<div class='input-area'>", unsafe_allow_html=True)
    user_input = st.text_input(
        "Ingresa una operación",
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Ej: 2+2, math.sqrt(9), etc.",
    )
    st.button("Enviar", on_click=enviar_mensaje)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # cierra .chat-container
st.markdown("</div>", unsafe_allow_html=True)  # cierra .chat-page-container
