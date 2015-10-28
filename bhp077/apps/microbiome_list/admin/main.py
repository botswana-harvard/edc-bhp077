from django.contrib import admin
from edc_base.modeladmin.admin import BaseModelAdmin
from bhp077.apps.microbiome_list.models import (ChronicConditions, Contraceptives,
                                         DiseasesAtEnrollment, HouseholdGoods, PriorArv)


class ChronicConditionsAdmin(BaseModelAdmin):
    pass
admin.site.register(ChronicConditions, ChronicConditionsAdmin)


class ContraceptivesAdmin(BaseModelAdmin):
    pass
admin.site.register(Contraceptives, ContraceptivesAdmin)


class DiseasesAtEnrollmentAdmin(BaseModelAdmin):
    pass
admin.site.register(DiseasesAtEnrollment, DiseasesAtEnrollmentAdmin)


class HouseholdGoodsAdmin(BaseModelAdmin):
    pass
admin.site.register(HouseholdGoods, HouseholdGoodsAdmin)


class PriorArvAdmin(BaseModelAdmin):
    pass
admin.site.register(PriorArv, PriorArvAdmin)
