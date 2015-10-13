from django.db import models
from django.core.urlresolvers import reverse

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel


class MaternalObstericalHistory(MaternalScheduledVisitModel):

    """Obsterical History for all mothers"""

    pregs_24wks_or_more = models.IntegerField(
        verbose_name="Number of pregnancies at least 24 weeks.?",
        help_text="")

    lost_before_24wks = models.IntegerField(
        verbose_name="Number of pregnancies lost before 24 weeks gestation",
        help_text="")

    lost_after_24wks = models.IntegerField(
        verbose_name="Number of pregnancies lost at or after 24 weeks gestation ",
        help_text="")

    live_children = models.IntegerField(
        verbose_name=("How many other living children does the participant currently have"
                      " (excluding baby to be enrolled in the study)"),
        help_text="")

    children_died_b4_5yrs = models.IntegerField(
        verbose_name=("How many of the participant's children died after birth before 5"
                      " years of age? "),
        help_text="")

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternalobstericalhistory_change', args=(self.id,))

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Obsterical History"
        verbose_name_plural = "Maternal Obsterical History"
