from django import forms

from edc_constants.constants import NOT_APPLICABLE

from ..models import AntenatalEnrollment

from .base_enrollment_form import BaseEnrollmentForm


class AntenatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        return cleaned_data

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
