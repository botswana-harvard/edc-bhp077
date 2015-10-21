from base_maternal_model_form import BaseMaternalModelForm

from ..models import RapidTestResult


class RapidTestResultForm(BaseMaternalModelForm):

    class Meta:
        model = RapidTestResult
        fields = '__all__'
