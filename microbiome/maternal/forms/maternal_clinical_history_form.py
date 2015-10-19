from django.forms import ModelForm

from ..models import MaternalClinicalHistory


class MaternalClinicalHistoryForm(ModelForm):

    class Meta:
        model = MaternalClinicalHistory
        fields = '__all__'
