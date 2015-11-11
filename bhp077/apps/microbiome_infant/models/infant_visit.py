from django.core.urlresolvers import reverse
from django.db import models

from edc.subject.visit_tracking.models import BaseVisitTracking

from edc_base.model.models.base_uuid_model import BaseUuidModel

from bhp077.apps.microbiome.choices import (VISIT_REASON, INFO_PROVIDER, INFANT_VISIT_STUDY_STATUS,
                                            ALIVE_DEAD_UNKNOWN)
from .infant_off_study_mixin import InfantOffStudyMixin


class InfantVisit(InfantOffStudyMixin, BaseVisitTracking, BaseUuidModel):

    information_provider = models.CharField(
        verbose_name="Please indicate who provided most of the information for this child's visit",
        choices=INFO_PROVIDER,
        max_length=20,
        help_text="")

    information_provider_other = models.CharField(
        verbose_name="if information provider is Other, please specify",
        max_length=20,
        help_text="",
        blank=True,
        null=True)

    study_status = models.CharField(
        verbose_name="What is the participant's current study status",
        max_length=50,
        choices=INFANT_VISIT_STUDY_STATUS)

    survival_status = models.CharField(
        max_length=10,
        verbose_name="Survival status",
        choices=ALIVE_DEAD_UNKNOWN,
        null=True,
        blank=False)

    date_last_alive = models.DateField(
        verbose_name="Date last known alive",
        help_text="",
        null=True,
        blank=True)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_infantvisit_add', args=(self.id,))

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
