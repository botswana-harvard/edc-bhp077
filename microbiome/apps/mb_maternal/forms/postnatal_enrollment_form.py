from django import forms

from edc_constants.constants import POS, YES

from microbiome.apps.mb.constants import LIVE

from ..models import MaternalEligibility, PostnatalEnrollment, AntenatalEnrollment

from .base_enrollment_form import BaseEnrollmentForm
from microbiome.apps.mb_maternal.models.maternal_visit import MaternalVisit


class MyBaseEnrollmentForm(BaseEnrollmentForm):
    pass


class PostnatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):

        cleaned_data = super(PostnatalEnrollmentForm, self).clean()
        self.number_of_infants_on_live_birth()
        self.complete_postnatal_enrollment_if_pregnant()
        self.raise_if_rapid_test_required()
        antenatal_enrollment = self.get_antenatal_enrollment(cleaned_data.get('registered_subject'))
        if antenatal_enrollment:
            self.previous_visit_complete()
            self.is_eligible_on_antenatal_enrollment(antenatal_enrollment.is_eligible)
            self.hiv_status_matches_antenatal_enrollment(
                antenatal_enrollment.current_hiv_status,
                antenatal_enrollment.evidence_hiv_status)
        return cleaned_data

    def previous_visit_complete(self):
        cleaned_data = self.cleaned_data
        try:
            MaternalVisit.objects.get(
                appointment__visit_definition__code='1000M',
                appointment__registered_subject=cleaned_data.get('registered_subject'))
        except MaternalVisit.DoesNotExist:
            raise forms.ValidationError(
                'Mother was enrolled antenatally. Visit 1000M must be completed before Postnatal Enrollment.')

    def clean_gestation_wks_delivered(self):
        """Confirms delivery happened within 45 weeks gestational age."""
        gestation_wks_delivered = self.cleaned_data['gestation_wks_delivered']
        if gestation_wks_delivered > 45:
            raise forms.ValidationError('Gestational age cannot be greater than 45 weeks')
        return gestation_wks_delivered

    def clean_live_infants(self):
        live_infants = self.cleaned_data['live_infants']
        if live_infants:
            if live_infants > 8:
                raise forms.ValidationError("Live infants cannot be greater than 8.")
        return live_infants

    def is_eligible_on_antenatal_enrollment(self, is_eligible):
        """Confirms that mother was eligible at Antenatal if the Antenatal Enrollment form was complete."""
        if not is_eligible:
            raise forms.ValidationError(
                "This mother is not eligible for postnatal enrollment. Failed antenatal enrollment.")

    def hiv_status_matches_antenatal_enrollment(self, current_hiv_status, evidence_hiv_status):
        cleaned_data = self.cleaned_data
        if current_hiv_status == POS and evidence_hiv_status == YES:
            if (cleaned_data.get('current_hiv_status') != POS or cleaned_data.get('evidence_hiv_status') != YES):
                raise forms.ValidationError(
                    "Antenatal Enrollment shows participant is {} and {} evidence ."
                    " Please Correct {} and {} evidence".format(
                        current_hiv_status,
                        evidence_hiv_status,
                        cleaned_data.get('current_hiv_status'),
                        cleaned_data.get('evidence_hiv_status')))

    def complete_postnatal_enrollment_if_pregnant(self):
        cleaned_data = self.cleaned_data
        try:
            MaternalEligibility.objects.get(
                registered_subject__subject_identifier=self.get_subject_identifier(cleaned_data),
                currently_pregnant=YES,
            )
            if not self.get_antenatal_enrollment(cleaned_data.get('registered_subject')):
                raise forms.ValidationError(
                    'According to the Maternal Eligibility form, the participant is pregnant. '
                    'Please fill in Antenatal Enrollment form instead.')
        except MaternalEligibility.DoesNotExist:
            pass

    def number_of_infants_on_live_birth(self):
        """Confirms live_infants greater than zero if delivery is a live birth."""
        cleaned_data = self.cleaned_data
        if cleaned_data.get("delivery_status") == LIVE:
            if not cleaned_data.get('live_infants'):
                raise forms.ValidationError("Live infants were born. How many?")
            elif cleaned_data.get('live_infants') <= 0:
                raise forms.ValidationError("Live infants were born. Number cannot be zero or less")

    def get_antenatal_enrollment(self, registered_subject):
        if not registered_subject:
            raise forms.ValidationError(
                'Cannot determine if the Antenatal Enrollment form is complete. '
                'Expected a registered subject. Got None.')
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(
                registered_subject=registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            antenatal_enrollment = None
        return antenatal_enrollment

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
