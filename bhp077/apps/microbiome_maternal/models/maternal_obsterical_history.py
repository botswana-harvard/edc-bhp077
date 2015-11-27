from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class MaternalObstericalHistory(MaternalScheduledVisitModel):

    """Obsterical History for all mothers"""

    CONSENT_MODEL = MaternalConsent

    prev_pregnancies = models.IntegerField(
        verbose_name="Not including this pregnancy, how many previous pregnancies for this participant?",
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
        help_text="")
    pregs_24wks_or_more = models.IntegerField(
        verbose_name="Number of pregnancies at least 24 weeks.?",
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
        help_text="")

    lost_before_24wks = models.IntegerField(
        verbose_name="Number of pregnancies lost before 24 weeks gestation",
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
        help_text="")

    lost_after_24wks = models.IntegerField(
        verbose_name="Number of pregnancies lost at or after 24 weeks gestation ",
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
        help_text="")

    live_children = models.IntegerField(
        verbose_name=("How many other living children does the participant currently have"
                      " (excluding baby to be enrolled in the study)"),
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
        help_text="")

    children_died_b4_5yrs = models.IntegerField(
        verbose_name=("How many of the participant's children died after birth before 5"
                      " years of age? "),
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
        help_text="")

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternalobstericalhistory_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Obsterical History"
        verbose_name_plural = "Maternal Obsterical History"
