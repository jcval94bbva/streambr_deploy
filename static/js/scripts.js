// Almacena la lista de géneros seleccionados y sus calificaciones
let selectedGenres = [];

// Manejo de tabs (secciones)
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    const targetId = this.getAttribute('data-target');

    // Ocultar todas las secciones
    document.querySelectorAll('[id^="seccion-"]').forEach(sec => {
      sec.classList.remove('seccion-activa');
      sec.classList.add('seccion-inactiva');
    });

    // Mostrar la sección seleccionada
    document.getElementById(targetId).classList.remove('seccion-inactiva');
    document.getElementById(targetId).classList.add('seccion-activa');
  });
});

// Elementos del DOM
const genreSelect = document.getElementById('genreSelect');
const errorMessage = document.getElementById('errorMessage');
const sliderContainer = document.getElementById('sliderContainer');
const recommendBtn = document.getElementById('recommendBtn');
const resultSection = document.getElementById('resultSection');

// Evento para controlar la selección de géneros
genreSelect.addEventListener('change', function () {
  // Obtener géneros seleccionados
  const options = Array.from(genreSelect.selectedOptions);
  selectedGenres = options.map(opt => opt.value);

  // Validar si son exactamente 3
  if (selectedGenres.length !== 3) {
    errorMessage.classList.remove('d-none');
    recommendBtn.disabled = true;
    sliderContainer.innerHTML = '';
  } else {
    errorMessage.classList.add('d-none');
    recommendBtn.disabled = false;
    renderSliders(selectedGenres);
  }
});

// Genera sliders dinámicamente para los géneros elegidos
function renderSliders(genres) {
  sliderContainer.innerHTML = '';
  genres.forEach(g => {
    const sliderItem = document.createElement('div');
    sliderItem.classList.add('slider-item');

    sliderItem.innerHTML = `
      <label for="slider_${g}"><strong>${g}:</strong></label>
      <input
        type="range"
        id="slider_${g}"
        name="${g}"
        min="1"
        max="10"
        value="8"
        oninput="document.getElementById('valor_${g}').textContent = this.value"
      />
      <span id="valor_${g}">8</span>
    `;

    sliderContainer.appendChild(sliderItem);
  });
}

// Evento para el botón "Obtener Recomendación"
recommendBtn.addEventListener('click', function () {
  // Recopilar calificaciones
  let ratings = {};
  selectedGenres.forEach(g => {
    const slider = document.getElementById(`slider_${g}`);
    ratings[g] = slider.value;
  });

  // Limpieza de la sección de resultados
  resultSection.innerHTML = '';

  // Mostrar calificaciones al usuario (interfaz)
  const calificacionesHTML = document.createElement('div');
  calificacionesHTML.innerHTML = `
    <h5>Calificaciones seleccionadas:</h5>
    <pre>${JSON.stringify(ratings, null, 2)}</pre>
  `;
  resultSection.appendChild(calificacionesHTML);

  // Aquí podrías hacer una llamada a tu backend en Python
  // por ejemplo, con fetch a un endpoint de Streamlit o similar.
  // Para DEMO, simulamos la respuesta:

  // Simulamos un "punto en el espacio de las canciones"
  const puntoEspacio = [Math.random().toFixed(2), Math.random().toFixed(2)];

  // Simulamos una respuesta JSON
  const simulatedResponse = {
    closest_tracks: ["Canción 1", "Canción 2", "Canción 3"],
    farthest_tracks: ["Canción X", "Canción Y", "Canción Z"]
  };

  // Mostramos la simulación de resultados
  const espacioHTML = document.createElement('div');
  espacioHTML.innerHTML = `
    <p><strong>Punto en el espacio de las canciones:</strong> [${puntoEspacio}]</p>
    <p><em>Notebook de referencia:</em> <a href="https://colab.research.google.com/drive/1rnYxUtNQ1GesDJ1n3fqJ2dyQBdsLb7XR#scrollTo=kRTze_zl76-I" target="_blank">Ver Notebook</a></p>
  `;
  resultSection.appendChild(espacioHTML);

  const recomendacionHTML = document.createElement('div');
  recomendacionHTML.innerHTML = `
    <p><strong>Te podrían gustar:</strong> ${simulatedResponse.closest_tracks.join(', ')}</p>
    <p><strong>Experimental:</strong> ${simulatedResponse.farthest_tracks.join(', ')}</p>
  `;
  resultSection.appendChild(recomendacionHTML);
});
