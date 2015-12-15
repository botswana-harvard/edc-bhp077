from django.db import models

from edc.entry_meta_data.models import MetaDataMixin
from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.choices import YES_NO, ALIVE_DEAD_UNKNOWN
from edc_base.model.validators import date_not_before_study_start, date_not_future
from edc_constants.constants import OFF_STUDY, DEATH_VISIT, UNSCHEDULED, SCHEDULED
from edc_visit_tracking.constants import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from edc_visit_tracking.models import BaseVisitTracking
from edc_visit_tracking.models import PreviousVisitMixin

from microbiome.apps.mb_maternal.models import PostnatalEnrollment
from microbiome.apps.mb.choices import (
    VISIT_REASON, INFO_PROVIDER, INFANT_VISIT_STUDY_STATUS)

from .infant_off_study_mixin import InfantOffStudyMixin
from edc.subject.visit_tracking.managers.base_visit_tracking_manager import BaseVisitTrackingManager


class InfantVisit(MetaDataMixin, PreviousVisitMixin, InfantOffStudyMixin, BaseVisitTracking, BaseUuidModel):

    """ A model completed by the user on the infant visits. """

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

    is_present = models.CharField(
        max_length=10,
        verbose_name="Is the infant present at today\'s visit",
        choices=YES_NO)

    study_status = models.CharField(
        verbose_name="What is the infant's current study status",
        max_length=50,
        choices=INFANT_VISIT_STUDY_STATUS)

    survival_status = models.CharField(
        max_length=10,
        verbose_name="Infant survival status",
        choices=ALIVE_DEAD_UNKNOWN,
        null=True,
        blank=False)

    last_alive_date = models.DateField(
        verbose_name="Date infant last known alive",
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True)

    history = AuditTrail()

    objects = BaseVisitTrackingManager()

    def __unicode__(self):
        return '{} {} {}'.format(
            self.appointment.registered_subject.subject_identifier,
            self.appointment.registered_subject.first_name,
            self.appointment.visit_definition.code)

#     def save(self, *args, **kwargs):
#         self.reason = OFF_STUDY if not self.postnatal_enrollment.is_eligible else self.reason
#         super(InfantVisit, self).save(*args, **kwargs)

    @property
    def postnatal_enrollment(self):
        """Returns the mother's postnatal enrollment instance."""
        maternal_registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.appointment.registered_subject.relative_identifier)
        return PostnatalEnrollment.objects.get(registered_subject=maternal_registered_subject)

    def custom_post_update_entry_meta_data(self):
        """Calls custom methods that manipulate meta data on the post save.

        This method is called in a post-save signal in edc.entry_meta_data."""

        if self.reason == OFF_STUDY:
            self.change_to_off_study_visit(self.appointment, 'mb_infant
', 'infantoffstudy')
        elif self.reason == DEATH_VISIT:
            self.change_to_death_visit(
                self.appointment, 'mb_infant
', 'infantoffstudy', 'infantdeath')
        elif self.reason == UNSCHEDULED:
            self.change_to_unscheduled_visit(self.appointment)
        elif self.reason == SCHEDULED:
            self.postnatal_enrollment.enrollment_hiv_status
            self.requires_infant_birth_arv_on_maternal_pos()
            self.requires_dna_pcr_on_maternal_pos()

    def requires_infant_birth_arv_on_maternal_pos(self):
        if self.appointment.visit_definition.code == '2000':
            self.form_is_required(
                self.appointment,
                'mb_infant
',
                'infantbirtharv',
                message=self.appointment.visit_definition.code)

    def requires_dna_pcr_on_maternal_pos(self):
        if self.appointment.visit_definition.code in ['2010', '2030', '2060', '2090', '2120']:
            self.requisition_is_required(
                self.appointment,
                'mb_lab
',
                'infantrequisition',
                'DNA PCR',
                message=self.appointment.visit_definition.code,
            )

    def natural_key(self):
        return self.get_appointment().natural_key()
    natural_key.dependencies = ['appointment.appointment', ]

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def get_visit_reason_no_follow_up_choices(self):
        """Returns the visit reasons that do not imply any data collection; that is, the subject is not available."""
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        del dct[DEATH_VISIT]
        return dct

    class Meta:
        app_label = "mb_infant
"
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
