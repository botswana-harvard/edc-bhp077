from django.db import models
from edc_base.audit_trail import AuditTrail
from edc_death_report.models import DeathReportModelMixin

from edc.device.sync.models import BaseSyncUuidModel
from edc.entry_meta_data.managers.entry_meta_data_manager import EntryMetaDataManager
from edc_visit_tracking.models.crf_model_mixin import CrfModelMixin

from .maternal_visit import MaternalVisit


class MaternalDeathReport(CrfModelMixin, DeathReportModelMixin, BaseSyncUuidModel):

    """ A model completed by the user on the mother's death. """

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    def natural_key(self):
        return self.get_visit().natural_key()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Death Report"
