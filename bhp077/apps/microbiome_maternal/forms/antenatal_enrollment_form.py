from django import forms

from edc_constants.constants import NOT_APPLICABLE

from ..models import AntenatalEnrollment

from .base_enrollment_form import BaseEnrollmentForm


class AntenatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        # If weeks of gestation are greater than 32 weeks, do a rapid test
        if cleaned_data.get('weeks_of_gestation') >= 32:
            if cleaned_data.get('process_rapid_test') == NOT_APPLICABLE:
                raise forms.ValidationError('Weeks of gestation are greater or equal to 32. Rapid test processing '
                                            'CANNOT be Not Applicable (Rapid test is expected). Please correct.')
        return cleaned_data

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
