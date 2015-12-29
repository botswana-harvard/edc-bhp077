from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin
from lis.specimen.lab_aliquot_list.models import BaseAliquotType


class AliquotTypeManager(models.Manager):

    def get_by_natural_key(self, alpha_code, numeric_code):
        return self.get(alpha_code=alpha_code, numeric_code=numeric_code)


class AliquotType(BaseAliquotType, SyncModelMixin, BaseUuidModel):

    objects = AliquotTypeManager()

    class Meta:
        app_label = 'mb_lab'
        ordering = ["name"]
