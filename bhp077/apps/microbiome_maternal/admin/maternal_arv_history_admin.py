from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..models import MaternalArvHistory, MaternalVisit
from ..forms import MaternalArvHistoryForm


class MaternalArvHistoryAdmin(BaseModelAdmin):
    form = MaternalArvHistoryForm

    list_display = ('haart_start_date', 'preg_on_haart')
    list_filter = ('preg_on_haart', )
    radio_fields = {'preg_on_haart': admin.VERTICAL,
                    'prior_preg': admin.VERTICAL, 
                    'is_date_estimated': admin.VERTICAL}
    filter_horizontal = ('prior_arv', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalArvHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArvHistory, MaternalArvHistoryAdmin)
