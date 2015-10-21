from django import forms

from ..models import AntenatalCallLog, AntenatalCallLogEntry


class AntenatalCallLogForm (forms.BaseForm):

    class Meta:
        model = AntenatalCallLog


class AntenatalCallLogEntryForm (forms.BaseForm):

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = AntenatalCallLogEntry
