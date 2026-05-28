from ak_ts_analysis.views.licence_parser_view import make_licences_data
from ak_ts_analysis.views.licence_parser_view import get_app_from_licences
from ak_ts_analysis.views.architecture_app_parser_view import get_app_from_architecture
from ak_ts_analysis.views.applications_parser_view import get_app_from_applications
from ak_ts_analysis.views.compare_module import match_phrases
from ak_ts_analysis.views.sanctions_module import check_sanctions


def get_licences_data(base_name):
    res_table_base = make_licences_data(base_name)
    app_architecture = get_app_from_architecture(base_name)
    app_licences = get_app_from_licences(base_name)
    app_applications = get_app_from_applications(base_name)

    compare_architecture = match_phrases(app_licences, app_architecture)

    for slide in res_table_base:
        for name in res_table_base[slide]:
            if name == 'Продукт':
                res_table_base[slide][name]['architecture'] = 'Архитектура-ПО'
                res_table_base[slide][name]['architecture_score'] = 'a_s'
                continue

            arr_architecture = []
            score = 0
            for k in range(len(compare_architecture)):
                if compare_architecture[k][0] == name:
                    arr_architecture = compare_architecture[k][1]
                    score = max(compare_architecture[k][2])
                    break

            str_architecture = ' '.join(arr_architecture)

            if len(arr_architecture) != 0:
                res_table_base[slide][name]['architecture'] = str_architecture
                res_table_base[slide][name]['architecture_score'] = round(score, 2)
            else:
                res_table_base[slide][name]['architecture'] = 'error'
                res_table_base[slide][name]['architecture_score'] = 0

    compare_applications = match_phrases(app_licences, app_applications)

    for slide in res_table_base:
        for name in res_table_base[slide]:
            if name == 'Продукт':
                res_table_base[slide][name]['applications'] = 'Исп. технологии'
                res_table_base[slide][name]['applications_score'] = 't_s'
                continue

            arr_applications = []
            score = 0
            for k in range(len(compare_applications)):
                if compare_applications[k][0] == name:
                    arr_applications = compare_applications[k][1]
                    score = max(compare_applications[k][2])
                    break

            str_applications = ' '.join(arr_applications)

            if len(arr_applications) != 0:
                res_table_base[slide][name]['applications'] = str_applications
                res_table_base[slide][name]['applications_score'] = round(score, 2)
            else:
                res_table_base[slide][name]['applications'] = 'error'
                res_table_base[slide][name]['applications_score'] = 0

    for slide in res_table_base:
        for name in res_table_base[slide]:
            if name == 'Продукт':
                res_table_base[slide][name]['sanctions_find'] = 'Санкции (поиск)'
                res_table_base[slide][name]['sanctions_score'] = 's_s'
                res_table_base[slide][name]['sanctions'] = 'Санкции'
                continue
            sanctions_find, sanctions_score, sanctions = check_sanctions(name)
            res_table_base[slide][name]['sanctions_find'] = sanctions_find
            res_table_base[slide][name]['sanctions_score'] = round(sanctions_score, 2)
            res_table_base[slide][name]['sanctions'] = sanctions

    return res_table_base
