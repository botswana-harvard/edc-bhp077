from django.db import models
from datetime import datetime, time

from django.core.urlresolvers import reverse

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.adverse_event.models import BaseDeathReport
from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel

from .maternal_off_study_mixin import MaternalOffStudyMixin
from .maternal_visit import MaternalVisit
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel


class MaternalDeath (MaternalScheduledVisitModel, BaseDeathReport):


    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternaldeath_change', args=(self.id,))

    def get_report_datetime(self):
        return datetime.combine(self.death_date, time(0, 0))

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Death"
        verbose_name_plural = "Maternal Death"
