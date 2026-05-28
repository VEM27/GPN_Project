document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('#licenses button');

  button.addEventListener('click', async () => {
    const base_name = sessionStorage.getItem('base_name');

    try {
      const response = await fetch(`/api/licenses/?base_name=${base_name}`);

      if (!response.ok) {
        throw new Error(`Ошибка сети: ${response.status}`);
      }

      const data = await response.json();

      // Теперь data — словарь, передаем в renderTable
      renderTableLicenses(data, "licenses-container");
      highlightTableLicenses("licenses-container")

    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      alert('Ошибка при получении данных');
    }
  });
});


function renderTableLicenses(data, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  for (const header in data) {
    const h3 = document.createElement('h3');
    h3.textContent = header;
    container.appendChild(h3);

      console.log(header);
      const entries = data[header];

      // Заголовок таблицы берётся из первой записи
      const headerRow = entries['Продукт'];
      const headers = Object.values(headerRow);

      // Получаем остальные строки
      const rows = Object.keys(entries)
        .filter(key => key !== 'Продукт')
        .map(key => {
          const entry = entries[key];
          return headers.map(header => {
            // Находим ключ по значению заголовка
            const fieldKey = Object.keys(headerRow).find(k => headerRow[k] === header);
            return entry[fieldKey] || '';
          });
        });

      // Создаём таблицу
      const table = document.createElement('table');
      table.classList.add('licenses-table');

      // Заголовки
      const thead = document.createElement('thead');
      const trHead = document.createElement('tr');
      headers.forEach(h => {
        const th = document.createElement('th');
        th.textContent = h;
        trHead.appendChild(th);
      });
      thead.appendChild(trHead);
      table.appendChild(thead);

      // Данные
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

      container.appendChild(table);

    }
  }


function highlightTableLicenses(containerId) {
  const container = document.getElementById(containerId);
  const tables = container.getElementsByTagName('table');

  for (const table of tables) {
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = tbody.getElementsByTagName('tr');

    for (const tr of rows) {
      const cells = tr.getElementsByTagName('td');
      if (cells.length >= 7) {

        const l_s_text = cells[4].textContent.replace(',', '.'); // на случай локали с запятой
        const l_s_value = parseFloat(l_s_text);
        if (!isNaN(l_s_value) && l_s_value < 0.7 && l_s_value != 0) {
          cells[3].style.backgroundColor = 'yellow'; // 4-я ячейка (индекс 3)
          cells[4].style.backgroundColor = 'yellow'; // 5-я ячейка (индекс 4)
        } else if (!isNaN(l_s_value) && l_s_value == 0) {
          cells[3].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
          cells[4].style.backgroundColor = 'red'; // 5-я ячейка (индекс 4)
        }


        const a_s_text = cells[6].textContent.replace(',', '.'); // на случай локали с запятой
        const a_s_value = parseFloat(a_s_text);
        if (!isNaN(a_s_value) && a_s_value < 0.7 && a_s_text != 0) {
          cells[5].style.backgroundColor = 'yellow'; // 4-я ячейка (индекс 3)
          cells[6].style.backgroundColor = 'yellow'; // 5-я ячейка (индекс 4)
        } else if (!isNaN(a_s_text) && a_s_text == 0) {
          cells[5].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
          cells[6].style.backgroundColor = 'red'; // 5-я ячейка (индекс 4)
        }


        const license_value = cells[3].textContent;
        if (license_value === '---') {
          cells[3].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
        }

        const arc_app_value = cells[5].textContent;
        if (arc_app_value === '---') {
          cells[5].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
        }

        const sanctions_value = cells[9].textContent;
        if (sanctions_value === 'СПО') {
          cells[9].style.backgroundColor = 'orange';
        } else if (sanctions_value === 'Да') {
            cells[9].style.backgroundColor = 'red';
        } else if (sanctions_value === 'Нет') {
            cells[9].style.backgroundColor = 'green';
        }

        const s_s_text = cells[8].textContent.replace(',', '.'); // на случай локали с запятой
        const s_s_value = parseFloat(s_s_text);
        if (!isNaN(s_s_value) && s_s_value < 0.7 && s_s_value != 0) {
          cells[7].style.backgroundColor = 'yellow'; // 4-я ячейка (индекс 3)
          cells[8].style.backgroundColor = 'yellow'; // 5-я ячейка (индекс 4)
        } else if (!isNaN(s_s_value) && s_s_value == 0) {
          cells[7].style.backgroundColor = 'red'; // 4-я ячейка (индекс 3)
          cells[8].style.backgroundColor = 'red'; // 5-я ячейка (индекс 4)
        }


      }
    }
  }
}
