from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from .site import admin_site
from ..models import (MaternalLabourDel, MaternalLabDelMed, MaternalLabDelClinic,
                      MaternalLabDelDx, MaternalLabDelDxT)
from ..forms import (MaternalLabourDelForm, MaternalLabDelMedForm, MaternalLabDelMedForm,
                     MaternalLabDelClinicForm, MaternalLabDelDxForm, MaternalLabDelDxTForm)


class MaternalLabourDelAdmin(BaseModelAdmin):

    form = MaternalLabourDelForm

    list_display = ('delivery_datetime',
                    'labour_hrs',
                    'del_mode',
                    'live_infants',
                    'live_infants_to_register')
    radio_fields = {'del_time_is_est': admin.VERTICAL,
                    'has_ga': admin.VERTICAL,
                    'has_uterine_tender': admin.VERTICAL,
                    'has_chorioamnionitis': admin.VERTICAL,
                    'has_del_comp': admin.VERTICAL,
                    'still_born_has_congen_abn': admin.VERTICAL}
admin_site.register(MaternalLabourDel, MaternalLabourDelAdmin)


class MaternalLabDelMedAdmin(BaseModelAdmin):

    form = MaternalLabDelMedForm
    list_display = ('has_health_cond', 'has_ob_comp')
    radio_fields = {'has_health_cond': admin.VERTICAL,
                    'has_ob_comp': admin.VERTICAL}
admin_site.register(MaternalLabDelMed, MaternalLabDelMedAdmin)


class MaternalLabDelClinicAdmin(BaseModelAdmin):

    form = MaternalLabDelClinicForm
    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'took_suppliments': admin.VERTICAL}
admin_site.register(MaternalLabDelClinic, MaternalLabDelClinicAdmin)


class MaternalLabDelDxAdmin(BaseModelAdmin):

    form = MaternalLabDelDxForm
    radio_fields = {'has_preg_dx': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
admin_site.register(MaternalLabDelDx, MaternalLabDelDxAdmin)


class MaternalLabDelDxTAdmin(BaseModelAdmin):

    form = MaternalLabDelDxTForm
    radio_fields = {'hospitalized': admin.VERTICAL}
admin_site.register(MaternalLabDelDxT, MaternalLabDelDxTAdmin)
