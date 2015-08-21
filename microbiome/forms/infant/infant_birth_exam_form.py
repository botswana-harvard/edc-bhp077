from django.forms.models import ModelForm

from ...models.infant import InfantBirthExam


class InfantBirthExamForm(ModelForm):

    class Meta:
        model = InfantBirthExam
        model = '__all__'
