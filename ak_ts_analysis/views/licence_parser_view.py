import os
import json
from django.conf import settings
import re
from ak_ts_analysis.views.applications_parser_view import get_app_from_applications
from ak_ts_analysis.views.architecture_app_parser_view import get_app_from_architecture
from ak_ts_analysis.views.compare_module import match_phrases


def get_licences_slides(name):
    json_filename = os.path.join(settings.MEDIA_ROOT, 'pptx_outputs', f"output_{name}", f"output_{name}.json")
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = []
    for item in data:
        if 'ЛИЦЕНЗИРОВАНИЕ' in str(item.get("title")).upper():
            result.append(item)

    return result


def get_numbers(table):
    numbers = {
        'N_name': -1,
        'N_count': -1,
        'N_provision': -1,
        'N_restriction_type': -1,
        'N_time_limit': -1,
        'N_competition': -1,
        'N_binding': -1,
    }

    for i in range(2):
        row = table[i]
        for k in range(len(row)):
            tmp_arr = [numbers['N_name'],
                       numbers['N_count'],
                       numbers['N_provision'],
                       numbers['N_restriction_type'],
                       numbers['N_time_limit'],
                       numbers['N_competition'],
                       numbers['N_binding']]
            if k in tmp_arr:
                continue
            cell = row[k].upper()
            if 'НАИМЕНОВАНИЕ' in cell and 'ПРОДУКТА' in cell and numbers['N_name'] == -1:
                numbers['N_name'] = k
            elif 'КОЛ-ВО' in cell and numbers['N_count'] == -1:
                numbers['N_count'] = k
            elif 'ОБЕСПЕЧЕНИЕ' in cell and numbers['N_provision'] == -1:
                numbers['N_provision'] = k
            elif 'ТИП' in cell and 'ОГРАНИЧЕНИ' in cell and numbers['N_restriction_type'] == -1:
                numbers['N_restriction_type'] = k
            elif 'ОГРАНИЧЕНИ' in cell and 'СРОКУ' in cell and numbers['N_time_limit'] == -1:
                numbers['N_time_limit'] = k
            elif 'КОНКУРЕНТНОСТЬ' in cell and numbers['N_competition'] == -1:
                numbers['N_competition'] = k
            elif 'ПРИВЯЗКА' in cell and numbers['N_binding'] == -1:
                numbers['N_binding'] = k

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


def slide_parser(slide):
    data = {}
    tables = slide['tables']
    for table in tables:
        numbers = get_numbers(table)
        for row in table:
            cell_name = clean_string(row[numbers['N_name']])
            if cell_name.upper() == 'Наименование лицензируемого продукта'.upper():
                cell_name = 'Продукт'
            cell_count = clean_string(row[numbers['N_count']])
            cell_provision = clean_string(row[numbers['N_provision']])
            #cell_restriction_type = clean_string(row[numbers['N_restriction_type']])
            #cell_time_limit = clean_string(row[numbers['N_time_limit']])
            #cell_competition = clean_string(row[numbers['N_competition']])
            #cell_binding = clean_string(row[numbers['N_binding']])

            data[cell_name] = {
                'name': cell_name,
                'count': cell_count,
                'provision': cell_provision,
                #'restriction_type': cell_restriction_type,
                #'time_limit': cell_time_limit,
                #'competition': cell_competition,
                #'binding': cell_binding
            }

    return data


def make_licences_data(base_name):
    slides = get_licences_slides(base_name)

    parsing_res = {}
    for slide in slides:
        header = str(slide['slide']) + ' - ' + str(slide['title'])
        slide_data = slide_parser(slide)
        parsing_res[header] = slide_data

    return parsing_res


def get_app_from_licences(base_name):
    res = []
    full_data = make_licences_data(base_name)
    for slide in full_data:
        for elem in full_data[slide]:
            if elem not in res:
                res.append(elem)
    res.pop(0)
    return res

