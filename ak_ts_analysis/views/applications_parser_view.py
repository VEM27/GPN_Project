import os
import json
from django.conf import settings
import re


def get_applications_slides(name):
    json_filename = os.path.join(settings.MEDIA_ROOT, 'pptx_outputs', f"output_{name}", f"output_{name}.json")
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = []
    for item in data:
        if 'Используемые технологии'.upper() in str(item.get("title")).upper():
            result.append(item)

    return result


def get_numbers(table):
    numbers = {
        'N_br': [],
        'N_bs': [],
        'N_pp': [],
        'N_sp': [],
        'N_db': [],
        'N_os': [],
        'N_arm': [],
        'N_comment': [],
        'N_as_is': [],
        'N_to_be': [],
        'N_no_class': []
    }

    for i in range(2):
        row = table[i]
        last = None
        for k in range(len(row)):
            cell = row[k].upper()
            if 'РЕШЕНИЕ' in cell and len(numbers['N_br']) == 0:
                numbers['N_br'].append(k)
                last = 'N_br'
            elif 'СИСТЕМА' in cell and len(numbers['N_bs']) == 0:
                numbers['N_bs'].append(k)
                last = 'N_bs'
            elif 'ПРИКЛАДНАЯ' in cell and len(numbers['N_pp']) == 0:
                numbers['N_pp'].append(k)
                last = 'N_pp'
            elif 'СИСТЕМНАЯ' in cell and len(numbers['N_sp']) == 0:
                numbers['N_sp'].append(k)
                last = 'N_sp'
            elif 'СУБД' in cell and len(numbers['N_db']) == 0:
                numbers['N_db'].append(k)
                last = 'N_db'
            elif ('ОС' in cell or 'OC' in cell) and 'РМ' not in cell and len(numbers['N_os']) == 0:
                numbers['N_os'].append(k)
                last = 'N_os'
            elif ('АРМ' in cell or 'РМ ' in cell or ' РМ' in cell or ' PM' in cell or 'PM ' in cell) and len(numbers['N_arm']) == 0:
                numbers['N_arm'].append(k)
                last = 'N_arm'
            elif 'КОММЕНТАРИ' in cell and len(numbers['N_comment']) == 0:
                numbers['N_comment'].append(k)
                last = 'N_comment'
            elif 'AS IS' in cell or 'AS-IS' in cell or 'ASIS' in cell:
                numbers['N_as_is'].append(k)
                last = 'N_as_is'
            elif 'TO BE' in cell or 'TO-BE' in cell or 'TOBE' in cell:
                numbers['N_to_be'].append(k)
                last = 'N_to_be'
            elif cell == '' and last:
                numbers[last].append(k)
            elif cell != '':
                numbers['N_no_class'].append(k)
                last = 'N_no_class'

    return numbers


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


def get_data_from_table(row, numbers, key, note):
    res_row = []
    for elem in numbers[key]:
        app_name = clean_string(row[elem])
        if app_name != '' and elem in numbers['N_to_be']:
            res_row = [app_name, 'To Be', note]
    if len(res_row) == 0:
        for elem in numbers[key]:
            app_name = clean_string(row[elem])
            if app_name != '':
                res_row = [app_name, 'To Be ?', note]

    return res_row


def make_unique(data):
    seen = set()
    result = []
    for row in data:
        key = row[0]
        if key not in seen:
            seen.add(key)
            result.append(row)

    return result


def slide_parser(slide):
    res_table = []
    tables = slide['tables']
    for table in tables:
        numbers = get_numbers(table)
        for row in table:
            upper_row = [elem.upper() for elem in row]
            if row == table[0] or "AS IS" in upper_row or "AS-IS" in upper_row or "ASIS" in upper_row or "TO BE" in upper_row or "TO-BE" in upper_row or "TOBE" in upper_row:
                continue
            if '1' in row and '2' in row and '3' in row:
                continue

            res_row = get_data_from_table(row, numbers, 'N_pp', 'ПП')
            if len(res_row) != 0:
                res_table.append(res_row)
            res_row = get_data_from_table(row, numbers, 'N_sp', 'СП')
            if len(res_row) != 0:
                res_table.append(res_row)
            res_row = get_data_from_table(row, numbers, 'N_db', 'СУБД')
            if len(res_row) != 0:
                res_table.append(res_row)
            res_row = get_data_from_table(row, numbers, 'N_os', 'ОС')
            if len(res_row) != 0:
                res_table.append(res_row)
            res_row = get_data_from_table(row, numbers, 'N_arm', 'АРМ')
            if len(res_row) != 0:
                res_table.append(res_row)
            res_row = get_data_from_table(row, numbers, 'N_no_class', '?')
            if len(res_row) != 0:
                res_table.append(res_row)

    unique_res_table = make_unique(res_table)
    return unique_res_table


def make_applications_data(base_name):
    slides = get_applications_slides(base_name)
    parsing_res = {}
    for slide in slides:
        header = str(slide['slide']) + ' - ' + str(slide['title'])
        slide_data = slide_parser(slide)
        parsing_res[header] = slide_data

    return parsing_res


def get_app_from_applications(base_name):
    res = []
    full_data = make_applications_data(base_name)
    for slide in full_data:
        for elem in full_data[slide]:
            if elem[0] not in res:
                res.append(elem[0])

    return res
