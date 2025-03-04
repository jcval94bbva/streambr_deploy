(function() {
  const Streamlit = window.Streamlit;

  // Renderizar los mensajes en el #chat-window
  function renderMessages(messages) {
    const chatWindow = document.getElementById("chat-window");
    chatWindow.innerHTML = "";

    messages.forEach(msg => {
      const [sender, text] = msg; // msg[0] = 'user'|'bot', msg[1] = texto
      const div = document.createElement("div");
      div.classList.add("message", sender);
      div.textContent = text;
      chatWindow.appendChild(div);
    });

    // Hacer scroll al final
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // Maneja el evento RENDER_EVENT que envía Streamlit
  function onRender(event) {
    const { messages } = event.detail; // Python nos envía messages como prop
    renderMessages(messages);
    // Ajusta la altura del iframe
    Streamlit.setFrameHeight();
  }

  // Escuchamos cuando Streamlit nos pide renderizar
  Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

  // Marcar el componente como listo
  Streamlit.setComponentReady();
  Streamlit.setFrameHeight();

  // Capturar elementos
  const chatInput = document.getElementById("chat-input");
  const sendButton = document.getElementById("send-button");

  // Evento click en "Enviar"
  sendButton.addEventListener("click", () => {
    const text = chatInput.value.trim();
    if (text) {
      // Enviar el texto a Python
      Streamlit.setComponentValue(text);
      // Limpiar el input
      chatInput.value = "";
    }
  });

  // Enviar con Enter
  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendButton.click();
    }
  });
})();
