from django import forms

from ..models import PostnatalEnrollment
from bhp077.apps.microbiome.constants import LIVE

from .base_enrollment_form import BaseEnrollmentForm


class PostnatalEnrollmentForm(BaseEnrollmentForm):

    def clean(self):

        cleaned_data = super(PostnatalEnrollmentForm, self).clean()
        if cleaned_data.get("live_or_still_birth") == LIVE:
            if not cleaned_data.get('live_infants'):
                raise forms.ValidationError("Live infants were born. How many?")
            if cleaned_data.get('live_infants', None) <= 0:
                raise forms.ValidationError("Live infants were born. Number cannot be zero or less")
        return cleaned_data

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
