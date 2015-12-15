from django import forms

from edc_constants.constants import YES, NOT_APPLICABLE
from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalClinicalHistory
from bhp077.apps.microbiome_maternal.models.maternal_obsterical_history import MaternalObstericalHistory


class MaternalClinicalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_prev_preg(cleaned_data)
        if cleaned_data.get('lowest_cd4_known') == YES:
            if not cleaned_data.get('cd4_count'):
                raise forms.ValidationError("If CD4 lowest count is known, what is the count?")
            if not cleaned_data.get('cd4_date'):
                raise forms.ValidationError("CD4 count is known please provide the date")
            if cleaned_data.get('cd4_date'):
                if not cleaned_data.get('is_date_estimated'):
                    raise forms.ValidationError('You have provided the CD4 date, is this estimated?')
        else:
            if cleaned_data.get('cd4_count'):
                raise forms.ValidationError("CD4 is NOT KNOWN. Do not give the count")
            if cleaned_data.get('cd4_date'):
                raise forms.ValidationError("CD4 is NOT KNOWN. Do not give the date")
            if cleaned_data.get('is_date_estimated'):
                raise forms.ValidationError("CD4 is NOT KNOWN. Do not give the date-estimated")
        return super(MaternalClinicalHistoryForm, self).clean()

    def validate_prev_preg(self, cleaned_data):
        ob_history = MaternalObstericalHistory.objects.filter(
            maternal_visit__appointment__registered_subject=cleaned_data.get(
                'maternal_visit').appointment.registered_subject)
        if not ob_history:
            raise forms.ValidationError('Please fill in the Maternal Obsterical History form first.')
        else:
            if ob_history[0].prev_pregnancies == 0:
                if cleaned_data.get('prev_preg_azt') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. Receive AZT monotherapy in previous pregancy should be '
                        'NOT APPLICABLE')
                if cleaned_data.get('prev_sdnvp_labour') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. Single sd-NVP in labour during a prev pregnancy should '
                        'be NOT APPLICABLE')
                if cleaned_data.get('prev_preg_haart') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'In Maternal Obsterical History form you indicated there were no previous '
                        'pregnancies. triple ARVs during a prev pregnancy should '
                        'be NOT APPLICABLE')

    class Meta:
        model = MaternalClinicalHistory
        fields = '__all__'
