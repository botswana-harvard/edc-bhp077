from django.db import models

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.registration.models.registered_subject import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel
from edc_offstudy.models import OffStudyModelMixin

from .maternal_visit import MaternalVisit
from ..managers import MaternalOffStudyManager


class MaternalOffStudy(OffStudyModelMixin, BaseSyncUuidModel):

    """ A model completed by the user that completed when the subject is taken off-study. """

    VISIT_MODEL = MaternalVisit

    registered_subject = models.OneToOneField(RegisteredSubject)

    maternal_visit = models.OneToOneField(MaternalVisit)

    objects = MaternalOffStudyManager(RegisteredSubject)

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    history = AuditTrail()

    def get_visit(self):
        return self.maternal_visit

    def get_visit_model_cls(self):
        return MaternalVisit

    def get_subject_identifier(self):
        return self.maternal_visit.appointment.registered_subject.subject_identifier

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Off Study"
        verbose_name_plural = "Maternal Off Study"
