from django.db import models
from datetime import datetime, time

from django.core.urlresolvers import reverse

from edc.audit.audit_trail import AuditTrail
from edc.subject.adverse_event.models import BaseDeathReport
from edc.entry_meta_data.managers import EntryMetaDataManager

from .maternal_off_study_mixin import MaternalOffStudyMixin
from .maternal_visit import MaternalVisit


class MaternalDeath (MaternalOffStudyMixin, BaseDeathReport):

    maternal_visit = models.OneToOneField(MaternalVisit)

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    def get_absolute_url(self):
        return reverse('admin:maternal_maternaldeath_change', args=(self.id,))

    def get_report_datetime(self):
        return datetime.combine(self.death_date, time(0, 0))

    class Meta:
        app_label = "maternal"
        verbose_name = "Maternal Death"
        verbose_name_plural = "Maternal Death"
