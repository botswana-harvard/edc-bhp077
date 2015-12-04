from django import forms

from ..models import AntenatalEnrollment, PostnatalEnrollment

from .base_enrollment_form import BaseEnrollmentForm
from edc_constants.constants import NEG, NO


class AntenatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        post_natal = None
        if not self.instance.id:
            registered_subject = cleaned_data.get('registered_subject')
            try:
                post_natal = PostnatalEnrollment.objects.get(registered_subject=registered_subject)
                raise forms.ValidationError(
                    "Antenatal enrollment is NOT REQUIRED. Postnatal Enrollment already completed")
            except PostnatalEnrollment.DoesNotExist:
                pass

        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = AntenatalEnrollment(**cleaned_data)
        self.validate_create_antenal_enrollment(instance, cleaned_data, post_natal)
        self.validate_create_rapid_tests(cleaned_data, instance)

        return cleaned_data

    def clean_rapid_test_date(self):
        rapid_test_date = self.cleaned_data['rapid_test_date']
        if rapid_test_date:
            try:
                initial = AntenatalEnrollment.objects.get(registered_subject=self.instance.registered_subject)
                if initial:
                    if rapid_test_date != initial.rapid_test_date:
                        raise forms.ValidationError('The rapid test result cannot be changed')
            except AntenatalEnrollment.DoesNotExist:
                pass
        return rapid_test_date

    def validate_create_antenal_enrollment(self, instance, cleaned_data, post_natal):
        if instance.maternal_eligibility_pregnant_currently_delivered_yes():
            if not post_natal:
                raise forms.ValidationError("Participant just delivered, fill postnatal instead.")

    def validate_create_rapid_tests(self, cleaned_data, instance):
        if instance.verbal_hiv_status == NEG:
            if instance.rapid_test_required:
                if cleaned_data.get('rapid_test_done') == NO:
                    raise forms.ValidationError(
                        "Rapid test is required. Participant tested >=32 weeks ago.")

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
