import os
import json
from ak_ts_analysis.views.compare_module import match_phrases

from django.conf import settings

# Путь к файлу внутри static/ak_ts_analysis/data
JSON_PATH = os.path.join(
    settings.BASE_DIR,
    'ak_ts_analysis',
    'static',
    'ak_ts_analysis',
    'data',
    'sanctions.json'
)


def load_software_data():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data  # ожидается список словарей [{ "name": ..., "origin": ... }, ...]


def check_sanctions(name):
    software_list = load_software_data()  # список словарей
    app_dict = {}
    app_list = []
    for item in software_list:
        app = item.get('name')
        app_list.append(app)
        app_dict[app] = item.get('origin')
    app_list = list(set(app_list))
    res_match = match_phrases([name], app_list)
    res_arr = []
    for elem in res_match:
        if elem[0] is not None:
            res_arr = elem
            break

    result_name = res_arr[1][0]
    score = res_arr[2][0]
    if result_name in app_dict:
        origin = app_dict[result_name]
    else:
        origin = ''
    if origin == 'СПО':
        result = 'СПО'
    elif origin == 'Россия':
        result = "Нет"
    elif origin == '':
        result = ''
    else:
        result = 'Да'
    return result_name, score, result
