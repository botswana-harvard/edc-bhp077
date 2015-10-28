from django import forms

from ..models import PostnatalCallList


class PostnatalCallListForm (forms.ModelForm):

    class Meta:
        model = PostnatalCallList
