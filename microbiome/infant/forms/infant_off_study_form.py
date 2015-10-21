from edc.subject.off_study.forms import BaseOffStudyForm

from ..models import InfantOffStudy


class InfantOffStudyForm(BaseOffStudyForm):

    class Meta:
        model = InfantOffStudy
        fields = '__all__'
