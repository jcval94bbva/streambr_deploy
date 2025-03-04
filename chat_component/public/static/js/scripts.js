(function() {
  const Streamlit = window.Streamlit;

  // Función para manejar el render (si quisieras recibir props desde Python)
  function onRender(event) {
    // Ajustamos altura para que no haya scrollbars raras
    Streamlit.setFrameHeight();
  }

  // Escuchar el evento RENDER_EVENT
  Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

  // Marcar el componente como listo
  Streamlit.setComponentReady();
  // Ajustar la altura inicial
  Streamlit.setFrameHeight();

  // Capturar elementos
  const input = document.getElementById("myInput");
  const sendBtn = document.getElementById("sendBtn");

  // Al hacer clic en "Enviar", devolvemos el texto a Python
  sendBtn.addEventListener("click", () => {
    const text = input.value.trim();
    if (text) {
      // Devuelve el valor al backend de Python
      Streamlit.setComponentValue(text);
      input.value = "";  // Limpia el campo
    }
  });
})();
