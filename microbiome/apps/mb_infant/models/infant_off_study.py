from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyModelMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .infant_visit import InfantVisit


class InfantOffStudy(CrfModelMixin, SyncModelMixin, OffStudyModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user when the infant is taken off study. """

    infant_visit = models.OneToOneField(InfantVisit)

    entry_meta_data_manager = CrfMetaDataManager(InfantVisit)

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant Off-Study"
        verbose_name_plural = "Infant Off-Study"
