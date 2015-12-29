from django.db import models

from edc_base.model.models.base_list_model import BaseListModel


class AliquotConditionManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)


class AliquotCondition(BaseListModel):

    objects = AliquotConditionManager()

    class Meta:
        app_label = 'mb_lab'
