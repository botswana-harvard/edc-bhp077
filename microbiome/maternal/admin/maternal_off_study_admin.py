from django.contrib import admin

from edc.subject.off_study.admin import BaseOffStudyModelAdmin

from ..models import MaternalOffStudy, MaternalVisit
from ..forms import MaternalOffStudyForm


class MaternalOffStudyAdmin(BaseOffStudyModelAdmin):
    form = MaternalOffStudyForm
    dashboard_type = 'maternal'
    visit_model_name = 'maternalvisit'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))

        return super(MaternalOffStudyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalOffStudy, MaternalOffStudyAdmin)
