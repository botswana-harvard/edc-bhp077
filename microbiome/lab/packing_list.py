from edc.lab.lab_packing.models import BasePackingList


class PackingList(BasePackingList):

    class Meta:
        app_label = "lab"
        verbose_name = 'Packing List'
