from django.forms import ModelForm

from ..models import MaternalMedicalHistory


class MaternalMedicalHistoryForm(ModelForm):

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'
