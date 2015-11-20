from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import InfantStoolCollectionForm
from ..models import InfantStoolCollection, InfantVisit


class InfantStoolCollectionAdmin(BaseModelAdmin):

    form = InfantStoolCollectionForm
    radio_fields = {
        "sample_obtained": admin.VERTICAL,
        "stool_colection": admin.VERTICAL,
        "stool_stored": admin.VERTICAL,
        "past_diarrhea": admin.VERTICAL,
        "diarrhea_past_24hrs": admin.VERTICAL,
        "antibiotics_7days": admin.VERTICAL,
        "antibiotic_dose_24hrs": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantStoolCollectionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantStoolCollection, InfantStoolCollectionAdmin)
