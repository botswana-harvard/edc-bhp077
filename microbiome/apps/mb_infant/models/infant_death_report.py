from django.db import models

from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_death_report.models import DeathReportModelMixin, InfantDrugRelationshipMixin

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantDeathReport (DeathReportModelMixin, InfantDrugRelationshipMixin, InfantScheduledVisitModel):

    """ A model completed by the user after an infant's death. """

    registered_subject = models.OneToOneField(RegisteredSubject)

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant Death Report"
