from django import forms

from ..models import AntenatalEnrollment, PostnatalEnrollment

from .base_enrollment_form import BaseEnrollmentForm


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
        self.validate_create_antenal_enrollment(cleaned_data, post_natal)
        try:
            initial = AntenatalEnrollment.objects.get(registered_subject=self.instance.registered_subject)
            if initial:
                if cleaned_data.get('date_of_rapid_test') != initial.date_of_rapid_test:
                    raise forms.ValidationError('The rapid test result cannot be changed')
        except AntenatalEnrollment.DoesNotExist:
            pass

        return cleaned_data

    def validate_create_antenal_enrollment(self, cleaned_data, post_natal):
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = AntenatalEnrollment(**cleaned_data)
        if instance.maternal_eligibility_pregnant_currently_delivered_yes():
            if not post_natal:
                raise forms.ValidationError("Participant just delivered, fill postnatal instead.")

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
