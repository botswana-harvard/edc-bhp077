from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO

from microbiome.apps.mb.choices import ARV_STATUS_WITH_NEVER

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantArvProph(InfantScheduledVisitModel):
    """ A model completed by the user on the infant's nvp or azt prophylaxis. """
    prophylatic_nvp = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was the baby supposed to be taking taking prophylactic antiretroviral medication for "
                     "any period since the last attended scheduled visit?",
    )

    arv_status = models.CharField(
        max_length=25,
        verbose_name=(
            "What is the status of the participant's ARV prophylaxis at this visit or since the last visit? "),
        choices=ARV_STATUS_WITH_NEVER,
        help_text="referring to prophylaxis other than single dose NVP",
        default='N/A',
    )

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.infant_visit)

    class Meta:
        app_label = 'mb_infant'
        verbose_name = 'Infant NVP or AZT Proph'
        verbose_name_plural = 'Infant NVP or AZT Proph'
