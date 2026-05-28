document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('#architecture_app button');

  button.addEventListener('click', async () => {
    const base_name = sessionStorage.getItem('base_name');

    try {
      const response = await fetch(`/api/architecture_app/?base_name=${base_name}`);
      if (!response.ok) {
        throw new Error(`Ошибка сети: ${response.status}`);
      }

      const data = await response.json();

      // Теперь data — словарь, передаем в renderTable
      renderTableArchitectureApp(data, "architecture_app-container");
      highlightTableArchitectureApp("architecture_app-container")

    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      alert('Ошибка при получении данных');
    }
  });
});


function renderTableArchitectureApp(data, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  for (const header in data) {
    const h3 = document.createElement('h3');
    h3.textContent = header;
    container.appendChild(h3);

      console.log(header);
      const rows = data[header];

    // Заголовки таблицы
    const headers = ['ОС/ПО', 'Лицензии', 'l_s', 'Исп. технологии', 't_s', 'Санкции (поиск)', 's_s', 'Санкции'];

    // Создаём таблицу
    const table = document.createElement('table');

    // Создаём <thead>
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headers.forEach(headerText => {
      const th = document.createElement('th');
      th.textContent = headerText;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Создаём <tbody>
    const tbody = document.createElement('tbody');
    rows.forEach(row => {
      const tr = document.createElement('tr');
      row.forEach(cell => {
        const td = document.createElement('td');
        td.textContent = cell;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    // Добавляем таблицу в контейнер
    container.appendChild(table);
  }

 }


function highlightTableArchitectureApp(containerId) {
  const container = document.getElementById(containerId);
  const tables = container.getElementsByTagName('table');

  for (const table of tables) {
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = tbody.getElementsByTagName('tr');

    for (const tr of rows) {
      const cells = tr.getElementsByTagName('td');
      if (cells.length >= 5) {

        const l_s_text = cells[2].textContent.replace(',', '.'); // на случай локали с запятой
        const l_s_value = parseFloat(l_s_text);
        if (!isNaN(l_s_value) && l_s_value < 0.7 && l_s_value != 0) {
          cells[1].style.backgroundColor = 'yellow'; // 4-я ячейка (индекс 3)
          cells[2].style.backgroundColor = 'yellow'; // 5-я ячейка (индекс 4)
        } else if (!isNaN(l_s_value) && l_s_value == 0) {
          cells[1].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
          cells[2].style.backgroundColor = 'red'; // 5-я ячейка (индекс 4)
        }


        const t_s_text = cells[4].textContent.replace(',', '.'); // на случай локали с запятой
        const t_s_value = parseFloat(t_s_text);
        if (!isNaN(t_s_value) && t_s_value < 0.7 && t_s_value != 0) {
          cells[3].style.backgroundColor = 'yellow'; // 4-я ячейка (индекс 3)
          cells[4].style.backgroundColor = 'yellow'; // 5-я ячейка (индекс 4)
        } else if (!isNaN(t_s_value) && t_s_value === 0) {
          cells[3].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
          cells[4].style.backgroundColor = 'red'; // 5-я ячейка (индекс 4)
        }

        const license_value = cells[1].textContent;
        if (license_value === '---') {
          cells[1].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
        }

        const arc_app_value = cells[3].textContent;
        if (arc_app_value === '---') {
          cells[3].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
        }

        const sanctions_value = cells[7].textContent;
        if (sanctions_value === 'СПО') {
          cells[7].style.backgroundColor = 'orange';
        } else if (sanctions_value === 'Да') {
            cells[7].style.backgroundColor = 'red';
        } else if (sanctions_value === 'Нет') {
            cells[7].style.backgroundColor = 'green';
        }

        const s_s_text = cells[6].textContent.replace(',', '.'); // на случай локали с запятой
        const s_s_value = parseFloat(s_s_text);
        if (!isNaN(s_s_value) && s_s_value < 0.7 && s_s_value != 0) {
          cells[6].style.backgroundColor = 'yellow'; // 4-я ячейка (индекс 3)
          cells[5].style.backgroundColor = 'yellow'; // 5-я ячейка (индекс 4)
        } else if (!isNaN(s_s_value) && s_s_value == 0) {
          cells[6].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
          cells[5].style.backgroundColor = 'red'; // 5-я ячейка (индекс 4)
        }

      }
    }
  }
}

