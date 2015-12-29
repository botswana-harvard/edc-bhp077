from edc_base.audit_trail import AuditTrail
from edc_offstudy.models import OffStudyModelMixin

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class MaternalOffStudy(OffStudyModelMixin, MaternalScheduledVisitModel):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    consent_model = MaternalConsent

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Off Study"
