from django import forms

from ..models import MaternalInfected


class MaternalInfectedForm(forms.ModelForm):

    class Meta:
        model = MaternalInfected
        fields = '__all__'
