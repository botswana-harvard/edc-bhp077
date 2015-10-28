from django.db import models
from django.core.urlresolvers import reverse

from .infant_fu import InfantFu
from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantFuDx(InfantScheduledVisitModel):

    infant_fu = models.OneToOneField(InfantFu)

    def __str__(self):
        return str(self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_infantfudx_change', args=(self.id,))

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant FollowUp: Dx"
        verbose_name_plural = "Infant FollowUp: Dx"
