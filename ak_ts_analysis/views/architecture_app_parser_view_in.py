from ak_ts_analysis.views.architecture_app_parser_view import make_architecture_app_data
from ak_ts_analysis.views.architecture_app_parser_view import get_app_from_architecture
from ak_ts_analysis.views.licence_parser_view import get_app_from_licences
from ak_ts_analysis.views.applications_parser_view import get_app_from_applications
from ak_ts_analysis.views.compare_module import match_phrases
from ak_ts_analysis.views.sanctions_module import check_sanctions


def get_architecture_app_data(base_name):
    res_table_base = make_architecture_app_data(base_name)
    app_architecture = get_app_from_architecture(base_name)
    app_licences = get_app_from_licences(base_name)
    app_applications = get_app_from_applications(base_name)
    compare_licences = match_phrases(app_architecture, app_licences)

    for slide in res_table_base:
        for i in range(len(res_table_base[slide])):
            name = res_table_base[slide][i][0]
            arr_licences = []
            score = 0
            for k in range(len(compare_licences)):
                if compare_licences[k][0] == name:
                    arr_licences = compare_licences[k][1]
                    score = max(compare_licences[k][2])
                    break

            str_licences = ' '.join(arr_licences)

            if len(arr_licences) != 0:
                res_table_base[slide][i].append(str_licences)
                res_table_base[slide][i].append(round(score, 2))
            else:
                res_table_base[slide][i].append('error')
                res_table_base[slide][i].append(0)

    compare_applications = match_phrases(app_architecture, app_applications)

    for slide in res_table_base:
        for i in range(len(res_table_base[slide])):
            name = res_table_base[slide][i][0]
            arr_applications = []
            score = 0
            for k in range(len(compare_applications)):
                if compare_applications[k][0] == name:
                    arr_applications = compare_applications[k][1]
                    score = max(compare_applications[k][2])
                    break

            str_applications = ' '.join(arr_applications)

            if len(arr_applications) != 0:
                res_table_base[slide][i].append(str_applications)
                res_table_base[slide][i].append(round(score, 2))
            else:
                res_table_base[slide][i].append('error')
                res_table_base[slide][i].append(0)

    for slide in res_table_base:
        for i in range(len(res_table_base[slide])):
            name = res_table_base[slide][i][0]
            sanctions_find, sanctions_score, sanctions = check_sanctions(name)
            res_table_base[slide][i].append(sanctions_find)
            res_table_base[slide][i].append(round(sanctions_score, 2))
            res_table_base[slide][i].append(sanctions)

    return res_table_base








