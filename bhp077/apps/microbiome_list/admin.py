from django.contrib import admin
from edc_base.modeladmin.admin import BaseModelAdmin
from bhp077.apps.microbiome_list.models import (ChronicConditions, Contraceptives,
                                                DiseasesAtEnrollment, HouseholdGoods,
                                                PriorArv, AutopsyInfoSource,
                                                Suppliments, InfantVaccines)
from bhp077.apps.microbiome_list.models.maternal_lab_del import HealthCond, DelComp, ObComp, LabDelDx


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


class AutopsyInfoSourceAdmin(BaseModelAdmin):
    pass
admin.site.register(AutopsyInfoSource, AutopsyInfoSourceAdmin)


class SupplimentsAdmin(BaseModelAdmin):
    pass
admin.site.register(Suppliments, SupplimentsAdmin)


class InfantVaccinesAdmin(BaseModelAdmin):
    pass
admin.site.register(InfantVaccines, InfantVaccinesAdmin)


class HealthCondAdmin(BaseModelAdmin):
    pass
admin.site.register(HealthCond, HealthCondAdmin)


class DelCompAdmin(BaseModelAdmin):
    pass
admin.site.register(DelComp, DelCompAdmin)


class ObCompAdmin(BaseModelAdmin):
    pass
admin.site.register(ObComp, ObCompAdmin)


class LabDelDxAdmin(BaseModelAdmin):
    pass
admin.site.register(LabDelDx, LabDelDxAdmin)
