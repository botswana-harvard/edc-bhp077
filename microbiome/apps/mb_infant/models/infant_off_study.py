from django.db import models

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.registration.models.registered_subject import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_offstudy.models import OffStudyModelMixin
from edc.subject.visit_tracking.managers.base_visit_tracking_manager import BaseVisitTrackingManager

from .infant_visit import InfantVisit


class InfantOffStudy(OffStudyModelMixin, BaseUuidModel):

    """ A model completed by the user when the infant is taken off study. """
    VISIT_MODEL = InfantVisit

    registered_subject = models.OneToOneField(RegisteredSubject)

    infant_visit = models.OneToOneField(InfantVisit)

    entry_meta_data_manager = EntryMetaDataManager(InfantVisit)

    objects = BaseVisitTrackingManager()

    history = AuditTrail()

    def natural_key(self):
        return self.get_visit().natural_key()

    def get_visit(self):
        return self.infant_visit

    def get_visit_model_cls(self):
        return InfantVisit

    def get_subject_identifier(self):
        return self.infant_visit.appointment.registered_subject.subject_identifier

    class Meta:
        app_label = "mb_infant
"
        verbose_name = "Infant Off-Study"
        verbose_name_plural = "Infant Off-Study"
