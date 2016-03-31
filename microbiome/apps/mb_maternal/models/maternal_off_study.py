from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyModelMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .maternal_consent import MaternalConsent
from .maternal_visit import MaternalVisit


class MaternalOffStudy(OffStudyModelMixin, CrfModelMixin, SyncModelMixin,
                       RequiresConsentMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the visit when the mother is taken off-study. """

    consent_model = MaternalConsent

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(MaternalVisit)

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Off Study"
