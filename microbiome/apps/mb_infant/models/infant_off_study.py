from django.db import models

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_offstudy.models import OffStudyModelMixin
from edc.device.sync.models import BaseSyncUuidModel
from edc_visit_tracking.models import CrfModelMixin

from .infant_visit import InfantVisit


class InfantOffStudy(CrfModelMixin, OffStudyModelMixin, BaseSyncUuidModel):

    """ A model completed by the user when the infant is taken off study. """

    registered_subject = models.OneToOneField(RegisteredSubject)

    infant_visit = models.OneToOneField(InfantVisit)

    entry_meta_data_manager = EntryMetaDataManager(InfantVisit)

    history = AuditTrail()

    def natural_key(self):
        return self.get_visit().natural_key()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant Off-Study"
        verbose_name_plural = "Infant Off-Study"
