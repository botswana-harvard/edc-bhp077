from django import forms

from edc_constants.constants import YES

from ..models import AntenatalEnrollment, PostnatalEnrollment, MaternalEligibility

from .base_enrollment_form import BaseEnrollmentForm


class AntenatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):
        cleaned_data = super(AntenatalEnrollmentForm, self).clean()
        registered_subject = cleaned_data.get('registered_subject')
        if not registered_subject:
            raise forms.ValidationError('Expected a registered subject. Got None.')
        if not self.instance.id:
            registered_subject = cleaned_data.get('registered_subject')
            try:
                PostnatalEnrollment.objects.get(registered_subject=registered_subject)
                raise forms.ValidationError(
                    "Antenatal enrollment is NOT REQUIRED. Postnatal Enrollment already completed")
            except PostnatalEnrollment.DoesNotExist:
                pass
        self.fill_postnatal_enrollment_if_recently_delivered()
        self.raise_if_rapid_test_required()

        return cleaned_data

    def clean_rapid_test_date(self):
        rapid_test_date = self.cleaned_data['rapid_test_date']
        if rapid_test_date:
            try:
                initial = AntenatalEnrollment.objects.get(
                    registered_subject=self.instance.registered_subject)
                if initial:
                    if rapid_test_date != initial.rapid_test_date:
                        raise forms.ValidationError('The rapid test result cannot be changed')
            except AntenatalEnrollment.DoesNotExist:
                pass
        return rapid_test_date

    def fill_postnatal_enrollment_if_recently_delivered(self):
        cleaned_data = self.cleaned_data
        registered_subject = cleaned_data.get('registered_subject')
        try:
            MaternalEligibility.objects.get(
                registered_subject=registered_subject,
                recently_delivered=YES)
            if not self.get_postnatal_enrollment():
                raise forms.ValidationError(
                    'According to the Maternal Eligibility form the participant has just delivered. '
                    'Please fill the Postnatal Enrollment form instead.')
        except MaternalEligibility.DoesNotExist:
            pass

    def get_postnatal_enrollment(self):
        cleaned_data = self.cleaned_data
        registered_subject = cleaned_data.get('registered_subject')
        try:
            postnatal_enrollment = PostnatalEnrollment.objects.get(
                registered_subject=registered_subject)
        except PostnatalEnrollment.DoesNotExist:
            postnatal_enrollment = None
        return postnatal_enrollment

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
