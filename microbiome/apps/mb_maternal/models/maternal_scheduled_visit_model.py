from django.db import models

from edc.data_manager.models import TimePointStatusMixin
from edc.device.sync.models import BaseSyncUuidModel
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc_base.audit_trail import AuditTrail
from edc_consent.models import RequiresConsentMixin
from edc_offstudy.models import OffStudyMixin
from edc_visit_tracking.models import CrfModelMixin

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit


class MaternalScheduledVisitModel(CrfModelMixin, OffStudyMixin, RequiresConsentMixin,
                                  TimePointStatusMixin, BaseSyncUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    consent_model = MaternalConsent

    off_study_model = ('mb_maternal', 'MaternalOffStudy')

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    def natural_key(self):
        return (self.maternal_visit.natural_key(), )
    natural_key.dependencies = ['mb_maternal.maternal_visit']

    def __unicode__(self):
        return unicode(self.get_visit())

    class Meta:
        abstract = True
