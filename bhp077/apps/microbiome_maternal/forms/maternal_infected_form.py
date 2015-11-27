from django import forms

from edc_constants.constants import NOT_APPLICABLE

from ..models import MaternalInfected, MaternalObstericalHistory

from base_maternal_model_form import BaseMaternalModelForm


class MaternalInfectedForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalInfectedForm, self).clean()
        self.validate_prev_preg(cleaned_data)
        return cleaned_data

    def validate_prev_preg(self, cleaned_data):
        ob_history = MaternalObstericalHistory.objects.filter(
            maternal_visit__appointment__registered_subject=cleaned_data.get('maternal_visit').appointment.registered_subject)
        if not ob_history:
            raise forms.ValidationError('Please fill in the Maternal Obsterical History form first.')
        else:
            if ob_history[0].prev_pregnancies == 0:
                if cleaned_data.get('prev_pregnancy_arv') != NOT_APPLICABLE:
                    raise forms.ValidationError('In Maternal Obsterical History form you indicated there were no previous '
                                                'pregnancies. ARVs for PMTCT purposes during previous pregnancy should be '
                                                'NOT APPLICABLE')

    class Meta:
        model = MaternalInfected
        fields = '__all__'
