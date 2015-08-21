from django.forms import ModelForm
from microbiome.models.microbiome_maternal import (MaternalLabourDel, MaternalLabDelClinic,
                                MaternalLabDelDx, MaternalLabDelDxT)


class MaternalLabourDelForm(ModelForm):

    class Meta:
        model = MaternalLabourDel
        fields = '__all__'


class MaternalLabDelClinicForm(ModelForm):

    class Meta:
        model = MaternalLabDelClinic
        fields = '__all__'


class MaternalLabDelDxForm(ModelForm):

    class Meta:
        model = MaternalLabDelDx
        fields = '__all__'


class MaternalLabDelDxTForm(ModelForm):

    class Meta:
        model = MaternalLabDelDxT
        fields = '__all__'
