from django.contrib import admin

from .site import admin_site

from ..models import (
    InfantCongenitalAnomalies, InfantCnsAbnormalityItems, InfantFacialDefectItems,
    InfantCleftDisorderItems, InfantMouthUpGastrointestinalItems, InfantCardiovascularDisorderItems,
    InfantRespiratoryDefectItems, InfantLowerGastrointestinalItems, InfantMaleGenitalAnomalyItems,
    InfantFemaleGenitalAnomalyItems, InfantRenalAnomalyItems, InfantMusculoskeletalAbnormalItems,
    InfantSkinAbnormalItems, InfantTrisomiesChromosomeItems
)


class InfantCongenitalAnomaliesAdmin(admin.ModelAdmin):

    list_display = ('infant_visit',)

admin_site.register(InfantCongenitalAnomalies, InfantCongenitalAnomaliesAdmin)


class InfantCnsAbnormalityItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies', 'abnormality_status',)

    list_filter = ('cns_abnormality',)

    radio_fields = {
        'cns_abnormality': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantCnsAbnormalityItems, InfantCnsAbnormalityItemsAdmin)


class InfantFacialDefectItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'facial_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantFacialDefectItems, InfantFacialDefectItemsAdmin)


class InfantCleftDisorderItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'cleft_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantCleftDisorderItems, InfantCleftDisorderItemsAdmin)


class InfantMouthUpGastrointestinalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'mouth_up_gastrointest': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantMouthUpGastrointestinalItems, InfantMouthUpGastrointestinalItemsAdmin)


class InfantCardiovascularDisorderItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'cardiovascular_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantCardiovascularDisorderItems, InfantCardiovascularDisorderItemsAdmin)


class InfantRespiratoryDefectItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'respiratory_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantRespiratoryDefectItems, InfantRespiratoryDefectItemsAdmin)


class InfantLowerGastrointestinalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'lower_gastrointestinal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantLowerGastrointestinalItems, InfantLowerGastrointestinalItemsAdmin)


class InfantFemaleGenitalAnomalyItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'female_genital_anomal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantFemaleGenitalAnomalyItems, InfantFemaleGenitalAnomalyItemsAdmin)


class InfantMaleGenitalAnomalyItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'male_genital_anomal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantMaleGenitalAnomalyItems, InfantMaleGenitalAnomalyItemsAdmin)


class InfantRenalAnomalyItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'renal_amomalies': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantRenalAnomalyItems, InfantRenalAnomalyItemsAdmin)


class InfantMusculoskeletalAbnormalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'musculo_skeletal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }


admin_site.register(InfantMusculoskeletalAbnormalItems, InfantMusculoskeletalAbnormalItemsAdmin)


class InfantSkinAbnormalItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'skin_abnormality': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantSkinAbnormalItems, InfantSkinAbnormalItemsAdmin)


class InfantTrisomiesChromosomeItemsAdmin(admin.ModelAdmin):

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'triso_chromo_abnormal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin_site.register(InfantTrisomiesChromosomeItems, InfantTrisomiesChromosomeItemsAdmin)
