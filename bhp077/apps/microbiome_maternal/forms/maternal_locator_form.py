from edc_locator.forms import LocatorFormMixin

from .base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalLocator


class MaternalLocatorForm(LocatorFormMixin, BaseMaternalModelForm):

    class Meta:
        model = MaternalLocator
        fields = '__all__'
