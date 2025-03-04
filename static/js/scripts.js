document.addEventListener('DOMContentLoaded', function() {
    console.log("scripts.js: DOMContentLoaded event ha ocurrido. JS está cargado.");
  
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatWindow = document.getElementById('chatWindow');
  
    console.log("scripts.js: Elementos HTML capturados:",
      { chatInput, sendBtn, chatWindow }
    );
  
    // Función para agregar un mensaje
    function appendMessage(sender, text) {
      console.log("appendMessage: Añadiendo mensaje de sender:", sender, "con text:", text);
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('message', sender);
      messageDiv.textContent = text;
      chatWindow.appendChild(messageDiv);
      // Auto-scroll hacia el final
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  
    // Procesa el mensaje ingresado
    function processMessage() {
      console.log("processMessage: Iniciando procesamiento de mensaje");
      const text = chatInput.value.trim();
      console.log("processMessage: Texto ingresado:", text);
  
      if (text === '') {
        console.log("processMessage: El usuario no escribió nada. Retorno.");
        return;
      }
      
      // Agregar mensaje del usuario
      appendMessage('user', text);
      chatInput.value = '';
  
      let result;
      try {
        console.log("processMessage: Evaluando expresión con math.js...");
        result = math.evaluate(text);
        console.log("processMessage: Resultado de math.evaluate:", result);
      } catch (e) {
        console.log("processMessage: Se produjo un error al evaluar:", e.message);
        result = 'Error: Expresión inválida';
      }
      // Agregar respuesta del "bot"
      appendMessage('bot', String(result));
    }
  
    // Asignar eventos
    console.log("scripts.js: Asignando evento click al botón Enviar...");
    sendBtn.addEventListener('click', function() {
      console.log("sendBtn: Botón clicado");
      processMessage();
    });
  
    chatInput.addEventListener('keypress', function(e) {
      console.log("chatInput: keypress detectado:", e.key);
      if (e.key === 'Enter') {
        console.log("chatInput: Enter presionado, llamando processMessage()");
        processMessage();
      }
    });
  });
  