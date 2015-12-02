from django import forms

from edc_constants.constants import POS, YES, NO, NEG

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome_maternal.models import (PostnatalEnrollment, AntenatalEnrollment)

from .base_enrollment_form import BaseEnrollmentForm


class PostnatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):

        cleaned_data = super(PostnatalEnrollmentForm, self).clean()
        if cleaned_data.get('gestation_before_birth') > 45:
            raise forms.ValidationError('Gestational age of {} exceeds 45 weeks. Please correct.'
                                        .format(cleaned_data.get('gestation_before_birth')))
        if cleaned_data.get("live_or_still_birth") == LIVE:
            if not cleaned_data.get('live_infants'):
                raise forms.ValidationError("Live infants were born. How many?")
            if cleaned_data.get('live_infants', None) <= 0:
                raise forms.ValidationError("Live infants were born. Number cannot be zero or less")
        try:
            ant = AntenatalEnrollment.objects.get(
                registered_subject__subject_identifier=cleaned_data.get('registered_subject').subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            ant = None
        if ant:
            if ant.verbal_hiv_status == POS and ant.evidence_hiv_status == YES:
                if not cleaned_data.get('verbal_hiv_status') == POS or not cleaned_data.get('evidence_hiv_status') == YES:
                    raise forms.ValidationError("Antenatal Enrollment shows participant is {} and {} evidence ."
                                                " Please Correct {} and {} evidence".format(ant.verbal_hiv_status,
                                                                                            ant.evidence_hiv_status,
                                                                                            cleaned_data.get('verbal_hiv_status'),
                                                                                            cleaned_data.get('evidence_hiv_status')))
        if ant:
            if not ant.antenatal_eligible:
                raise forms.ValidationError(
                    "This mother is not eligible for postnatal enrollment. Failed antenatal enrollment.")
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = PostnatalEnrollment(**cleaned_data)

        self.validate_create_postnatal_enrollment(cleaned_data, ant, instance)
        self.validate_create_rapid_tests(cleaned_data, instance)

        return cleaned_data

    def validate_create_postnatal_enrollment(self, cleaned_data, ant, instance):
        if instance.maternal_eligibility_pregnant_yes():
            if not ant:
                raise forms.ValidationError("Participant is pregnant, please fill in antenatal instead.")

    def validate_create_rapid_tests(self, cleaned_data, instance):
        if instance.verbal_hiv_status == NEG:
            if instance.validate_rapid_test_required_or_not_required():
                if cleaned_data.get('process_rapid_test') == NO:
                    raise forms.ValidationError(
                        "Rapid test is required. You have tested {} weeks ago.".format(
                            instance.number_of_weeks_after_tests))

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
