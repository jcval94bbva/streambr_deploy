(function() {
  const Streamlit = window.Streamlit;
  // Establecer la altura del frame
  Streamlit.setFrameHeight(600);
  console.log("Calc Chat Component: Frame height establecido.");

  // Obtener las propiedades iniciales pasadas desde Python
  const props = window.Streamlit?.componentProps || {};
  const chatHistory = props.chat_history || [];
  console.log("Calc Chat Component: Historial recibido desde Python:", chatHistory);

  // Función para renderizar el historial en el contenedor del chat
  function renderChatHistory() {
    const chatWindow = document.getElementById("chat-window");
    chatWindow.innerHTML = "";
    chatHistory.forEach(item => {
      const div = document.createElement("div");
      div.className = "message " + item.sender;
      div.textContent = item.message;
      chatWindow.appendChild(div);
    });
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  renderChatHistory();

  // Capturar elementos del input y botón
  const sendButton = document.getElementById("send-button");
  const chatInput = document.getElementById("chat-input");

  // Evento para el botón "Enviar"
  sendButton.addEventListener("click", () => {
    const message = chatInput.value.trim();
    console.log("Calc Chat Component: Botón enviar clicado. Mensaje:", message);
    if (message !== "") {
      // Enviar el mensaje a Python
      Streamlit.setComponentValue(message);
      chatInput.value = "";
    }
  });

  // Permitir enviar con Enter
  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendButton.click();
    }
  });
})();
