from django.core.urlresolvers import reverse
from django.db import models

from edc_constants.choices import YES_NO

from ..maternal_choices import LIVE_STILL_BIRTH
from .base_enrollment import BaseEnrollment
from .maternal_consent import MaternalConsent


class PostnatalEnrollment(BaseEnrollment):

    CONSENT_MODEL = MaternalConsent

    postpartum_days = models.IntegerField(
        verbose_name="How many days postpartum?",
        help_text="If more than 3days, not eligible")

    delivery_type = models.CharField(
        verbose_name="Was this a vaginal delivery?",
        choices=YES_NO,
        max_length=3,
        help_text="INELIGIBLE if NO")

    gestation_before_birth = models.IntegerField(
        verbose_name="How many weeks after gestation was the child born?",
        help_text="ineligible if premature or born before 37weeks")

    live_or_still_birth = models.CharField(
        verbose_name="Was this a live or still birth?",
        choices=LIVE_STILL_BIRTH,
        max_length=15,
        help_text='if still birth, not eligible')

    live_infants = models.IntegerField(
        verbose_name="How many live infants?",
        null=True,
        blank=True)

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_postnatalenrollment_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Postnatal Enrollment'
        verbose_name_plural = 'Postnatal Enrollment'
