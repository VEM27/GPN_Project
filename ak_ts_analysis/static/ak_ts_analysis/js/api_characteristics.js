//document.addEventListener('DOMContentLoaded', () => {
//  const button = document.querySelector('#characteristics button');
//
//  button.addEventListener('click', async () => {
//
//    const base_name = sessionStorage.getItem('base_name');
//
//    try {
//      const [characteristicsRes] = await Promise.all([
//        fetch(`/api/characteristics/?base_name=${base_name}`)
//      ]);
//
//      const characteristicsData = characteristicsRes.ok ? await characteristicsRes.json() : {};
//
//      console.log(characteristicsData[0]);
//      console.log(characteristicsData[1]);
//      renderTable(characteristicsData[0], "characteristics-container-v");
//      renderTable(characteristicsData[1], "characteristics-container-p");
//
//    } catch (error) {
//      console.error('Ошибка загрузки данных:', error);
//      alert('Ошибка при получении данных');
//    }
//  });
//});

document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('#characteristics button');

  button.addEventListener('click', async () => {
    const base_name = sessionStorage.getItem('base_name');

    try {
      const response = await fetch(`/api/characteristics/?base_name=${base_name}`);

      if (!response.ok) {
        throw new Error(`Ошибка сети: ${response.status}`);
      }

      const data = await response.json();

      // Теперь data — словарь, передаем в renderTable
      renderTableCharacteristics(data, "characteristics-container");

    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      alert('Ошибка при получении данных');
    }
  });
});


function compareNames(cmdb, file) {
  return cmdb === file.toUpperCase() ? 1 : 0;
}

// используется только вместе с compareOS. Преобразует некоторое описание ос в формальный вид.
function getOS(in_os) {
    let res = [];

    if (in_os.includes('WINDOWS')) {
        res.push('WINDOWS');
        if (in_os.includes('SERVER')) {
            res.push('WINDOWS SERVER');
            if (in_os.includes('2022')) {
                res.push('WINDOWS SERVER 2022');
            } else if (in_os.includes('2019')) {
                res.push('WINDOWS SERVER 2019');
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS SERVER 2022', 'LATER');
                }
            } else if (in_os.includes('2016')) {
                res.push('WINDOWS SERVER 2016');
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS SERVER 2022', 'WINDOWS SERVER 2019', 'LATER');
                }
            } else if (in_os.includes('2012')) {
                res.push('WINDOWS SERVER 2012');
                if (in_os.includes('R2')) {
                    res.push('WINDOWS SERVER 2012 R2');
                }
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS SERVER 2022', 'WINDOWS SERVER 2019', 'WINDOWS SERVER 2016', 'LATER');
                }
            } else if (in_os.includes('2008')) {
                res.push('WINDOWS SERVER 2008');
                if (in_os.includes('R2')) {
                    res.push('WINDOWS SERVER 2008 R2');
                }
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS SERVER 2022', 'WINDOWS SERVER 2019', 'WINDOWS SERVER 2016', 'WINDOWS SERVER 2012', 'LATER');
                }
            } else if (in_os.includes('2003')) {
                res.push('WINDOWS SERVER 2003');
                if (in_os.includes('R2')) {
                    res.push('WINDOWS SERVER 2003 R2');
                }
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS SERVER 2022', 'WINDOWS SERVER 2019', 'WINDOWS SERVER 2016', 'WINDOWS SERVER 2008', 'WINDOWS SERVER 2012', 'LATER');
                }
            } else if (in_os.includes('2000')) {
                res.push('WINDOWS SERVER 2000');
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS SERVER 2022', 'WINDOWS SERVER 2019', 'WINDOWS SERVER 2016', 'WINDOWS SERVER 2008', 'WINDOWS SERVER 2012', 'WINDOWS SERVER 2003', 'LATER');
                }
            } else if (in_os.includes('NT')) {
                res.push('WINDOWS SERVER NT');
                if (in_os.includes('3.1')) {
                    res.push('WINDOWS SERVER NT 3.1');
                } else if (in_os.includes('3.5')) {
                    res.push('WINDOWS SERVER NT 3.5');
                } else if (in_os.includes('3.51')) {
                    res.push('WINDOWS SERVER NT 3.51');
                } else if (in_os.includes('4.0')) {
                    res.push('WINDOWS SERVER NT 4.0');
                }
            }
        } else {
            if (in_os.includes('11')) {
                res.push('WINDOWS 11');
            } else if (in_os.includes('10')) {
                res.push('WINDOWS 10');
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS 11', 'LATER');
                }
            } else if (in_os.includes('8')) {
                res.push('WINDOWS 8');
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS 11', 'WINDOWS 10', 'LATER');
                }
            } else if (in_os.includes('7')) {
                res.push('WINDOWS 7');
                if (in_os.includes('LATER')) {
                    res.push('WINDOWS 11', 'WINDOWS 10', 'WINDOWS 8', 'LATER');
                }
            } else if (in_os.includes('2000')) {
                res.push('WINDOWS 2000');
            } else if (in_os.includes('98')) {
                res.push('WINDOWS 98');
            } else if (in_os.includes('95')) {
                res.push('WINDOWS 95');
            } else if (in_os.includes('NT')) {
                res.push('WINDOWS NT');
            } else if (in_os.includes('XP')) {
                res.push('WINDOWS XP');
            } else if (in_os.includes('VISTA')) {
                res.push('WINDOWS VISTA');
            }
        }
    } else if (in_os.includes('ASTRA')) {
        res.push('LINUX', 'ASTRA LINUX');
    } else if (in_os.includes('CENT')) {
        res.push('LINUX', 'CENTOS');
    } else if (in_os.includes('DEBIAN')) {
        res.push('LINUX', 'DEBIAN');
    } else if (in_os.includes('UBUNTU')) {
        res.push('LINUX', 'UBUNTU');
    } else if (in_os.includes('ORACLE')) {
        res.push('LINUX', 'ORACLE');
    } else if (in_os.includes('REDOS') || in_os.includes('RED OS') || in_os.includes('РЕДОС') || in_os.includes('РЕД ОС')) {
        res.push('LINUX', 'РЕД ОС');
    } else if (in_os.includes('АЛЬТ') || in_os.includes('ALT')) {
        res.push('LINUX', 'ALT LINUX');
    } else if (in_os.includes('MS SQL')) {
        res.push('MS SQL SERVER');
    } else if (in_os.includes('REDIS')) {
        res.push('СУБД REDIS');
    } else if (in_os.includes('RHEL') || in_os.includes('RED HAT')) {
        res.push('LINUX', 'RHEL');
    } else if (in_os.includes('FEDORA') || in_os.includes('FCOS')) {
        res.push('LINUX', 'FEDORA');
    } else if (in_os.includes('RHCOS') || in_os.includes('CORE')) {
        res.push('LINUX', 'COREOS');
    } else if (in_os.includes('MIRACLE')) {
        res.push('LINUX', 'FEDORA');
    } else if (in_os.includes('SUSE') || in_os.includes('SLES')) {
        res.push('LINUX', 'SUSE');
    } else if (in_os.includes('FREEBSD')) {
        res.push('FREEBSD');
    } else if (in_os.includes('VMWARE')) {
        res.push('VMWARE');
        if (in_os.includes('VCSA')) {
            res.push('LINUX', 'VMWARE VCSA');
        }
        if (in_os.includes('PHOTON')) {
            res.push('VMWARE PHOTON');
        }
        if (in_os.includes('ESXI')) {
            res.push('VMWARE ESXI');
        }
        if (in_os.includes('VSPHERE')) {
            res.push('VMWARE VSPHERE');
        }
    } else if (in_os.includes('ESXI')) {
        res.push('VMWARE ESXI');
    } else if (in_os.includes('ZVIRT')) {
        res.push('ZVIRT');
    } else if (in_os.includes('RAIDIX')) {
        res.push('RAIDIX');
    } else if (in_os.includes('VIRTUAL APPLIANCE')) {
        res.push('LINUX');
    } else if (in_os.includes('UBI')) {
        res.push('LINUX');
    } else if (in_os.includes('LINUX')) {
        res.push('LINUX');
    } else {
        res.push(in_os);
    }
    console.log(res);
    return res;
}

function compareOS(cmdb, file) {
    os1 = cmdb.toUpperCase();
    os2 = file.toUpperCase();

    if (os1 === '' || os2 === '') {
        return 0;
    }

    let setOS1 = Array.from(new Set(getOS(os1)));
    let setOS2 = Array.from(new Set(getOS(os2)));

    if (JSON.stringify(setOS1) === JSON.stringify(setOS2)) {
        return 1;
    } else if (setOS1.every(val => setOS2.includes(val)) && setOS2.includes('LATER')) {
        return 1;
    } else if (setOS2.every(val => setOS1.includes(val)) && setOS1.includes('LATER')) {
        return 1;
    } else if (setOS1.every(val => setOS2.includes(val))) {
        return 2;
    } else if (setOS2.every(val => setOS1.includes(val))) {
        return 2;
    } else {
        return 0;
    }
}

function compareXAAS(cmdb, file) {
    if (file.toUpperCase().includes('IAAS') && cmdb.includes('IAAS')){
        return 1;
    } else if (file.toUpperCase().includes('IAAS') || cmdb.includes('IAAS')) {
        return 0;
    } else {
        return 2;
    }
}

function extractFromBracketsOne(text) {
    if (typeof text !== 'string') {
        return null;
    }
    const match = text.match(/\(([^)]+)\)/);
    if (match) {
        return match[1]; // Содержимое внутри первых скобок
    } else {
        return null; // Скобок нет
    }
}

function compareCoresRam(cmdb, file) {
    extract = extractFromBracketsOne(file);
    if (extract === null){
        return compareLikeNums(cmdb, file);
    } else {
        return compareLikeNums(cmdb, extract);
    }
}

function compareLikeNums(cmdb, file){
    try {
        const num_cmdb = Number(cmdb);
        const num_file = Number(file);

        if (isNaN(num_cmdb) || isNaN(num_file)) {
            cmdb == file ? 1 : 0;
        }

        if (num_cmdb > num_file) {
          return 0;
        } else if (num_cmdb < num_file) {
          return 2;
        } else {
          return 1;
        }

    } catch (error) {
        return 0;
    }
}

function compareHDD(cmdb, file) {
    if (cmdb == '0' && file == '' || cmdb == '' && file == '0'){
        return 1;
    }
    extract = extractFromBracketsOne(file);
    if (extract === null){
        return compareLikeNums(cmdb, file);
    } else {
        return compareLikeNums(cmdb, extract);
    }
    return 0;
}

function compareDefault(cmdb, file) {
  return cmdb === file ? 1 : 0;
}

const compareFunctions = {
  'CI_name': compareNames,
  'VM_OS': compareOS,
  'VM_vCenter': compareXAAS,
  'VM_Cores': compareCoresRam,
  'VM_RAM': compareCoresRam,
  'Gold': compareHDD,
  'Silver': compareHDD,
  'Bronze': compareHDD,
  'Iron': compareHDD,
  'Other': compareHDD,
  'default': compareDefault
};

function renderTableCharacteristics(data, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  for (const header in data) {
    const servers = data[header];

    const h3 = document.createElement('h3');
    h3.textContent = header;
    container.appendChild(h3);

    const table = document.createElement('table');
    table.classList.add('custom-table');
    container.appendChild(table);

    let keys = null;
    for (const srv in servers) {
      if (servers[srv].file) {
        keys = Object.keys(servers[srv].file);
        break;
      }
      if (servers[srv].cmdb_v) {
        keys = Object.keys(servers[srv].cmdb_v);
      }
    }
    if (!keys) keys = [];

    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');

    const thType = document.createElement('th');
    thType.textContent = 'Тип';
    headRow.appendChild(thType);

    keys.forEach(key => {
      const th = document.createElement('th');
      th.textContent = key;
      headRow.appendChild(th);
    });

    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    table.appendChild(tbody);

    for (const srv in servers) {
      const trSrv = document.createElement('tr');
      trSrv.classList.add('server-name-row');

      const tdSrv = document.createElement('td');
      tdSrv.colSpan = keys.length + 1;
      tdSrv.textContent = srv;
      trSrv.appendChild(tdSrv);
      tbody.appendChild(trSrv);

      const file = servers[srv].file || {};
      const cmdb = servers[srv].cmdb_v || {};

      ['file', 'cmdb_v'].forEach(type => {
        const obj = servers[srv][type];
        if (!obj) return;

        const tr = document.createElement('tr');
        const tdType = document.createElement('td');
        tdType.textContent = type === 'file' ? 'file' : 'cmdb';
        tr.appendChild(tdType);

        keys.forEach(key => {
          const td = document.createElement('td');
          const value = obj[key] !== undefined ? obj[key] : '';
          td.textContent = value;

          if (type === 'file' && cmdb[key] !== undefined) {
            const compareFn = compareFunctions[key] || compareFunctions['default'];
            const result = compareFn(cmdb[key], value);

            if (result === 1) td.classList.add('match-green');
            else if (result === 2) td.classList.add('match-yellow');
            else if (result === 0) td.classList.add('match-red');
          }

          tr.appendChild(td);
        });

        tbody.appendChild(tr);
      });
    }
  }
}



//function renderTable(data, containerId) {
//  const container = document.getElementById(containerId);
//  container.innerHTML = "";
//
//  if (!Array.isArray(data) || data.length === 0) {
//    container.textContent = "Нет данных";
//    return;
//  }
//
//  const table = document.createElement("table");
//  table.border = 1;
//
//  const thead = document.createElement("thead");
//  const headerRow = document.createElement("tr");
//
//  const headers = Object.keys(data[0]);
//  headers.forEach(key => {
//    const th = document.createElement("th");
//    th.textContent = key;
//    headerRow.appendChild(th);
//  });
//  thead.appendChild(headerRow);
//  table.appendChild(thead);
//
//  const tbody = document.createElement("tbody");
//  data.forEach(item => {
//    const row = document.createElement("tr");
//    headers.forEach(key => {
//      const td = document.createElement("td");
//      td.textContent = item[key];
//      row.appendChild(td);
//    });
//    tbody.appendChild(row);
//  });
//
//  table.appendChild(tbody);
//  container.appendChild(table);
//}
//
