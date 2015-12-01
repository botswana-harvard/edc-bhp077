from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import PostnatalCallLog, PostnatalCallLogEntry


class PostnatalCallLogForm (BaseModelForm):

    class Meta:
        model = PostnatalCallLog


class PostnatalCallLogEntryForm (BaseModelForm):

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = PostnatalCallLogEntry
