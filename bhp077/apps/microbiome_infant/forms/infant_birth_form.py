from django import forms

from edc_constants.constants import YES

from bhp077.apps.microbiome.base_model_form import BaseModelForm
from bhp077.apps.microbiome_maternal.models import MaternalLabourDel

from ..models import InfantBirth


class InfantBirthForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(InfantBirthForm, self).clean()
        # DOB should match delivery date
        maternal_identifier = cleaned_data.get('registered_subject', None).relative_identifier
        try:
            maternal_lab_del = MaternalLabourDel.objects.get(
                maternal_visit__appointment__registered_subject__subject_identifier=maternal_identifier)
            if not cleaned_data.get('dob', None) == maternal_lab_del.delivery_datetime.date():
                raise forms.ValidationError('Infant dob must match maternal delivery date of {}. You wrote {}'
                                            .format(maternal_lab_del.delivery_datetime.date(),
                                                    cleaned_data.get('dob', None)))
        except MaternalLabourDel.DoesNotExist:
            raise forms.ValidationError('Cannot find maternal labour and delivery form for this infant!'
                                        ' This is not expected.')
        return cleaned_data

    def validate_apgar(self, cleaned_data):
        if cleaned_data.get('apgar_score') == YES:
            if not cleaned_data.get('apgar_score_min_1'):
                raise forms.ValidationError('APGAR score is indicated to have been performed. '
                                            'Please specify score at 1 min.')
            if not cleaned_data.get('apgar_score_min_5'):
                raise forms.ValidationError('APGAR score is indicated to have been performed. '
                                            'Please specify score at 5 min.')
        else:
            if cleaned_data.get('apgar_score_min_1'):
                raise forms.ValidationError('You have indicated that APGAR was not performed. '
                                            'You CANNOT provide score at 1 min')
            if cleaned_data.get('apgar_score_min_5'):
                raise forms.ValidationError('You have indicated that APGAR was not performed. '
                                            'You CANNOT provide score at 5 min')
            if cleaned_data.get('apgar_score_min_1'):
                raise forms.ValidationError('You have indicated that APGAR was not performed. '
                                            'You CANNOT provide score at 10 min')

    class Meta:
        model = InfantBirth
        fields = '__all__'
