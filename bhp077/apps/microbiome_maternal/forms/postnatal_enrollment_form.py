from django import forms

from edc_constants.constants import POS, YES, NO, NEG

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome_maternal.models import (PostnatalEnrollment, AntenatalEnrollment)
from .base_enrollment_form import BaseEnrollmentForm


class MyBaseEnrollmentForm(BaseEnrollmentForm):
    pass


class PostnatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):

        cleaned_data = super(PostnatalEnrollmentForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = PostnatalEnrollment(**cleaned_data)
        try:
            ant = AntenatalEnrollment.objects.get(
                registered_subject__subject_identifier=cleaned_data.get('registered_subject').subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            ant = None
        self.validate_ante_eligibility(ant)
        self.validate_delivery()
        self.validate_hiv_status(ant)
        self.validate_create_postnatal_enrollment(ant, instance)
        self.validate_create_rapid_tests(instance)
        return cleaned_data

    def validate_ante_eligibility(self, ant):
        if ant:
            if not ant.antenatal_eligible:
                raise forms.ValidationError(
                    "This mother is not eligible for postnatal enrollment. Failed antenatal enrollment.")

    def validate_hiv_status(self, ant):
        cleaned_data = self.cleaned_data
        if ant:
            if ant.current_hiv_status == POS and ant.evidence_hiv_status == YES:
                if (cleaned_data.get('current_hiv_status') != POS or cleaned_data.get('evidence_hiv_status') != YES):
                    raise forms.ValidationError(
                        "Antenatal Enrollment shows participant is {} and {} evidence ."
                        " Please Correct {} and {} evidence".format(
                            ant.current_hiv_status,
                            ant.evidence_hiv_status,
                            cleaned_data.get('current_hiv_status'),
                            cleaned_data.get('evidence_hiv_status')))

    def validate_create_postnatal_enrollment(self, ant, instance):
        if instance.maternal_eligibility_pregnant_yes():
            if not ant:
                raise forms.ValidationError("Participant is pregnant, please fill in antenatal instead.")

    def validate_delivery(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('gestation_to_birth_wks') > 45:
            raise forms.ValidationError('Gestational age of {} exceeds 45 weeks. Please correct.'
                                        .format(cleaned_data.get('gestation_to_birth_wks')))
        if cleaned_data.get("delivery_status") == LIVE:
            if not cleaned_data.get('live_infants'):
                raise forms.ValidationError("Live infants were born. How many?")
            if cleaned_data.get('live_infants', None) <= 0:
                raise forms.ValidationError("Live infants were born. Number cannot be zero or less")

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
