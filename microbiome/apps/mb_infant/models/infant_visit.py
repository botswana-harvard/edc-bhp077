from django.db.models import get_model

from edc_meta_data.models import CrfMetaDataMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_constants.constants import UNSCHEDULED, SCHEDULED, COMPLETED_PROTOCOL_VISIT, DEAD, POS
from edc_offstudy.models import OffStudyMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.constants import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from edc_visit_tracking.models import PreviousVisitMixin
from edc_visit_tracking.models import VisitModelMixin

from microbiome.apps.mb_maternal.models import PostnatalEnrollment
from microbiome.apps.mb.choices import VISIT_REASON
from edc_visit_tracking.models.caretaker_fields_mixin import CaretakerFieldsMixin


class InfantVisit(
        CrfMetaDataMixin, SyncModelMixin, PreviousVisitMixin, OffStudyMixin, VisitModelMixin,
        CaretakerFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the infant visits. """

    off_study_model = ('mb_infant', 'InfantOffStudy')

    death_report_model = ('mb_infant', 'InfantDeathReport')

    history = AuditTrail()

    def __unicode__(self):
        return '{} {} {}'.format(
            self.appointment.registered_subject.subject_identifier,
            self.appointment.registered_subject.first_name,
            self.appointment.visit_definition.code)

    @property
    def postnatal_enrollment(self):
        """Returns the mother's postnatal enrollment instance."""
        maternal_registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.appointment.registered_subject.relative_identifier)
        return PostnatalEnrollment.objects.get(registered_subject=maternal_registered_subject)

    def custom_post_update_crf_meta_data(self):
        """Calls custom methods that manipulate meta data on the post save.

        This method is called in a post-save signal in edc_meta_data."""
        if self.survival_status == DEAD:
            self.require_death_report()
        elif self.reason == COMPLETED_PROTOCOL_VISIT:
            self.require_off_study_report()
        elif self.reason == UNSCHEDULED:
            self.change_to_unscheduled_visit(self.appointment)
        elif self.reason == SCHEDULED:
            if self.postnatal_enrollment.enrollment_hiv_status:
                self.requires_infant_birth_arv_on_maternal_pos()
                self.requires_dna_pcr_on_maternal_pos()
        return self

    def requires_infant_birth_arv_on_maternal_pos(self):
        PostnatalEnrollment = get_model('mb_maternal', 'PostnatalEnrollment')
        maternal_registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.appointment.registered_subject.relative_identifier)
        postnatal_enrollment = PostnatalEnrollment.objects.get(
            registered_subject=maternal_registered_subject)
        if postnatal_enrollment.enrollment_hiv_status == POS:
            if self.appointment.visit_definition.code == '2000':
                self.crf_is_required(self.appointment, 'mb_infant', 'infantbirtharv')

    def requires_dna_pcr_on_maternal_pos(self):
        if self.appointment.visit_definition.code in ['2000', '2010', '2030', '2060', '2090', '2120']:
            self.requisition_is_required(self.appointment, 'mb_lab', 'infantrequisition', 'DNA PCR')

    def natural_key(self):
        return (self.report_datetime,) + self.appointment.natural_key()
    natural_key.dependencies = ['edc_appointment.appointment']

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def get_visit_reason_no_follow_up_choices(self):
        """Returns the visit reasons that do not imply any data collection;
        that is, the subject is not available."""
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        return dct

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
