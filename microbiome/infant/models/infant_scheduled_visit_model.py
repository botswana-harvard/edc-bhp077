from django.db import models

from datetime import datetime

from edc.subject.consent.models.base_consented_uuid_model import BaseConsentedUuidModel
from edc.entry_meta_data.managers import EntryMetaDataManager

from .infant_visit import InfantVisit
from .infant_off_study_mixin import InfantOffStudyMixin


class InfantScheduledVisitModel(InfantOffStudyMixin, BaseConsentedUuidModel):

    infant_visit = models.OneToOneField(InfantVisit)

    objects = models.Manager()

    entry_meta_data_manager = EntryMetaDataManager(InfantVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Visit Date and Time",
#         validators=[
#             datetime_not_before_study_start,
#             datetime_is_after_consent,
#             datetime_not_future,
#         ],
        default=datetime.today()
    )

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.get_visit().appointment.registered_subject.relative_identifier

    def get_subject_identifier(self):
        return self.get_visit().appointment.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.report_datetime

    def get_visit(self):
        return self.infant_visit

    class Meta:
        abstract = True
