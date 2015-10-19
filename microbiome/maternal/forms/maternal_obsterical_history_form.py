from django.forms import ModelForm

from ..models import MaternalObstericalHistory


class MaternalObstericalHistoryForm(ModelForm):

    class Meta:
        model = MaternalObstericalHistory
        fields = '__all__'
