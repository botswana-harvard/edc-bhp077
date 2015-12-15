from django.db import models

from edc.lab.lab_profile.models import BaseProfileItem
from edc.device.sync.models import BaseSyncUuidModel

from ..managers import ProfileItemManager

from .aliquot_type import AliquotType
from .aliquot_profile import AliquotProfile


class AliquotProfileItem(BaseProfileItem, BaseSyncUuidModel):

    profile = models.ForeignKey(AliquotProfile)

    aliquot_type = models.ForeignKey(AliquotType)

    objects = ProfileItemManager()

    def __unicode__(self):
        return unicode(self.aliquot_type)

    def natural_key(self):
        return self.profile.natural_key() + self.aliquot_type.natural_key()

    class Meta:
        app_label = 'mb_lab'
        unique_together = ('profile', 'aliquot_type')
        db_table = 'mb_lab_profileitem'
