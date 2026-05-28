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


def get_numbers(table):
    numbers = {
        'N_os': -1,
    }

    for i in range(2):
        row = table[i]
        for k in range(len(row)):
            cell = row[k].upper()
            if 'ОС' in cell and 'ПО' in cell and numbers['N_os'] == -1:
                numbers['N_os'] = k
    return numbers


def parce_string(s):
    if s is None:
        return []

    # Удалить управляющие символы с начала и конца
    s = str(s).strip('\x0b\n\r')

    # Заменить управляющие символы внутри строки пробелами
    s = s.replace(',\n', '\n').replace(',\x0b', '\n').replace(',\r\n', '\n').replace(',\r', '\n').replace('\x0b', '\n').replace('\r\n', '\n').replace('\r', '\n').replace(', ', '\n').replace(',', '\n')
    while '\n\n' in s:
        s = s.replace('\n\n', '\n')
    while '  ' in s:
        s = s.replace('  ', ' ')

    # Удалить лишние пробелы (много пробелов → один пробел)
    res = s.split('\n')

    return res


def slide_parser(slide):
    res_table = []
    tables = slide['tables']
    for table in tables:
        numbers = get_numbers(table)
        for row in table:
            if 'ОС' in row[numbers['N_os']] and 'ПО' in row[numbers['N_os']]:
                continue
            cell_os = parce_string(row[numbers['N_os']])
            if len(cell_os) != 0:
                for item in cell_os:
                    if item != '':
                        res_table.append([item])

    unique_res_table = [list(t) for t in set(tuple(row) for row in res_table)]
    return unique_res_table


def make_architecture_app_data(base_name):
    slides = get_characteristics_slides(base_name)

    parsing_res = {}
    for slide in slides:
        header = str(slide['slide']) + ' - ' + str(slide['title'])
        slide_data = slide_parser(slide)
        parsing_res[header] = slide_data

    return parsing_res


def get_app_from_architecture(base_name):
    res = []
    full_data = make_architecture_app_data(base_name)
    for slide in full_data:
        for elem in full_data[slide]:
            if elem[0] not in res:
                res.append(elem[0])
    return res








