from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_death_report.models import DeathReportModelMixin
from edc_export.models import ExportTrackingFieldsMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models.crf_model_mixin import CrfModelMixin

from .maternal_visit import MaternalVisit


class MaternalDeathReport(CrfModelMixin, SyncModelMixin, DeathReportModelMixin, ExportTrackingFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the mother's death. """

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(MaternalVisit)

    def natural_key(self):
        return self.maternal_visit.natural_key()
    natural_key.dependencies = ['mb_maternal.maternalvisit']

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Death Report"
