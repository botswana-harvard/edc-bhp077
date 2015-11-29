from datetime import date
from dateutil.relativedelta import relativedelta
from django import forms

from edc_constants.constants import YES

from base_maternal_model_form import BaseMaternalModelForm

from ..models import (MaternalLabourDel, MaternalLabDelMed,
                      MaternalLabDelClinic, MaternalLabDelDx,
                      MaternalLabDelDxT, PostnatalEnrollment)


class MaternalLabourDelForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalLabourDelForm, self).clean()
        if cleaned_data.get('live_infants_to_register') > 1:
            raise forms.ValidationError("For this study we can only register ONE infant")
        # Validate that number of live_infants_to_register cannot be 0 or less
        if cleaned_data.get('live_infants_to_register') <= 0:
            raise forms.ValidationError('Number of live infants to register may not be less than or equal to 0!.')
        if cleaned_data.get('delivery_datetime') > cleaned_data.get('report_datetime'):
                raise forms.ValidationError('Maternal Labour Delivery date cannot be greater than report date. '
                                            'Please correct.')
        postnatal = PostnatalEnrollment.objects.get(registered_subject__subject_identifier=cleaned_data.get('maternal_visit').appointment.registered_subject.subject_identifier)
        if postnatal:
            expected_delivery_date = cleaned_data.get('report_datetime').date() - relativedelta(days=postnatal.postpartum_days)
            if cleaned_data.get('delivery_datetime').date() != expected_delivery_date:
                raise forms.ValidationError('Delivery date is incorrect. Postpartum days is {} ago'.format(postnatal.postpartum_days))
        if cleaned_data.get('has_temp') == YES:
            if not cleaned_data.get('labr_max_temp'):
                raise forms.ValidationError('You have indicated that maximum temperature at delivery is known. '
                                            'Please provide the maximum temperature.')
        else:
            if cleaned_data.get('labr_max_temp'):
                raise forms.ValidationError('You have indicated that maximum temperature is not known. '
                                            'You CANNOT provide the maximum temperature')
        return cleaned_data

    class Meta:
        model = MaternalLabourDel
        fields = '__all__'


class MaternalLabDelMedForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalLabDelMedForm, self).clean()
        if 'health_cond' in cleaned_data.keys():
            self.validate_m2m(
                label='health condition',
                leading=cleaned_data.get('has_health_cond'),
                m2m=cleaned_data.get('health_cond'),
                other=cleaned_data.get('health_cond_other'))
        if 'ob_comp' in cleaned_data.keys():
            self.validate_m2m(
                label='obstetric complication',
                leading=cleaned_data.get('has_ob_comp'),
                m2m=cleaned_data.get('ob_comp'),
                other=cleaned_data.get('ob_comp_other'))
        if 'suppliments' in cleaned_data.keys():
            self.validate_m2m(
                label='pregnancy suppliment',
                leading=cleaned_data.get('took_suppliments'),
                m2m=cleaned_data.get('suppliments'))
        return cleaned_data

    class Meta:
        model = MaternalLabDelMed
        fields = '__all__'


class MaternalLabDelClinicForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalLabDelClinicForm, self).clean()
        # If CD4 performed, date and result should be supplied
        if cleaned_data.get('has_cd4') == YES:
            if not cleaned_data.get('cd4_date'):
                raise forms.ValidationError('You indicated that a CD4 count was performed. Please provide the date.')
            if not cleaned_data.get('cd4_result'):
                raise forms.ValidationError('You indicated that a CD4 count was performed. Please provide the result.')
        else:
            # If cd4 was not performed no date nor result should be provided
            if cleaned_data.get('cd4_date'):
                raise forms.ValidationError('You indicated that a CD4 count was NOT performed, yet provided a date '
                                            'CD4 was performed. Please correct.')
            if cleaned_data.get('cd4_result'):
                raise forms.ValidationError('You indicated that a CD4 count was NOT performed, yet provided a CD4 '
                                            'result. Please correct.')
        # If VL performed, date and result should be supplied
        if cleaned_data.get('has_vl') == YES:
            if not cleaned_data.get('vl_date'):
                raise forms.ValidationError('You indicated that a VL count was performed. Please provide the date.')
            if not cleaned_data.get('vl_result'):
                raise forms.ValidationError('You indicated that a VL count was performed. Please provide the result.')
        else:
            # If VL was not performed, no VL date nor result should be supplied
            if cleaned_data.get('vl_date'):
                raise forms.ValidationError('You indicated that a VL count was NOT performed, yet provided a date VL '
                                            'was performed. Please correct.')
            if cleaned_data.get('vl_result'):
                raise forms.ValidationError('You indicated that a VL count was NOT performed, yet provided a VL result'
                                            ' Please correct.')
        if cleaned_data.get('vl_detectable') == YES:
            if not cleaned_data.get('vl_result'):
                raise forms.ValidationError('You indicated that the VL was detectable. Provide provide VL result.')
        return cleaned_data

    class Meta:
        model = MaternalLabDelClinic
        fields = '__all__'


class MaternalLabDelDxForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalLabDelDxForm, self).clean()
        check_dx = self.data.get('maternallabdeldxt_set-0-lab_del_dx')

        # WHO validations
        if 'wcs_dx_adult' in cleaned_data.keys():
            self.validate_m2m_wcs_dx(
                label='who diagnoses',
                leading=cleaned_data.get('has_who_dx'),
                m2m=cleaned_data.get('wcs_dx_adult'))

        # Validate diagnosis
        if cleaned_data.get('has_preg_dx') == 'Yes' and not check_dx:
            raise forms.ValidationError('You indicated that participant had diagnosis. Please list them.')
        return cleaned_data

    class Meta:
        model = MaternalLabDelDx
        fields = '__all__'


class MaternalLabDelDxTForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalLabDelDxTForm, self).clean()
        maternal_lab_del_dx = cleaned_data.get('maternal_lab_del_dx')

        if maternal_lab_del_dx.has_preg_dx == 'No' and cleaned_data.get('lab_del_dx'):
            raise forms.ValidationError('You have indicated that the participant did NOT have diagnosis '
                                        'and yet provided them. Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalLabDelDxT
        fields = '__all__'
