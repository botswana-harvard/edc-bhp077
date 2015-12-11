from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import MaternalOffStudy, MaternalVisit
from ..forms import MaternalOffStudyForm


class MaternalOffStudyAdmin(BaseModelAdmin):
    form = MaternalOffStudyForm
    dashboard_type = 'maternal'
    visit_model_name = 'maternalvisit'

    fields = (
        'registered_subject',
        'maternal_visit',
        'offstudy_date',
        'reason',
        'reason_other',
        'has_scheduled_data',
        'comment')

    radio_fields = {
        "has_scheduled_data": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))

        return super(MaternalOffStudyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalOffStudy, MaternalOffStudyAdmin)
