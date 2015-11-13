from django import forms

from edc.base.form.forms import BaseModelForm

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

    class Meta:
        model = InfantBirth
        fields = '__all__'
