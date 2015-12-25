from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline

from ..forms import (MaternalLabourDelForm, MaternalLabDelMedForm,
                     MaternalLabDelClinicForm, MaternalLabDelDxForm, MaternalLabDelDxTForm)
from ..models import (MaternalLabourDel, MaternalLabDelMed, MaternalLabDelClinic,
                      MaternalLabDelDx, MaternalLabDelDxT, MaternalVisit)

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalLabourDelAdmin(BaseMaternalModelAdmin):

    form = MaternalLabourDelForm

    list_display = ('delivery_datetime',
                    'labour_hrs',
                    'delivery_hospital',
                    'live_infants_to_register')
    radio_fields = {'delivery_time_estimated': admin.VERTICAL,
                    'has_uterine_tender': admin.VERTICAL,
                    'has_chorioamnionitis': admin.VERTICAL,
                    'delivery_hospital': admin.VERTICAL,
                    'delivery_complications': admin.VERTICAL,
                    'has_temp': admin.VERTICAL, }

admin.site.register(MaternalLabourDel, MaternalLabourDelAdmin)


class MaternalLabDelMedAdmin(BaseMaternalModelAdmin):

    form = MaternalLabDelMedForm

    list_display = ('has_health_cond', 'has_ob_comp')

    radio_fields = {'has_health_cond': admin.VERTICAL,
                    'has_ob_comp': admin.VERTICAL,
                    'took_supplements': admin.VERTICAL}

    filter_horizontal = ('supplements', 'health_cond', 'ob_comp')

admin.site.register(MaternalLabDelMed, MaternalLabDelMedAdmin)


class MaternalLabDelClinicAdmin(BaseMaternalModelAdmin):

    form = MaternalLabDelClinicForm

    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'vl_detectable': admin.VERTICAL}

admin.site.register(MaternalLabDelClinic, MaternalLabDelClinicAdmin)


class MaternalLabDelDxTInlineAdmin(BaseTabularInline):
    model = MaternalLabDelDxT
    form = MaternalLabDelDxTForm
    extra = 1


class MaternalLabDelDxAdmin(BaseMaternalModelAdmin):

    form = MaternalLabDelDxForm

    radio_fields = {'has_preg_dx': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('who',)

    inlines = [MaternalLabDelDxTInlineAdmin, ]

admin.site.register(MaternalLabDelDx, MaternalLabDelDxAdmin)


class MaternalLabDelDxTAdmin(BaseMaternalModelAdmin):

    form = MaternalLabDelDxTForm

    radio_fields = {
        'lab_del_dx': admin.VERTICAL,
        'hospitalized': admin.VERTICAL}
    radio_fields = {'hospitalized': admin.VERTICAL}

admin.site.register(MaternalLabDelDxT, MaternalLabDelDxTAdmin)
