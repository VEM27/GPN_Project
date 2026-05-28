import os
import json
from django.conf import settings
import re

def get_characteristics_slides(name):
    json_filename = os.path.join(settings.MEDIA_ROOT, 'pptx_outputs', f"output_{name}", f"output_{name}.json")
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = []
    for item in data:
        if 'ТРЕБОВАНИЯ' in str(item.get("title")).upper() and 'ХАРАКТЕРИСТИК' in str(item.get("title")).upper() and 'АРХИТЕКТУР' in str(item.get("title")).upper():
            result.append(item)

    return result


def extract_servers(slides):
    result = []

    for slide in slides:
        for table in slide.get("tables", []):
            for row in table:
                for cell in row:
                    if "СУЩЕСТВУЮЩИЙ" in cell.upper():
                        result.append(cell)

    return result  # если не найдено


def clean_servers(lines):
    result = []
    pattern = re.compile(r'^[A-Za-z0-9_.-]+$')         # полностью допустимая строка
    strip_pattern = re.compile(r'[^A-Za-z0-9_.-]+')     # нежелательные символы по краям

    for line in lines:
        parts = re.split(r'[\n\s]+', line)  # делим по пробелам и \n
        for part in parts:
            if pattern.match(part):  # допустимая строка целиком
                result.append(part)
            else:
                # убираем недопустимые символы только по краям
                cleaned = re.sub(r'^[^A-Za-z0-9_.-]+|[^A-Za-z0-9_.-]+$', '', part)
                if pattern.match(cleaned):
                    result.append(cleaned)
                # иначе — пропускаем

    return result


def remove_duplicates(seq):
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def get_numbers(table):
    numbers = {
        'N_os': -1,
        'N_cpu': -1,
        'N_ram': -1,
        'N_disk': -1,
        'N_place': -1,
        'N_sector': -1,
        'N_xaas': -1,
        'N_exist': -1,
        'N_target': -1,
        'N_size': -1,
        'N_type': -1,
        'N_system_size': -1,
        'N_data_size': -1
    }

    for i in range(2):
        row = table[i]
        for k in range(len(row)):
            tmp_arr = [numbers['N_os'], numbers['N_cpu'],
                       numbers['N_ram'], numbers['N_disk'],
                       numbers['N_place'], numbers['N_sector'], numbers['N_xaas'],
                       numbers['N_exist'], numbers['N_target'],
                       numbers['N_size'], numbers['N_type'],
                       numbers['N_system_size'], numbers['N_data_size']]
            if k in tmp_arr:
                continue
            cell = row[k].upper()
            if 'ОС' in cell and 'ПО' in cell and numbers['N_os'] == -1:
                numbers['N_os'] = k
            elif 'CPU' in cell and numbers['N_cpu'] == -1:
                numbers['N_cpu'] = k
            elif 'RAM' in cell and numbers['N_ram'] == -1:
                numbers['N_ram'] = k
            elif 'ДИСК' in cell and numbers['N_disk'] == -1:
                numbers['N_disk'] = k
            elif 'ПЛОЩАДКА' in cell and numbers['N_place'] == -1:
                numbers['N_place'] = k
            elif 'РАЗМЕЩЕНИЕ' in cell and numbers['N_sector'] == -1:
                numbers['N_sector'] = k
            elif 'ПЛАТФОРМА' in cell and numbers['N_xaas'] == -1:
                numbers['N_xaas'] = k
            elif ('НОВЫЙ' in cell or 'СУЩЕСТВУЮЩИЙ' in cell) and numbers['N_exist'] == -1:
                numbers['N_exist'] = k
            elif 'CORE' in cell and numbers['N_cpu'] == -1:
                numbers['N_cpu'] = k
            elif 'НАЗНАЧЕНИЕ' in cell and numbers['N_target'] == -1:
                numbers['N_target'] = k
            elif ('ОБЪЕМ' in cell or 'ОБЬЕМ' in cell or 'ОБЪЁМ' in cell) and numbers['N_size'] == -1:
                numbers['N_size'] = k
            elif 'ТИП' in cell and numbers['N_type'] == -1:
                numbers['N_type'] = k
            elif 'СИСТЕМНЫЙ ОБЪЕМ' in cell and numbers['N_system_size'] == -1:
                numbers['N_system_size'] = k
            elif 'ДАННЫЕ ОБЪЕМ' in cell and numbers['N_data_size'] == -1:
                numbers['N_data_size'] = k

    return numbers


def get_name_from_cell(cell):
    result = []
    pattern = re.compile(r'^[A-Za-z0-9_.-]+$')         # полностью допустимая строка

    parts = re.split(r'[\n\s]+', cell)  # делим по пробелам и \n
    for part in parts:
        if pattern.match(part):  # допустимая строка целиком
            result.append(part)
        else:
            # убираем недопустимые символы только по краям
            cleaned = re.sub(r'^[^A-Za-z0-9_.-]+|[^A-Za-z0-9_.-]+$', '', part)
            if pattern.match(cleaned):
                result.append(cleaned)
            # иначе — пропускаем

    return result


def summ_size(a, b):
    if a == '' or a is None:
        if b == '' or b is None:
            return ''
        a = 0

    if b == '' or b is None:
        b = 0

    try:
        fa = float(a)
        fb = float(b)
        result = fa + fb
        return int(result) if result.is_integer() else result
    except (ValueError, TypeError):
        if a == 0:
            return str(b)
        if b == 0:
            return str(a)
        return f"{a}, {b}"


def clean_string(s):
    if s is None:
        return ""

    # Удалить управляющие символы с начала и конца
    s = str(s).strip('\x0b\n\r')

    # Заменить управляющие символы внутри строки пробелами
    s = s.replace('\x0b', ' ').replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')

    # Удалить лишние пробелы (много пробелов → один пробел)
    s = ' '.join(s.split())

    return s


def slide_parser(slide):
    data = {}
    tables = slide['tables']
    for table in tables:
        numbers = get_numbers(table)
        flag = None
        for row in table:
            cell_name = row[numbers['N_exist']]
            cell_cpu = clean_string(row[numbers['N_cpu']])
            cell_ram = clean_string(row[numbers['N_ram']])
            names = get_name_from_cell(cell_name)
            cell_type = clean_string(row[numbers['N_type']])
            cell_size = clean_string(row[numbers['N_size']])
            cell_os = clean_string(row[numbers['N_os']])
            cell_xaas = clean_string(row[numbers['N_xaas']])

            if cell_name == '' and cell_cpu == '' and cell_ram == '' and flag is not None:
                for name in flag:
                    if str(cell_type).upper() == 'GOLD':
                        data[name]['file']['Gold'] = summ_size(data[name]['file']['Gold'], cell_size)
                    elif str(cell_type).upper() == 'SILVER':
                        data[name]['file']['Silver'] = summ_size(data[name]['file']['Silver'], cell_size)
                    elif str(cell_type).upper() == 'BRONZE':
                        data[name]['file']['Bronze'] = summ_size(data[name]['file']['Bronze'], cell_size)
                    elif str(cell_type).upper() == 'IRON':
                        data[name]['file']['Iron'] = summ_size(data[name]['file']['Iron'], cell_size)
                    elif str(cell_type).upper() == 'OTHER':
                        data[name]['file']['Other'] = summ_size(data[name]['file']['Other'], cell_size)
            else:
                cell_gold = ''
                cell_silver = ''
                cell_bronze = ''
                cell_iron = ''
                cell_other = ''

                if str(cell_type).upper() == 'GOLD':
                    cell_gold = cell_size
                elif str(cell_type).upper() == 'SILVER':
                    cell_silver = cell_size
                elif str(cell_type).upper() == 'BRONZE':
                    cell_bronze = cell_size
                elif str(cell_type).upper() == 'IRON':
                    cell_iron = cell_size
                elif str(cell_type).upper() == 'OTHER':
                    cell_other = cell_size

                for name in names:
                    data[name] = {
                        'file': {
                            'CI_name': name,
                            'VM_OS': cell_os,
                            'VM_vCenter': cell_xaas,
                            'VM_Cores': cell_cpu,
                            'VM_RAM': cell_ram,
                            'Gold': cell_gold,
                            'Silver': cell_silver,
                            'Bronze': cell_bronze,
                            'Iron': cell_iron,
                            'Other': cell_other
                        }
                    }
                    flag = names

    return data


def get_characteristics_data(base_name):
    slides = get_characteristics_slides(base_name)

    parsing_res = {}
    for slide in slides:
        header = str(slide['slide']) + ' - ' + str(slide['title'])
        slide_data = slide_parser(slide)
        parsing_res[header] = slide_data

    return parsing_res





