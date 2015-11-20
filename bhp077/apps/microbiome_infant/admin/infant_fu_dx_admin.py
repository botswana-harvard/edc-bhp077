from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin, BaseTabularInline

from ..models import InfantFuDx, InfantVisit, InfantFuDxItems
from ..forms import InfantFuDxItemsForm


class InfantFuDxItemsInline(BaseTabularInline):

    model = InfantFuDxItems
    form = InfantFuDxItemsForm
    extra = 0


class InfantFuDxAdmin(BaseModelAdmin):

    inlines = [InfantFuDxItemsInline, ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantFuDxAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFuDx, InfantFuDxAdmin)
