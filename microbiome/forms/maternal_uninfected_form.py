from django import forms

from ..models import MaternalUninfected


class MaternalUninfectedForm(forms.ModelForm):
    
    class Meta:
        model = MaternalUninfected
        fields = '__all__'
