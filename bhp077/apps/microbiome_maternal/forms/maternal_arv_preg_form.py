from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from edc_constants.constants import YES, NO

from ..models import MaternalArvPreg, MaternalArv


class MaternalArvPregForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPregForm, self).clean()
        if cleaned_data.get('is_interrupt') == YES and cleaned_data.get('interrupt') == 'N/A':
            raise forms.ValidationError('You indicated that ARVs were interrupted during pregnancy. '
                                        'Please provide a reason for interruption')
        if cleaned_data.get('is_interrupt') == NO and cleaned_data.get('interrupt') != 'N/A':
            raise forms.ValidationError('You indicated that ARVs were NOT interrupted during pregnancy. '
                                        'You cannot provide a reason. Please correct.')
        check_arvs = self.data.get('maternalarv_set-0-arv_code')
        if cleaned_data.get('took_arv') == 'Yes' and not check_arvs:
            raise forms.ValidationError(
                "You indicated that participant started ARV(s) during this pregnancy on 'Maternal ARV in This Preg'. "
                "Please list them or correct 'Maternal ARV in This Preg'.")
        # if no is indicated for any arv's started in Maternal ARV in This Preg then list must be provided
        if cleaned_data.get('took_arv') == 'No' and check_arvs:
            raise forms.ValidationError(
                "You indicated that ARV(s) were NOT started during this pregnancy on 'Maternal ARV in This Preg'."
                "You cannot provide a list or correct 'Maternal ARV in This Preg'.")

        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = MaternalArvPreg(**cleaned_data)
        self.validate_took_arv(cleaned_data, instance)

        return cleaned_data

    def validate_took_arv(self, cleaned_data, instance):
        if cleaned_data.get('took_arv') == NO:
            if instance.maternal_visit.postnatal_enrollment.valid_regimen_duration == YES:
                raise forms.ValidationError(
                    "You indicated that the participant has been on regimen for period of time. The answer should be (YES)"
                    "to question 3.(ARVs during pregnancy?).")

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvForm(BaseMaternalModelForm):
    def clean(self):
        return super(MaternalArvForm, self).clean()

    class Meta:
        model = MaternalArv
        fields = '__all__'
