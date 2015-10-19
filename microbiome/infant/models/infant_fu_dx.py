from django.db import models
from django.core.urlresolvers import reverse

from edc_base.model.models import BaseUuidModel

from .infant_fu import InfantFu


class InfantFuDx(BaseUuidModel):

    infant_fu = models.OneToOneField(InfantFu)

    def __str__(self):
        return str(self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantfudx_change', args=(self.id,))

    class Meta:
        app_label = "infant"
        verbose_name = "Infant FollowUp: Dx"
        verbose_name_plural = "Infant FollowUp: Dx"
