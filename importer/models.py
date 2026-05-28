from django.db import models


class KT670(models.Model):
    br_code = models.CharField(max_length=10)
    br_name = models.CharField(max_length=300)
    br_rto = models.CharField(max_length=10)
    br_rpo = models.CharField(max_length=10)
    br_criticality = models.CharField(max_length=100)
    bu_code = models.CharField(max_length=100)
    bu_name = models.CharField(max_length=300)


class ESIS(models.Model):
    br_code = models.CharField(max_length=10)
    br_name = models.CharField(max_length=300)
    br_rpo = models.CharField(max_length=10)
    br_rto = models.CharField(max_length=10)
    br_criticality = models.CharField(max_length=100)
    bs_code = models.CharField(max_length=10)
    bs_name = models.CharField(max_length=300)
    bs_rpo = models.CharField(max_length=10)
    bs_rto = models.CharField(max_length=10)


class CMDB_v(models.Model):
    CI_name = models.CharField(max_length=100)
    VM_OS = models.CharField(max_length=100)
    VM_Platform = models.CharField(max_length=100)
    VM_vCenter = models.CharField(max_length=100)
    VM_Cores = models.CharField(max_length=100)
    VM_RAM = models.CharField(max_length=100)


class CMDB_p(models.Model):
    CI_name = models.CharField(max_length=100)
    CI_vendor = models.CharField(max_length=100)
    CI_serialNo = models.CharField(max_length=100)
    CI_OS = models.CharField(max_length=100)
    CI_MemoryCnt = models.CharField(max_length=100)
    CI_CoresCnt = models.CharField(max_length=100)


class CMDB_d(models.Model):
    CI_name = models.CharField(max_length=100)
    vDiskName = models.CharField(max_length=100)
    vDiskCapacityGb = models.CharField(max_length=100)
    vDiskClass = models.CharField(max_length=100)

