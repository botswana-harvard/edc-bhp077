from django.core.urlresolvers import reverse
from django.db import models

from .base_enrollment import BaseEnrollment
from .maternal_consent import MaternalConsent


class AntenatalEnrollment(BaseEnrollment):

    CONSENT_MODEL = MaternalConsent

    weeks_of_gestation = models.IntegerField(
        verbose_name="How many weeks pregnant?",
        null=True,
        blank=True,
        help_text=" (weeks of gestation). If >=32 weeks do rapid test", )

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_antenatalenrollment_change', args=(self.id,))

    def __unicode__(self):
        return "{0} {1}".format(self.registered_subject.subject_identifier,
                                self.registered_subject.first_name)

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
