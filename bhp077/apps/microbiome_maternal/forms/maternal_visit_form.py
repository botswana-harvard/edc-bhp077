from django import forms

from ..models import MaternalVisit


class MaternalVisitForm (forms.ModelForm):

    class Meta:
        model = MaternalVisit
        fields = '__all__'
