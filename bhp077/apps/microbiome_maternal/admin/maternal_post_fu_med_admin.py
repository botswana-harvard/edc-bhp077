from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..forms import MaternalPostFuMedForm, MaternalPostFuMedItemsForm
from ..models import MaternalPostFuMed, MaternalPostFuMedItems, MaternalVisit


class MaternalPostFuMedItemsInlineAdmin(BaseTabularInline):

    model = MaternalPostFuMedItems
    form = MaternalPostFuMedItemsForm
    extra = 1


class MaternalPostFuMedItemsAdmin(BaseModelAdmin):
    form = MaternalPostFuMedItemsForm

    radio_fields = {
        "medication": admin.VERTICAL,
        "drug_route": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_post_fu_med":
                kwargs["queryset"] = MaternalPostFuMed.objects.filter(id=request.GET.get('maternal_post_fu_med'))
        return super(MaternalPostFuMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuMedItems, MaternalPostFuMedItemsAdmin)


class MaternalPostFuMedAdmin(BaseModelAdmin):

    form = MaternalPostFuMedForm
    inlines = [MaternalPostFuMedItemsInlineAdmin, ]

    fields = (
        "maternal_visit",
        "report_datetime",
        "has_taken_meds",
    )

    radio_fields = {
        "has_taken_meds": admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalPostFuMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuMed, MaternalPostFuMedAdmin)
