from django.db import models

from edc_base.audit_trail import AuditTrail

from microbiome.apps.mb.choices import CIRCUMCISION

from .infant_crf_visit_model import InfantCrfModel


class InfantCircumcision(InfantCrfModel):

    """ A model completed by the user on the infant's circumcision. """
    circumcised = models.CharField(
        max_length=15,
        verbose_name="In performing your physical exam, you determined this male infant to be:",
        choices=CIRCUMCISION)

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant Male Circumcision"
