from django.db import models

from edc.lab.lab_profile.models import BaseProfile
from edc.device.sync.models import BaseSyncUuidModel

from ..managers import ProfileManager

from .aliquot_type import AliquotType


class AliquotProfile(BaseProfile, BaseSyncUuidModel):

    aliquot_type = models.ForeignKey(
        AliquotType,
        verbose_name='Source aliquot type')

    objects = ProfileManager()

    def natural_key(self):
        return (self.name,)

    class Meta:
        app_label = 'mb_lab'
        db_table = 'mb_lab_profile'
