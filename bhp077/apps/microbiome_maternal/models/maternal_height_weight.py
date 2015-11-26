from django.core.urlresolvers import reverse
from django.db import models

from edc_base.audit_trail import AuditTrail

from .maternal_consent import MaternalConsent
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel


class MaternalHeightWeight(MaternalScheduledVisitModel):

    """Height, Weight details for all mothers"""

    CONSENT_MODEL = MaternalConsent

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Mother's weight? ",
        help_text="Measured in Kilograms (kg)")
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Mother's height? ",
        help_text="Measured in Centimeters (cm)")
    systolic_bp = models.IntegerField(
        max_length=3,
        verbose_name="Mother's systolic blood pressure?",
        help_text="in mm e.g. 120, should be between 75 and 175.")
    diastolic_bp = models.IntegerField(
        max_length=3,
        verbose_name="Mother's diastolic blood pressure?",
        help_text="in hg e.g. 80, should be between 35 and 130.")

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternalheightweight_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Height & Weight'
        verbose_name_plural = 'Maternal Height & Weight'
