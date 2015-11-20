from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline

from ..forms import InfantFuImmunizationsForm
from ..models import InfantFuImmunizations, VaccinesReceived, VaccinesMissed


class VaccinesReceivedInlineAdmin(BaseTabularInline):
    model = VaccinesReceived
    extra = 1


class VaccinesMissedInlineAdmin(BaseTabularInline):
    model = VaccinesMissed
    extra = 1


class InfantFuImmunizationsAdmin(BaseModelAdmin):
    form = InfantFuImmunizationsForm
    inlines = [VaccinesReceivedInlineAdmin, VaccinesMissedInlineAdmin, ]
    radio_fields = {'vaccines_received': admin.VERTICAL,
                    'vaccines_missed': admin.VERTICAL}

admin.site.register(InfantFuImmunizations, InfantFuImmunizationsAdmin)
