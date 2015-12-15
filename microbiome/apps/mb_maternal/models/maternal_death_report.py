from django.db import models
from edc_base.audit_trail import AuditTrail
from edc_death_report.models import DeathReportMixin

from edc.subject.registration.models.registered_subject import RegisteredSubject
from edc.entry_meta_data.managers.entry_meta_data_manager import EntryMetaDataManager
from edc.device.sync.models import BaseSyncUuidModel

from .maternal_visit import MaternalVisit
from ..managers import ScheduledModelManager


class MaternalDeathReport(DeathReportMixin, BaseSyncUuidModel):

    """ A model completed by the user on the mother's death. """

    VISIT_MODEL = MaternalVisit

    registered_subject = models.OneToOneField(RegisteredSubject)

    maternal_visit = models.OneToOneField(MaternalVisit)

    objects = ScheduledModelManager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    def natural_key(self):
        return self.get_visit().natural_key()

    def get_report_datetime(self):
        return self.report_datetime

    def get_subject_identifier(self):
        return self.maternal_visit.appointment.registered_subject.subject_identifier

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Death Report"
