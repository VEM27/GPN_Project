document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('uploadForm');
  const pdfInput = document.getElementById('pdfInput');
  const pdfViewer = document.getElementById('pdfViewer');

  // Отображаем PDF сразу при выборе файла
  pdfInput.addEventListener('change', () => {
    const file = pdfInput.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      pdfViewer.src = url;
    }
  });

  // Отправляем только презентацию на сервер
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const presentationFile = form.elements['presentation'].files[0];

    formData.append('presentation', presentationFile);

    const response = await fetch('', {
      method: 'POST',
      body: formData,
    });

    if(response.ok) {
      const data = await response.json(); // <- читаем JSON-ответ
      sessionStorage.setItem('base_name', data.base_name);
      alert('Презентация успешно отправлена на сервер!');
    } else {
      alert('Ошибка при отправке презентации');
    }
  });
});


