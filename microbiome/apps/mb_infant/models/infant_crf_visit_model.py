from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .infant_visit import InfantVisit


class InfantCrfModel(
        CrfModelMixin, SyncModelMixin, OffStudyMixin, BaseUuidModel):

    """ A model completed by the user on the infant's scheduled visit. """

    off_study_model = ('mb_infant', 'InfantOffStudy')

    infant_visit = models.OneToOneField(InfantVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(InfantVisit)

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
