from ..models import InfantBirth

from edc.base.form.forms import BaseModelForm


class InfantBirthForm(BaseModelForm):

    class Meta:
        model = InfantBirth
        fields = '__all__'
