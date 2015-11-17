from ..forms import BaseInfantModelForm

from ..models import InfantOffStudy


class InfantOffStudyForm(BaseInfantModelForm):

    class Meta:
        model = InfantOffStudy
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantVisitForm, self).clean()
        self.validate_azt_after_birth(cleaned_data)
        self.validate_sdnvp_after_birth(cleaned_data)
        self.validate_nvp_discharge_supply(cleaned_data)

    def validate_offstudy_date(self, cleaned_data):
        pass
