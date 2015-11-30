from datetime import datetime, time

from edc.subject.adverse_event.models import BaseDeathReport

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel


class MaternalDeath (MaternalScheduledVisitModel, BaseDeathReport):

    def get_report_datetime(self):
        return datetime.combine(self.death_date, time(0, 0))

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Death"
        verbose_name_plural = "Maternal Death"
