from django.db import models

from edc_base.audit_trail import AuditTrail

from .infant_arv_proph import InfantArvProph
from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantArvProphMod(InfantScheduledVisitModel):
    """ A model completed by the user on the infant's nvp or azt prophylaxis modifications. """

    infant_arv_proph = models.ForeignKey(InfantArvProph)

    other_reason = models.CharField(
        verbose_name="Specify Other",
        max_length=100,
        null=True,
        blank=True,
    )

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.infant_arv_proph.infant_visit)

    class Meta:
        app_label = "mb_infant
"
        verbose_name = 'Infant NVP or AZT Proph: Mods'
        verbose_name_plural = 'Infant NVP or AZT Proph: Mods'
