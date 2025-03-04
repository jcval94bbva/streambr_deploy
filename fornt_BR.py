import streamlit as st
import math

# 1. Configurar la página
st.set_page_config(page_title="Calculadora Chat", layout="centered")

# 2. CSS inline para dar estilo al "chat"
#    Aquí definimos .chat-container, .message, .user y .bot
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
    background-color: #d1e7dd; /* verde claro */
    margin-left: auto;
    margin-right: 0;
    text-align: right;
    border-bottom-right-radius: 0;
}

.bot {
    background-color: #f8d7da; /* rojo claro */
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

# 3. Inicializar un contenedor para la "app de chat"
st.markdown("""
<div class="chat-container">
    <div class="chat-window" id="chat-window">
""", unsafe_allow_html=True)

# 4. Manejar el estado de los mensajes
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Lista de tuplas (sender, texto)

# 5. Mostrar los mensajes que haya en la sesión
for sender, text in st.session_state["messages"]:
    sender_class = "user" if sender == "user" else "bot"
    st.markdown(f'<div class="message {sender_class}">{text}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Cerrar chat-window

# 6. Área de input
#    Para capturar el texto ingresado, usaremos un st.text_input
#    y un st.button dentro de la misma "línea" visual.
user_input = st.text_input("", key="chat_input", label_visibility="collapsed")
send_clicked = st.button("Enviar")

# 7. Cerrar el chat-container
st.markdown("</div>", unsafe_allow_html=True)

# 8. Lógica para manejar la entrada del usuario
if send_clicked and user_input.strip():
    # 8.1 Agregar el mensaje del usuario al historial
    message_text = user_input.strip()
    st.session_state["messages"].append(("user", message_text))

    # 8.2 Evaluar la operación en Python
    #     Restringir eval a un entorno muy limitado
    allowed_names = {
        "math": math,
        # Podrías exponer otras funciones seguras si quieres
        # Ej: "abs": abs, "pow": pow, etc.
    }
    try:
        result = eval(message_text, {"__builtins__": None}, allowed_names)
    except Exception as e:
        result = f"Error: {e}"

    # 8.3 Agregar la respuesta (resultado) al historial
    st.session_state["messages"].append(("bot", str(result)))

    # 8.4 Limpiar el input
    st.session_state["chat_input"] = ""

    # 8.5 Forzar recarga para que se muestre de inmediato el nuevo mensaje
    st.experimental_rerun()
