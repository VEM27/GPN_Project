from rest_framework import serializers
from importer.models import KT670, ESIS, CMDB_v, CMDB_d, CMDB_p


class KT670Serializer(serializers.ModelSerializer):
    class Meta:
        model = KT670
        fields = ['br_code', 'br_name', 'br_rto', 'br_rpo', 'br_criticality', 'bu_code', 'bu_name']


class ESIS_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ESIS
        fields = ['br_code', 'br_name', 'br_rpo', 'br_rto', 'br_criticality', 'bs_code', 'bs_name', 'bs_rpo', 'bs_rto']


class CMDB_v_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CMDB_v
        fields = ['CI_name', 'VM_OS', 'VM_Platform', 'VM_vCenter', 'VM_Cores', 'VM_RAM']


class CMDB_p_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CMDB_p
        fields = ['CI_name', 'CI_vendor', 'CI_serialNo', 'CI_OS', 'CI_MemoryCnt', 'CI_CoresCnt']


class CMDB_d_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CMDB_d
        fields = ['CI_name', 'vDiskName', 'vDiskCapacityGb', 'vDiskClass']

