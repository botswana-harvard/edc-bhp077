from django import forms

from ..models import PostnatalCallLog, PostnatalCallLogEntry


class PostnatalCallLogForm (forms.BaseForm):

    class Meta:
        model = PostnatalCallLog


class PostnatalCallLogEntryForm (forms.BaseForm):

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = PostnatalCallLogEntry
