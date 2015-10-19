from django.forms import ModelForm

from ..models import RapidTestResult


class RapidTestResultForm(ModelForm):

    class Meta:
        model = RapidTestResult
        fields = '__all__'
