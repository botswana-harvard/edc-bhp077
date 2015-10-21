from django import forms

from ..models import AntenatalCallList


class AntenatalCallListForm (forms.ModelForm):

    class Meta:
        model = AntenatalCallList
