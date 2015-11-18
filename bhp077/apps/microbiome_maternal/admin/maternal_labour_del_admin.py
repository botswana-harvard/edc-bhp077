from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..models import (MaternalLabourDel, MaternalLabDelMed, MaternalLabDelClinic,
                      MaternalLabDelDx, MaternalLabDelDxT, MaternalVisit)
from ..forms import (MaternalLabourDelForm, MaternalLabDelMedForm,
                     MaternalLabDelClinicForm, MaternalLabDelDxForm, MaternalLabDelDxTForm)


class MaternalLabourDelAdmin(BaseModelAdmin):

    form = MaternalLabourDelForm

    list_display = ('delivery_datetime',
                    'labour_hrs',
                    'del_hosp',
                    'live_infants_to_register')
    radio_fields = {'del_time_is_est': admin.VERTICAL,
                    'has_uterine_tender': admin.VERTICAL,
                    'has_chorioamnionitis': admin.VERTICAL,
                    'del_hosp': admin.VERTICAL,
                    'has_del_comp': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalLabourDelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabourDel, MaternalLabourDelAdmin)


class MaternalLabDelMedAdmin(BaseModelAdmin):

    form = MaternalLabDelMedForm
    list_display = ('has_health_cond', 'has_ob_comp')
    radio_fields = {'has_health_cond': admin.VERTICAL,
                    'has_ob_comp': admin.VERTICAL,
                    'took_suppliments': admin.VERTICAL}
    filter_horizontal = ('suppliments', 'health_cond', 'ob_comp')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalLabDelMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabDelMed, MaternalLabDelMedAdmin)


class MaternalLabDelClinicAdmin(BaseModelAdmin):

    form = MaternalLabDelClinicForm
    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalLabDelClinicAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabDelClinic, MaternalLabDelClinicAdmin)


class MaternalLabDelDxTInlineAdmin(BaseTabularInline):
    model = MaternalLabDelDxT
    form = MaternalLabDelDxTForm
    extra = 1


class MaternalLabDelDxAdmin(BaseModelAdmin):

    form = MaternalLabDelDxForm
    radio_fields = {'has_preg_dx': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('wcs_dx_adult',)
    inlines = [MaternalLabDelDxTInlineAdmin, ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalLabDelDxAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabDelDx, MaternalLabDelDxAdmin)


class MaternalLabDelDxTAdmin(BaseModelAdmin):

    form = MaternalLabDelDxTForm
    radio_fields = {'hospitalized': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalLabDelDxTAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabDelDxT, MaternalLabDelDxTAdmin)
