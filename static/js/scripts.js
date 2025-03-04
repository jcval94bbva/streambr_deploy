document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatWindow = document.getElementById('chatWindow');
  
    // Función para agregar un mensaje al chat
    function appendMessage(sender, text) {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('message', sender);
      messageDiv.textContent = text;
      chatWindow.appendChild(messageDiv);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  
    // Función para procesar el mensaje enviado
    function processMessage() {
      const text = chatInput.value.trim();
      if (text === '') return;
      // Agrega el mensaje del usuario
      appendMessage('user', text);
      chatInput.value = '';
  
      let result;
      try {
        // Evaluar la expresión usando math.js
        result = math.evaluate(text);
      } catch (e) {
        result = 'Error: Expresión inválida';
      }
      // Agrega la respuesta del "bot"
      appendMessage('bot', result);
    }
  
    sendBtn.addEventListener('click', processMessage);
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        processMessage();
      }
    });
  });
  