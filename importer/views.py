import pandas as pd
from django.shortcuts import render, redirect
from .models import KT670, ESIS, CMDB_v, CMDB_d, CMDB_p


def clean_value(val):
    if pd.isna(val):
        return ''

    try:
        float_val = float(val)
        if float_val.is_integer():
            return str(int(float_val))
        else:
            return str(float_val)
    except (ValueError, TypeError):
        return str(val).upper()



def upload_excel(request):
    if request.method == "POST":
        submit_type = request.POST.get("submit_type")

        if submit_type == "kt670" and request.FILES.get("kt670_file"):
            df = pd.read_excel(request.FILES["kt670_file"], header=None, skiprows=20)
            KT670.objects.all().delete()
            KT670.objects.all().delete()
            objs = []
            for _, row in df.iterrows():
                objs.append(KT670(
                    br_code=clean_value(row[0]).strip(),
                    br_name=clean_value(row[1]).strip(),
                    br_rto=clean_value(row[3]).strip(),
                    br_rpo=clean_value(row[4]).strip(),
                    br_criticality=clean_value(row[5]).strip(),
                    bu_code=clean_value(row[7]).strip(),
                    bu_name=clean_value(row[8]).strip()
                ))
            KT670.objects.bulk_create(objs, batch_size=1000)

        elif submit_type == "esis" and request.FILES.get("esis_file"):
            df = pd.read_excel(request.FILES["esis_file"], header=None, skiprows=2)
            ESIS.objects.all().delete()
            objs = []
            for _, row in df.iterrows():
                objs.append(ESIS(
                    br_code=clean_value(row[0]).strip(),
                    br_name=clean_value(row[1]).strip(),
                    br_rpo=clean_value(row[2]).strip(),
                    br_rto=clean_value(row[3]).strip(),
                    br_criticality=clean_value(row[4]).strip(),
                    bs_code=clean_value(row[5]).strip(),
                    bs_name=clean_value(row[6]).strip(),
                    bs_rpo=clean_value(row[7]).strip(),
                    bs_rto=clean_value(row[8]).strip(),
                ))
            ESIS.objects.bulk_create(objs, batch_size=1000)

        elif submit_type == "cmdb" and request.FILES.get("cmdb_file"):
            df = pd.read_excel(request.FILES["cmdb_file"], sheet_name="v", header=None, skiprows=2)
            CMDB_v.objects.all().delete()
            objs = []
            for _, row in df.iterrows():
                objs.append(CMDB_v(
                    CI_name=clean_value(row[0]).strip(),
                    VM_OS=clean_value(row[1]).strip(),
                    VM_Platform=clean_value(row[2]).strip(),
                    VM_vCenter=clean_value(row[3]).strip(),
                    VM_Cores=clean_value(row[4]).strip(),
                    VM_RAM=clean_value(row[5]).strip(),
                ))
            CMDB_v.objects.bulk_create(objs, batch_size=1000)

            df = pd.read_excel(request.FILES["cmdb_file"], sheet_name="p", header=None, skiprows=2)
            CMDB_p.objects.all().delete()
            objs = []
            for _, row in df.iterrows():
                objs.append(CMDB_p(
                    CI_name=clean_value(row[0]).strip(),
                    CI_vendor=clean_value(row[1]).strip(),
                    CI_serialNo=clean_value(row[2]).strip(),
                    CI_OS=clean_value(row[3]).strip(),
                    CI_MemoryCnt=clean_value(row[4]).strip(),
                    CI_CoresCnt=clean_value(row[5]).strip(),
                ))
            CMDB_p.objects.bulk_create(objs, batch_size=1000)

            df = pd.read_excel(request.FILES["cmdb_file"], sheet_name="d", header=None, skiprows=2)
            CMDB_d.objects.all().delete()
            objs = []
            for _, row in df.iterrows():
                objs.append(CMDB_d(
                    CI_name=clean_value(row[0]).strip(),
                    vDiskName=clean_value(row[1]).strip(),
                    vDiskCapacityGb=clean_value(row[2]).strip(),
                    vDiskClass=str(row[3]).strip(),
                ))
            CMDB_d.objects.bulk_create(objs, batch_size=1000)

        return render(request, "importer/upload.html", {"success": True})

    return render(request, "importer/upload.html")
