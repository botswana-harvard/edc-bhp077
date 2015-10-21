from edc.lab.lab_packing.models import BasePackingList


class PackingList(BasePackingList):

    class Meta:
        app_label = "microbiome_lab"
        verbose_name = 'Packing List'
