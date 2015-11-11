from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import PostnatalEnrollment
from bhp077.apps.microbiome.constants import LIVE


class PostnatalEnrollmentForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        if cleaned_data.get("live_or_still_birth") == LIVE:
            if not cleaned_data.get('live_infants'):
                raise forms.ValidationError("Live infants were born. How many?")
            if cleaned_data.get('live_infants', None) <= 0:
                raise forms.ValidationError("Live infants were born. Number cannot be zero or less")
        return super(PostnatalEnrollmentForm, self).clean()

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
