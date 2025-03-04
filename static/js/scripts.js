document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatWindow = document.getElementById('chatWindow');
  
    // Función para agregar un mensaje
    function appendMessage(sender, text) {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('message', sender);
      messageDiv.textContent = text;
      chatWindow.appendChild(messageDiv);
      // Auto-scroll hacia el final
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  
    // Procesa el mensaje ingresado
    function processMessage() {
      const text = chatInput.value.trim();
      if (text === '') return;
      
      // Agregar mensaje del usuario
      appendMessage('user', text);
      chatInput.value = '';
  
      let result;
      try {
        // Evaluar la expresión con math.js
        result = math.evaluate(text);
      } catch (e) {
        result = 'Error: Expresión inválida';
      }
      // Agregar respuesta del "bot"
      appendMessage('bot', result);
    }
  
    // Asignar eventos: clic en botón y tecla Enter en el input
    sendBtn.addEventListener('click', processMessage);
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        processMessage();
      }
    });
  });
  