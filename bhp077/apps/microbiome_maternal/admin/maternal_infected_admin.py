from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalInfectedForm
from ..models import MaternalInfected, MaternalVisit


class MaternalInfectedAdmin(BaseModelAdmin):

    form = MaternalInfectedForm
    fields = ('maternal_visit',
              'prior_health_haart',
              'prev_pregnancy_arv',
              'know_hiv_status')
    list_display = ('prior_health_haart',
                    'prev_pregnancy_arv')
    list_filter = ('prior_health_haart',
                   'prev_pregnancy_arv')
    radio_fields = {'prior_health_haart': admin.VERTICAL,
                    'prev_pregnancy_arv': admin.VERTICAL,
                    'know_hiv_status': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalInfectedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(MaternalInfected, MaternalInfectedAdmin)
