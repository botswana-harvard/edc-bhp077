from django.forms.models import ModelForm

from ...models.infant import InfantOffStudy


class InfantOffStudyForm(ModelForm):

    class Meta:
        model = InfantOffStudy
        fields = '__all__'
