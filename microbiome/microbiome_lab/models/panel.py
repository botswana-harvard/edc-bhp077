from django.db import models

from edc.lab.lab_clinic_api.choices import PANEL_TYPE
from edc.lab.lab_clinic_api.models import TestCode

from lis.specimen.lab_panel.models import BasePanel

from .aliquot_type import AliquotType

from .managers import PanelManager


class Panel(BasePanel):

    test_code = models.ManyToManyField(TestCode, null=True, blank=True, related_name='+')

    aliquot_type = models.ManyToManyField(
        AliquotType,
        help_text='Choose all that apply',)

    panel_type = models.CharField(max_length=15, choices=PANEL_TYPE, default='TEST')

    objects = PanelManager()

    def save(self, *args, **kwargs):
        super(Panel, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.name, )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'microbiome_lab'
