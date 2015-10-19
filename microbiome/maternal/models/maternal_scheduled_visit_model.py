from datetime import datetime

from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.data_manager.models import TimePointStatusMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc_consent.models import RequiresConsentMixin

from ..managers import ScheduledModelManager

from maternal.models.maternal_off_study_mixin import MaternalOffStudyMixin
from maternal.models.maternal_visit import MaternalVisit


class MaternalScheduledVisitModel(MaternalOffStudyMixin, RequiresConsentMixin,
                                  TimePointStatusMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    maternal_visit = models.OneToOneField(MaternalVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.now,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    objects = ScheduledModelManager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    def natural_key(self):
        return self.get_visit().natural_key()

    def __unicode__(self):
        return unicode(self.get_visit())

    def get_report_datetime(self):
        return self.get_visit().report_datetime

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_visit(self):
        return self.maternal_visit

    def get_visit_code(self):
        try:
            return self.maternal_visit.appointment.visit_definition.code
        except AttributeError:
            return None

    @classmethod
    def visit_model(self):
        """Used by search in audit_trail"""
        return MaternalVisit

    class Meta:
        abstract = True
