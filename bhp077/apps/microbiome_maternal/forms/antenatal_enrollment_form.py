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
                raise forms.ValidationError("Antenatal enrollment Not required, it can not be done when postnatal enrollment has been done already.")
            except PostnatalEnrollment.DoesNotExist:
                pass
        return cleaned_data

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
