from django import forms

from edc_constants.constants import POS, YES

from .base_enrollment_form import BaseEnrollmentForm
from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment, AntenatalEnrollment


class PostnatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):

        cleaned_data = super(PostnatalEnrollmentForm, self).clean()
        if cleaned_data.get("live_or_still_birth") == LIVE:
            if not cleaned_data.get('live_infants'):
                raise forms.ValidationError("Live infants were born. How many?")
            if cleaned_data.get('live_infants', None) <= 0:
                raise forms.ValidationError("Live infants were born. Number cannot be zero or less")
        ant = AntenatalEnrollment.objects.filter(registered_subject__subject_identifier=cleaned_data.get('registered_subject').subject_identifier)
        if ant:
            if ant[0].verbal_hiv_status == POS and ant[0].evidence_hiv_status == YES:
                if not cleaned_data.get('verbal_hiv_status') == POS or not cleaned_data.get('evidence_hiv_status') == YES:
                    raise forms.ValidationError("Antenatal Enrollment shows participant is {} and {} evidence ."
                                                " Please Correct {} and {} evidence".format(ant[0].verbal_hiv_status,
                                                                                            ant[0].evidence_hiv_status,
                                                                                            cleaned_data.get('verbal_hiv_status'),
                                                                                            cleaned_data.get('evidence_hiv_status')))
        return cleaned_data

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
