from django import forms
from django.utils import timezone

from base_maternal_model_form import BaseMaternalModelForm

from edc_constants.constants import YES, NO, NOT_APPLICABLE
from bhp077.apps.microbiome.utils import weeks_between

from ..models import MaternalArvPreg, MaternalArv, MaternalArvHistory


class MaternalArvPregForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvPregForm, self).clean()
        if cleaned_data.get('is_interrupt') == YES and cleaned_data.get('interrupt') == NOT_APPLICABLE:
            raise forms.ValidationError('You indicated that ARVs were interrupted during pregnancy. '
                                        'Please provide a reason for interruption')
        if cleaned_data.get('is_interrupt') == NO and cleaned_data.get('interrupt') != NOT_APPLICABLE:
            raise forms.ValidationError('You indicated that ARVs were NOT interrupted during pregnancy. '
                                        'You cannot provide a reason. Please correct.')
        check_arvs = self.data.get('maternalarv_set-0-arv_code')
        if cleaned_data.get('took_arv') == YES and not check_arvs:
            raise forms.ValidationError(
                "You indicated that participant started ARV(s) during this "
                "pregnancy on 'Maternal ARV in This Preg'. "
                "Please list them or correct 'Maternal ARV in This Preg'.")
        # if no is indicated for any arv's started in Maternal ARV in This Preg then list must be provided
        if cleaned_data.get('took_arv') == NO and check_arvs:
            raise forms.ValidationError(
                "You indicated that ARV(s) were NOT started during this pregnancy on 'Maternal ARV in This Preg'."
                "You cannot provide a list or correct 'Maternal ARV in This Preg'.")

        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = MaternalArvPreg(**cleaned_data)
        self.validate_arv_exposed(cleaned_data, instance)

        return cleaned_data

    def validate_arv_exposed(self, cleaned_data, instance):
        if cleaned_data.get('took_arv') == NO:
            if instance.maternal_visit.postnatal_enrollment.valid_regimen_duration == YES:
                raise forms.ValidationError(
                    "You indicated that the participant has been on regimen "
                    "for period of time. But now you indicated that the participant did not take ARVs.")

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalArvForm, self).clean()
        if weeks_between(cleaned_data.get('start_date'), timezone.now()) < 6:
            raise forms.ValidationError("ARV start date must be six weeks prior to today's date or greater.")
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('start_date'):
                raise forms.ValidationError(
                    'You have indicated that the stop date of {} is prior to start date of {}. '
                    'Please correct'.format(cleaned_data.get('stop_date'), cleaned_data.get('start_date')))
        return cleaned_data

    def validate_arv_start_dates(self):
        """Confirms that the Historical ARV start date is not less than the ARV start date
            in this pregnancy"""
        cleaned_data = self.cleaned_data
        try:
            maternal_visit = cleaned_data.get('maternal_visit')
            history_arv = MaternalArvHistory.objects.get(maternal_visit=maternal_visit)
            if cleaned_data.get('start_date') < history_arv.haart_start_date:
                raise forms.ValidationError(
                    "Your ARV start date {} is before your Historical ARV date {}".format(
                        cleaned_data.get('start_date'), history_arv.haart_start_date))
        except MaternalArvHistory.DoesNotExist:
            pass

    class Meta:
        model = MaternalArv
        fields = '__all__'
