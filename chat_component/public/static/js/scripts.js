(function() {
  const Streamlit = window.Streamlit;

  // Renderizar los mensajes del historial
  function renderChat(props) {
    const chatWindow = document.getElementById("chat-window");
    if (!chatWindow) return;

    // Limpia el contenedor
    chatWindow.innerHTML = "";

    // Extrae la propiedad 'chat_history' pasada desde Python
    const chatHistory = props.chat_history || [];
    chatHistory.forEach(([sender, text]) => {
      const msgDiv = document.createElement("div");
      msgDiv.classList.add("message");
      msgDiv.classList.add(sender === "user" ? "user" : "bot");
      msgDiv.textContent = text;
      chatWindow.appendChild(msgDiv);
    });

    // Hacer scroll hasta el final
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // Se llama cada vez que Streamlit renderiza el componente
  function onRender(event) {
    const { props } = event.detail;
    renderChat(props);
    // Ajustar la altura del iframe
    Streamlit.setFrameHeight();
  }

  // Inicializar
  document.addEventListener("DOMContentLoaded", () => {
    // Suscribirse al evento "streamlit:render"
    document.addEventListener("streamlit:render", onRender);

    const sendBtn = document.getElementById("send-button");
    const inputField = document.getElementById("chat-input");

    // Cuando el usuario hace clic en "Enviar"
    sendBtn.addEventListener("click", () => {
      const text = inputField.value.trim();
      if (text) {
        // Enviamos el mensaje a Python
        Streamlit.setComponentValue(text);
        // Limpiamos el input
        inputField.value = "";
      }
    });

    // Permitir enviar con la tecla Enter
    inputField.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        sendBtn.click();
      }
    });
  });
})();
