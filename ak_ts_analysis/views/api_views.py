from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from importer.models import KT670, ESIS, CMDB_v, CMDB_p, CMDB_d
from ak_ts_analysis.serializers import KT670Serializer, ESIS_Serializer, CMDB_d_Serializer, CMDB_v_Serializer, CMDB_p_Serializer
from ak_ts_analysis.views.passport_parser_view import get_passport_data
from ak_ts_analysis.views.characteristics_parser_view import get_characteristics_data
from ak_ts_analysis.views.licence_parser_view_in import get_licences_data
from ak_ts_analysis.views.applications_parser_view_in import get_applications_data
from ak_ts_analysis.views.architecture_app_parser_view_in import get_architecture_app_data


class KT670Detail(APIView):
    def get(self, request):
        value = request.GET.get('value') or ''
        field = request.GET.get('field') or ''
        base_name = request.GET.get('base_name') or ''
        try:
            objs = KT670.objects.filter(**{f"{field}__icontains": value})
            serializer = KT670Serializer(objs, many=True)

            file_br_name, file_rto, file_rpo = get_passport_data(base_name)

            extra_row = {
                'br_code': 'ИЗ ФАЙЛА',
                'br_name': file_br_name,
                'bu_code': '',
                'bu_name': '',
                'br_rpo': file_rpo,
                'br_rto': file_rto,
                'br_criticality': '',
            }

            data = serializer.data + [extra_row]
            return Response(data)

        except KT670.DoesNotExist:
            return Response({'error': 'KT670 not found'}, status=404)


class ESISDetail(APIView):
    def get(self, request):
        value = request.GET.get('value') or ''
        field = request.GET.get('field') or ''
        base_name = request.GET.get('base_name') or ''
        try:
            objs = ESIS.objects.filter(**{f"{field}__icontains": value})
            serializer = ESIS_Serializer(objs, many=True)

            file_br_name, file_rto, file_rpo = get_passport_data(base_name)

            extra_row = {
                'br_code': 'ИЗ ФАЙЛА',
                'br_name': file_br_name,
                'br_rpo': file_rpo,
                'br_rto': file_rto,
                'br_criticality': '',
                'bs_code': '',
                'bs_name': '',
                'bs_rpo': '',
                'bs_rto': '',
            }

            data = serializer.data + [extra_row]
            return Response(data)

        except ESIS.DoesNotExist:
            return Response({'error': 'ESIS_BR not found'}, status=404)


class characteristicsDetail(APIView):

    def sum_disk_capacity_by_class(self, data):
        result = {}

        for item in data:
            tmp_res = {
                "Gold": 0,
                "Silver": 0,
                "Bronze": 0,
                "Iron": 0,
                "Other": 0
            }

            cls = item.get("vDiskClass", "Other")
            if not cls:  # если None или пустая строка
                cls = "Other"

            capacity_str = item.get("vDiskCapacityGb", "0")
            if not capacity_str:  # если None или пустая строка
                capacity_str = "0"

            try:
                capacity = float(capacity_str)
                if capacity.is_integer():
                    capacity = int(capacity)
            except ValueError:
                capacity = 0

            if cls not in tmp_res:
                cls = "Other"

            tmp_res[cls] += capacity

            name = item.get("CI_name", "")
            if name in result:
                result[name]["Gold"] += tmp_res['Gold']
                result[name]["Silver"] += tmp_res['Silver']
                result[name]["Bronze"] += tmp_res['Bronze']
                result[name]["Iron"] += tmp_res['Iron']
                result[name]["Other"] += tmp_res['Other']
            else:
                result[name] = tmp_res

        return result

    def get(self, request):
        base_name = request.GET.get('base_name') or ''
        try:

            data = get_characteristics_data(base_name)

            for header in data:
                print(header)
                for server in data[header]:
                    print(server)
                    v_objs = CMDB_v.objects.filter(CI_name__iexact=server.upper())
                    if v_objs.exists():
                        v_obj = v_objs.first()
                        v_serializer = CMDB_v_Serializer(v_obj, many=False)
                    else:
                        v_obj = None
                        v_serializer = None

                    p_objs = CMDB_p.objects.filter(CI_name__iexact=server.upper())
                    if p_objs.exists():
                        p_obj = p_objs.first()
                        p_serializer = CMDB_p_Serializer(p_obj, many=False)
                    else:
                        p_obj = None
                        p_serializer = None

                    d_objs = CMDB_d.objects.filter(CI_name__iexact=server.upper())
                    d_serializer = CMDB_d_Serializer(d_objs, many=True)

                    d_dict = self.sum_disk_capacity_by_class(d_serializer.data)

                    if v_obj:
                        item = v_serializer.data
                        item.pop("VM_Platform", None)
                        item['VM_vCenter'] = item['VM_vCenter'].split('.')[0]
                        item['VM_RAM'] = int(item['VM_RAM']) // 1024
                        if item['CI_name'] in d_dict:
                            v_data = item | d_dict[item['CI_name']]
                        else:
                            tmp_dict = {
                                "Gold": 0,
                                "Silver": 0,
                                "Bronze": 0,
                                "Iron": 0,
                                "Other": 0
                            }
                            v_data = item | tmp_dict

                        data[header][server]['cmdb_v'] = v_data

                    if p_obj:
                        item = p_serializer.data
                        if item['CI_name'] in d_dict:
                            p_data = item | d_dict[item['CI_name']]
                        else:
                            tmp_dict = {
                                "Gold": 0,
                                "Silver": 0,
                                "Bronze": 0,
                                "Iron": 0,
                                "Other": 0
                            }
                            p_data = item | tmp_dict

                        data[header][server]['cmdb_p'] = p_data

            print(data)
            return Response(data)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return Response({'error': str(e)}, status=500)


class licenceDetail(APIView):

    def get(self, request):
        base_name = request.GET.get('base_name') or ''
        try:
            data = get_licences_data(base_name)

            return Response(data)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return Response({'error': str(e)}, status=500)


class applicationsDetail(APIView):

    def get(self, request):
        base_name = request.GET.get('base_name') or ''
        try:
            data = get_applications_data(base_name)

            return Response(data)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return Response({'error': str(e)}, status=500)


class architectureAppDetail(APIView):

    def get(self, request):
        base_name = request.GET.get('base_name') or ''
        try:
            data = get_architecture_app_data(base_name)

            return Response(data)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return Response({'error': str(e)}, status=500)