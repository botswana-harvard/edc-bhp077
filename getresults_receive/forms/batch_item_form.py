from django import forms

from ..models import BatchItem


class BatchItemForm(forms.ModelForm):

    class Meta:
        model = BatchItem
        fields = '__all__'
