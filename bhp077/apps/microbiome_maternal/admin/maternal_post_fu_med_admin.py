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

admin.site.register(MaternalPostFuMedItems, MaternalPostFuMedItemsAdmin)


class MaternalPostFuMedAdmin(BaseModelAdmin):

    form = MaternalPostFuMedForm
    inlines = [MaternalPostFuMedItemsInlineAdmin, ]

    fields = (
        "maternal_visit",
        "maternal_post_fu",
        "report_datetime",
        "has_taken_meds",
    )

    radio_fields = {
        "has_taken_meds": admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        if db_field.name == "maternal_post_fu":
            if request.GET.get('maternal_visit'):
                infant_visit = MaternalVisit.objects.get(id=request.GET.get('maternal_visit'))
                kwargs["queryset"] = MaternalPostFuMed.objects.filter(registered_subject=infant_visit.appointment.registered_subject)
        return super(MaternalPostFuMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuMed, MaternalPostFuMedAdmin)
