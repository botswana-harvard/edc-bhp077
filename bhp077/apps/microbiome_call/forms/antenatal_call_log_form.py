from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import AntenatalCallLog, AntenatalCallLogEntry


class AntenatalCallLogForm (BaseModelForm):

    class Meta:
        model = AntenatalCallLog


class AntenatalCallLogEntryForm (BaseModelForm):

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = AntenatalCallLogEntry
