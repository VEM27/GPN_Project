import os
import json
from django.conf import settings


def get_tables_from_passport(name):
    json_filename = os.path.join(settings.MEDIA_ROOT, 'pptx_outputs', f"output_{name}", f"output_{name}.json")
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        if item.get("title") == "Паспорт проекта":
            return item.get("tables")

    return None  # если не найдено


def extract_rto_rpo(tables):
    rto = None
    rpo = None

    for table in tables:
        for row in table:  # table — это список строк
            if not isinstance(row, list) or len(row) < 2:
                continue  # пропускаем некорректные строки

            key = str(row[0]).strip().upper()
            value = row[1]

            if key == "RTO":
                rto = value
            elif key == "RPO":
                rpo = value

            if rto and rpo:
                return rto, rpo

    if rto is None:
        rto = '-'
    if rpo is None:
        rpo = '-'

    return rto, rpo


def extract_br(tables):
    for table in tables:
        for row in table:
            if not isinstance(row, list) or len(row) < 2:
                continue

            key = str(row[0]).strip()
            if key == "ИТ решение:":
                return row[1]

    return '-'  # если не найдено


def get_passport_data(base_name):
    tables = get_tables_from_passport(base_name)
    rto, rpo = extract_rto_rpo(tables)
    br = extract_br(tables)
    return br, rto, rpo

