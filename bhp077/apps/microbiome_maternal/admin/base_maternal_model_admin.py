from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import MaternalVisit


class BaseMaternalModelAdmin(BaseModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(BaseMaternalModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
