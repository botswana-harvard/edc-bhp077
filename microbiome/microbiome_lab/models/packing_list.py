from edc.lab.lab_packing.models import BasePackingList
from edc_base.model.models import BaseUuidModel


class PackingList(BasePackingList, BaseUuidModel):

    class Meta:
        app_label = "microbiome_lab"
        verbose_name = 'Packing List'
