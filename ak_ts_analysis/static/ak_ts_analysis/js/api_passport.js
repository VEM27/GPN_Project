function createTablePassport(data, highlightColumn, containerId, columns,headers) {
  const container = document.getElementById(containerId);
  container.innerHTML = ""; // Очистить перед вставкой

  const table = document.createElement("table");
  table.border = 1;

  // Заголовок
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  headers.forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Тело таблицы
  const tbody = document.createElement("tbody");
  const rowsData = Array.isArray(data) ? data : [data];
rowsData.forEach((item, index) => {
  const row = document.createElement("tr");

  columns.forEach(col => {
    const td = document.createElement("td");
    td.textContent = item[col] ?? "";

    if (col === highlightColumn) {
      td.style.backgroundColor = "#ffff99";
    }

    if (col.includes("rto") || col.includes("rpo") || col.includes("br_criticality")) {
      td.style.color = "blue";
      td.style.fontWeight = "bold";
    }

    if (col === "br_criticality" && item["br_rpo"] && item["br_rto"]) {
      if ((Number(item["br_rto"]) > 48 || Number(item["br_rpo"]) > 24) && item[col] !== "Поддерживающая") {
        td.style.color = "red";
      } else if (((Number(item["br_rto"]) <= 48 && Number(item["br_rto"]) > 4) ||
                 (Number(item["br_rpo"]) <= 24 && Number(item["br_rpo"]) > 2)) &&
                 item[col] !== "Важная") {
        td.style.color = "red";
      } else if ((Number(item["br_rto"]) <= 4 || Number(item["br_rpo"]) <= 2) &&
                 item[col] !== "Критическая") {
        td.style.color = "red";
      }
    }

    row.appendChild(td);
  });

  // Если это последняя строка — красим её целиком
  if (index === rowsData.length - 1) {
      [...row.children].forEach(cell => {
        cell.style.backgroundColor = "#535353";
        cell.style.color = "white";
        cell.style.borderLeft = "1px solid black";
        cell.style.borderRight = "1px solid black";
      });
    }

  tbody.appendChild(row);
});

  table.appendChild(tbody);

  container.appendChild(table);
}


document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('#passport input');
  const button = document.querySelector('#passport button');

  button.addEventListener('click', async () => {
    let value = input.value.trim();
    if (!value) {
      value = '999999999999';
    }

    const selectedValue = document.getElementById("parameter").value;
    const base_name = sessionStorage.getItem('base_name');
    try {
      const [esisRes, ktRes] = await Promise.all([
        fetch(`/api/esis/?value=${encodeURIComponent(value)}&field=${selectedValue}&base_name=${base_name}`),
        fetch(`/api/kt670/?value=${encodeURIComponent(value)}&field=${selectedValue}&base_name=${base_name}`)
      ]);

      const esisData = esisRes.ok ? await esisRes.json() : {};
      const ktData = ktRes.ok ? await ktRes.json() : {};

      createTablePassport(esisData, selectedValue, "esis-container", ["br_code", "br_name", "br_rto", "br_rpo", "br_criticality","bs_code","bs_name","bs_rpo","bs_rto"], ["БР.КОД", "БР.ИМЯ", "БР.RTO", "БР.RPO", "Критичность","БС.КОД","БС.ИМЯ","БС.RPO","БС.RTO"]);
      createTablePassport(ktData, selectedValue, "kt-container", ["br_code", "br_name", "bu_code", "bu_name","br_rto","br_rpo","br_criticality"], ["БР.КОД", "БР.ИМЯ", "БУ.КОД", "БУ.ИМЯ","БР.RTO", "БР.RPO", "Критичность"]);
      document.querySelectorAll('.table-header').forEach(el => {
        el.style.display = 'block';
      });

    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      alert('Ошибка при получении данных');
    }
  });
});





