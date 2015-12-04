from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalBreastHealthForm
from ..models import MaternalBreastHealth, MaternalVisit


class MaternalBreastHealthAdmin(BaseModelAdmin):

    form = MaternalBreastHealthForm

    radio_fields = {
        "breast_feeding": admin.VERTICAL,
        "has_mastitis": admin.VERTICAL,
        "mastitis": admin.VERTICAL,
        "has_lesions": admin.VERTICAL,
        "lesions": admin.VERTICAL,
        "advised_stop_bf": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalBreastHealthAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalBreastHealth, MaternalBreastHealthAdmin)
