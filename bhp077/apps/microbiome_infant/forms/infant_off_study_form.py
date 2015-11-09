from ..forms import BaseInfantModelForm

from ..models import InfantOffStudy


class InfantOffStudyForm(BaseInfantModelForm):

    class Meta:
        model = InfantOffStudy
        fields = '__all__'
