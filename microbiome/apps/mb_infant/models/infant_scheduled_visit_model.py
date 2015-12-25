from django.db import models

from edc.data_manager.models import TimePointStatusMixin
from edc.device.sync.models import BaseSyncUuidModel
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc_base.audit_trail import AuditTrail
from edc_offstudy.models import OffStudyMixin
from edc_visit_tracking.models import CrfModelMixin

from .infant_visit import InfantVisit


class InfantScheduledVisitModel(CrfModelMixin, OffStudyMixin, TimePointStatusMixin, BaseSyncUuidModel):

    """ A model completed by the user on the infant's scheduled visit. """

    off_study_model = ('mb_infant', 'InfantOffStudy')

    infant_visit = models.OneToOneField(InfantVisit)

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(InfantVisit)

    def __unicode__(self):
        return str(self.infant_visit)

    def __str__(self):
        return str(self.infant_visit)

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.get_visit().appointment.registered_subject.relative_identifier

    def natural_key(self):
        return (self.infant_visit.natural_key(), )
    natural_key.dependencies = ['mb_infant.infant_visit']

    class Meta:
        abstract = True
