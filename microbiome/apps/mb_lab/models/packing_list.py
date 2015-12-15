from django.db import models

from edc.lab.lab_packing.models import BasePackingList
from edc_base.model.models import BaseUuidModel

from ..managers import PackingListManager


class PackingList(BasePackingList, BaseUuidModel):

    def natural_key(self):
        return (self.timestamp, )

    objects = PackingListManager()

    @property
    def item_models(self):
        item_m = []
        item_m.append(models.get_model('mb_lab', 'InfantRequisition'))
        item_m.append(models.get_model('mb_lab', 'MaternalRequisition'))
        item_m.append(models.get_model('mb_lab', 'Aliquot'))
        return item_m

    @property
    def packing_list_item_model(self):
        return models.get_model('mb_lab', 'PackingListItem')

    class Meta:
        app_label = 'mb_lab'
        verbose_name = 'Packing List'
