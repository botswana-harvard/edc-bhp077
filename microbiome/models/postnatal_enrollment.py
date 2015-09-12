from django.core.urlresolvers import reverse
from django.db import models

from .base_enrollment import BaseEnrollment
from ..choices import LIVE_STILL_BIRTH
from edc_constants.choices import YES_NO


class PostnatalEnrollment(BaseEnrollment):

    postpartum_days = models.IntegerField(
        verbose_name="How days postpartum?",
        help_text="If more than 3days, not eligible")

    delivery_type = models.CharField(
        verbose_name="Was this a vaginal delivery?",
        choices=YES_NO,
        max_length=3,
        help_text="INELIGIBLE if NO")

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
        return reverse('admin:microbiome_postnatalenrollment_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome'
        verbose_name = 'Postnatal Enrollment'
        verbose_name_plural = 'Postnatal Enrollment'
