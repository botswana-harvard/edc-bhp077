from django.db import models
from django.utils import timezone

from edc.device.sync.models import BaseSyncUuidModel
from edc_base.audit_trail import AuditTrail
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.data_manager.models import TimePointStatusMixin

from ..managers import ScheduledModelManager

from .infant_off_study_mixin import InfantOffStudyMixin
from .infant_visit import InfantVisit


class InfantScheduledVisitModel(InfantOffStudyMixin, TimePointStatusMixin, BaseSyncUuidModel):

    """ A model completed by the user on the infant's scheduled visit. """

    infant_visit = models.OneToOneField(InfantVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Visit Date and Time",
        default=timezone.now
    )

    objects = ScheduledModelManager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(InfantVisit)

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.get_visit().appointment.registered_subject.relative_identifier

    def get_subject_identifier(self):
        return self.get_visit().appointment.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.report_datetime

    def get_visit(self):
        return self.infant_visit

    def natural_key(self):
        return (self.get_visit(),)
    natural_key.dependencies = ['mb_infant.infant_visit']

    class Meta:
        abstract = True
