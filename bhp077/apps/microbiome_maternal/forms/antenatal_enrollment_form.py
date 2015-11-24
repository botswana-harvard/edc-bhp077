from django import forms

from ..models import AntenatalEnrollment, PostnatalEnrollment

from .base_enrollment_form import BaseEnrollmentForm


class AntenatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        if not self.instance.id:
            registered_subject = cleaned_data.get('registered_subject')
            try:
                PostnatalEnrollment.objects.get(registered_subject=registered_subject)
                raise forms.ValidationError("Antenatal enrollment is NOT REQUIRED. Postnatal Enrollment already completed")
            except PostnatalEnrollment.DoesNotExist:
                pass

        try:
            initial = AntenatalEnrollment.objects.get(registered_subject=self.instance.registered_subject)
            if initial:
                if cleaned_data.get('date_of_rapid_test') != initial.date_of_rapid_test:
                    raise forms.ValidationError('The rapid test result cannot be changed')
        except AntenatalEnrollment.DoesNotExist:
            pass

        return cleaned_data

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
