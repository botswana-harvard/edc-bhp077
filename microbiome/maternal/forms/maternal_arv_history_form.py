from django.forms.models import ModelForm

from ..models import MaternalArvHistory


class MaternalArvHistoryForm(ModelForm):

    class Meta:
        model = MaternalArvHistory
        fields = '__all__'
