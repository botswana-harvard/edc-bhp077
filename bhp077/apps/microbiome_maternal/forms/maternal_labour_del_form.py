from django import forms
from base_maternal_model_form import BaseMaternalModelForm
from ..models import (MaternalLabourDel, MaternalLabDelMed,
                      MaternalLabDelClinic, MaternalLabDelDx,
                      MaternalLabDelDxT)


class MaternalLabourDelForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('live_infants_to_register') > 1:
            raise forms.ValidationError("For this study we can only register ONE infant")
        return super(MaternalLabourDelForm, self).clean()

    class Meta:
        model = MaternalLabourDel
        fields = '__all__'


class MaternalLabDelMedForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalLabDelMed
        fields = '__all__'


class MaternalLabDelClinicForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalLabDelClinic
        fields = '__all__'


class MaternalLabDelDxForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalLabDelDx
        fields = '__all__'


class MaternalLabDelDxTForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalLabDelDxT
        fields = '__all__'
