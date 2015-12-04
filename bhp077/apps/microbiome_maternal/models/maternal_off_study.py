from django.db import models

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.off_study.models import BaseOffStudy
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel

from .maternal_visit import MaternalVisit


class MaternalOffStudy(BaseOffStudy, BaseUuidModel):

    """ A model completed by the user that completed when the subject is taken off-study. """

    maternal_visit = models.OneToOneField(MaternalVisit)

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    objects = models.Manager()

    history = AuditTrail()

    def get_visit(self):
        return self.maternal_visit

    def get_visit_model_cls(self):
        return MaternalVisit

    def get_subject_identifier(self):
        return self.maternal_visit.appointment.registered_subject.subject_identifier

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Off Study"
        verbose_name_plural = "Maternal Off Study"
