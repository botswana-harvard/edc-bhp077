from django.db import models

from edc.device.sync.models import BaseSyncUuidModel
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.registration.models.registered_subject import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_constants.constants import OFF_STUDY, DEATH_VISIT
from edc_offstudy.models import OffStudyModelMixin
from edc_visit_tracking.managers import BaseVisitTrackingManager

from .infant_visit import InfantVisit


class InfantOffStudy(OffStudyModelMixin, BaseSyncUuidModel):

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
        app_label = 'mb_infant'
        verbose_name = "Infant Off-Study"
        verbose_name_plural = "Infant Off-Study"
