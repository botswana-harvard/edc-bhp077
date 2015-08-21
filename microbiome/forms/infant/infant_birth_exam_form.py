from django.forms.models import ModelForm

from microbiome.models.microbiome_infant import InfantBirthExam


class InfantBirthExamForm(ModelForm):

    class Meta:
        model = InfantBirthExam
        model = '__all__'
