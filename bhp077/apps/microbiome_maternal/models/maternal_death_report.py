from datetime import datetime, time

from edc.subject.adverse_event.models import BaseDeathReport

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class MaternalDeath(BaseDeathReport, MaternalScheduledVisitModel):

    """ A model completed by the user on the mother's death. """
    CONSENT_MODEL = MaternalConsent

    def get_report_datetime(self):
        return datetime.combine(self.death_date, time(0, 0))

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Death"
        verbose_name_plural = "Maternal Death"
