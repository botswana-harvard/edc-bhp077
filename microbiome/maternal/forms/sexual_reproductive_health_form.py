from django import forms

from ..models import SexualReproductiveHealth


class SexualReproductiveHealthForm(forms.ModelForm):

    class Meta:
        model = SexualReproductiveHealth
        fields = '__all__'
