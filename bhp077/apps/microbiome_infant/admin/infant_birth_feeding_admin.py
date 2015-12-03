from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin
from edc.base.modeladmin.admin import BaseTabularInline

from ..models import InfantBirthFeedVaccine, InfantVaccines
from ..forms import InfantVaccinesForm, InfantBirthFeedVaccineForm


class InfantVaccinesInline(BaseTabularInline):

    model = InfantVaccines
    form = InfantVaccinesForm
    extra = 0


class InfantBirthFeedVaccineAdmin(BaseModelAdmin):
    form = InfantBirthFeedVaccineForm

    list_display = ('feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    inlines = [InfantVaccinesInline]

    radio_fields = {'feeding_after_delivery': admin.VERTICAL}
admin.site.register(InfantBirthFeedVaccine, InfantBirthFeedVaccineAdmin)


class InfantVaccinesAdmin(BaseModelAdmin):
    form = InfantVaccinesForm
admin.site.register(InfantVaccines, InfantVaccinesAdmin)
