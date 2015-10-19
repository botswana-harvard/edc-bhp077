from django.forms.models import ModelForm

from ..models import InfantBirthExam


class InfantBirthExamForm(ModelForm):

    class Meta:
        model = InfantBirthExam
        fields = '__all__'
