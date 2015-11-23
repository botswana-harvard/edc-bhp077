from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin
from edc.base.modeladmin.admin import BaseTabularInline

from ..models import InfantBirthFeedVaccine, InfantVaccines
from ..forms import InfantVaccinesForm


class InfantVaccinesInline(BaseTabularInline):

    model = InfantVaccines
    form = InfantVaccinesForm
    extra = 0


class InfantBirthFeedVaccineAdmin(BaseModelAdmin):

    list_display = ('infant_birth', 'feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    inlines = [InfantVaccinesInline]

    radio_fields = {'feeding_after_delivery': admin.VERTICAL}
admin.site.register(InfantBirthFeedVaccine, InfantBirthFeedVaccineAdmin)
