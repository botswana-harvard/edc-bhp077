from django.contrib import admin

from ..models import (
    InfantCongenitalAnomalies, InfantCnsAbnormalityItems, InfantFacialDefectItems,
    InfantCleftDisorderItems, InfantMouthUpGastrointestinalItems, InfantCardiovascularDisorderItems,
    InfantRespiratoryDefectItems, InfantLowerGastrointestinalItems, InfantMaleGenitalAnomalyItems,
    InfantFemaleGenitalAnomalyItems, InfantRenalAnomalyItems, InfantMusculoskeletalAbnormalItems,
    InfantSkinAbnormalItems, InfantTrisomiesChromosomeItems
)


@admin.register(InfantCongenitalAnomalies)
class InfantCongenitalAnomalies(admin.ModelAdmin):

    list_display = ('infant_visit',)


@admin.register(InfantCnsAbnormalityItems)
class InfantCnsAbnormalityItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies', 'abnormality_status',)

    list_filter = ('cns_abnormality',)


@admin.register(InfantFacialDefectItems)
class InfantFacialDefectItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantCleftDisorderItems)
class InfantCleftDisorderItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantMouthUpGastrointestinalItems)
class InfantMouthUpGastrointestinalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantCardiovascularDisorderItems)
class InfantCardiovascularDisorderItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantRespiratoryDefectItems)
class InfantRespiratoryDefectItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantLowerGastrointestinalItems)
class InfantLowerGastrointestinalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantFemaleGenitalAnomalyItems)
class InfantFemaleGenitalAnomalyItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantMaleGenitalAnomalyItems)
class InfantMaleGenitalAnomalyItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantRenalAnomalyItems)
class InfantRenalAnomalyItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantMusculoskeletalAbnormalItems)
class InfantMusculoskeletalAbnormalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantSkinAbnormalItems)
class InfantSkinAbnormalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)


@admin.register(InfantTrisomiesChromosomeItems)
class InfantTrisomiesChromosomeItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)
