from django.db import models

from edc.lab.lab_profile.models import BaseProfile
# from edc_base.model.models import BaseUuidModel

from .managers import ProfileManager

from .aliquot_type import AliquotType


class AliquotProfile(BaseProfile):

    aliquot_type = models.ForeignKey(
        AliquotType,
        verbose_name='Source aliquot type')

    objects = ProfileManager()

    def natural_key(self):
        return (self.name,)

    class Meta:
        app_label = 'microbiome_lab'
        db_table = 'microbiome_lab_profile'
