from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin
from edc.base.modeladmin.admin import BaseTabularInline

from ..models import (
    InfantCongenitalAnomalies, InfantCnsAbnormalityItems, InfantFacialDefectItems,
    InfantCleftDisorderItems, InfantMouthUpGastrointestinalItems, InfantCardiovascularDisorderItems,
    InfantRespiratoryDefectItems, InfantLowerGastrointestinalItems, InfantMaleGenitalAnomalyItems,
    InfantFemaleGenitalAnomalyItems, InfantRenalAnomalyItems, InfantMusculoskeletalAbnormalItems,
    InfantSkinAbnormalItems, InfantTrisomiesChromosomeItems, InfantVisit
)


from bhp077.apps.microbiome_infant.forms import (
    InfantCongenitalAnomaliesForm, InfantFacialDefectItemsForm,
    InfantCleftDisorderItemsForm, InfantMouthUpGastrointestinalItemsForm, InfantCardiovascularDisorderItemsForm,
    InfantRespiratoryDefectItemsForm, InfantLowerGastrointestinalItemsForm, InfantFemaleGenitalAnomalyItemsForm,
    InfantMaleGenitalAnomalyItemsForm, InfantRenalAnomalyItemsForm, InfantMusculoskeletalAbnormalItemsForm,
    InfantSkinAbnormalItemsForm, InfantTrisomiesChromosomeItemsForm,
    InfantCnsAbnormalityItemsForm
)


class InfantCnsAbnormalityItemsAdmin(BaseModelAdmin):
    form = InfantCnsAbnormalityItemsForm
    list_display = ('congenital_anomalies', 'abnormality_status',)

    list_filter = ('cns_abnormality',)

    radio_fields = {
        'cns_abnormality': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantCnsAbnormalityItems, InfantCnsAbnormalityItemsAdmin)


class InfantCnsAbnormalityItemsInline(BaseTabularInline):

    model = InfantCnsAbnormalityItems
    form = InfantCnsAbnormalityItemsForm
    extra = 0


class InfantFacialDefectItemsAdmin(BaseModelAdmin):
    form = InfantFacialDefectItemsForm
    list_display = ('congenital_anomalies',)

    radio_fields = {
        'facial_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }
admin.site.register(InfantFacialDefectItems, InfantFacialDefectItemsAdmin)


class InfantFacialDefectItemsInline(BaseTabularInline):

    model = InfantFacialDefectItems
    form = InfantFacialDefectItemsForm
    extra = 0


class InfantCleftDisorderItemsAdmin(BaseModelAdmin):
    form = InfantCleftDisorderItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'cleft_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantCleftDisorderItems, InfantCleftDisorderItemsAdmin)


class InfantCleftDisorderItemsInline(BaseTabularInline):

    model = InfantCleftDisorderItems
    form = InfantCleftDisorderItemsForm
    extra = 0


class InfantMouthUpGastrointestinalItemsAdmin(BaseModelAdmin):
    form = InfantMouthUpGastrointestinalItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'mouth_up_gastrointest': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantMouthUpGastrointestinalItems, InfantMouthUpGastrointestinalItemsAdmin)


class InfantMouthUpGastrointestinalItemsInline(BaseTabularInline):

    model = InfantMouthUpGastrointestinalItems
    form = InfantMouthUpGastrointestinalItemsForm
    extra = 0


class InfantCardiovascularDisorderItemsAdmin(BaseModelAdmin):
    form = InfantCardiovascularDisorderItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'cardiovascular_disorder': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantCardiovascularDisorderItems, InfantCardiovascularDisorderItemsAdmin)


class InfantCardiovascularDisorderItemsInline(BaseTabularInline):

    model = InfantCardiovascularDisorderItems
    form = InfantCardiovascularDisorderItemsForm
    extra = 0


class InfantRespiratoryDefectItemsAdmin(BaseModelAdmin):
    form = InfantRespiratoryDefectItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'respiratory_defect': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantRespiratoryDefectItems, InfantRespiratoryDefectItemsAdmin)


class InfantRespiratoryDefectItemsInline(BaseTabularInline):

    model = InfantRespiratoryDefectItems
    form = InfantRespiratoryDefectItemsForm
    extra = 0


class InfantLowerGastrointestinalItemsAdmin(BaseModelAdmin):
    form = InfantLowerGastrointestinalItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'lower_gastrointestinal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantLowerGastrointestinalItems, InfantLowerGastrointestinalItemsAdmin)


class InfantLowerGastrointestinalItemsInline(BaseTabularInline):

    model = InfantLowerGastrointestinalItems
    form = InfantLowerGastrointestinalItemsForm
    extra = 0


class InfantFemaleGenitalAnomalyItemsAdmin(BaseModelAdmin):
    form = InfantFemaleGenitalAnomalyItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'female_genital_anomal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantFemaleGenitalAnomalyItems, InfantFemaleGenitalAnomalyItemsAdmin)


class InfantFemaleGenitalAnomalyItemsInline(BaseTabularInline):

    model = InfantFemaleGenitalAnomalyItems
    form = InfantFemaleGenitalAnomalyItemsForm
    extra = 0


class InfantMaleGenitalAnomalyItemsAdmin(BaseModelAdmin):
    form = InfantMaleGenitalAnomalyItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'male_genital_anomal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantMaleGenitalAnomalyItems, InfantMaleGenitalAnomalyItemsAdmin)


class InfantMaleGenitalAnomalyItemsInline(BaseTabularInline):

    model = InfantMaleGenitalAnomalyItems
    form = InfantMaleGenitalAnomalyItemsForm
    extra = 0


class InfantRenalAnomalyItemsAdmin(BaseModelAdmin):
    form = form = InfantRenalAnomalyItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'renal_amomalies': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantRenalAnomalyItems, InfantRenalAnomalyItemsAdmin)


class InfantRenalAnomalyItemsInline(BaseTabularInline):

    model = InfantRenalAnomalyItems
    form = InfantRenalAnomalyItemsForm
    extra = 0


class InfantMusculoskeletalAbnormalItemsAdmin(BaseModelAdmin):
    form = form = InfantMusculoskeletalAbnormalItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'musculo_skeletal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantMusculoskeletalAbnormalItems, InfantMusculoskeletalAbnormalItemsAdmin)


class InfantMusculoskeletalAbnormalItemsInline(BaseTabularInline):

    model = InfantMusculoskeletalAbnormalItems
    form = InfantMusculoskeletalAbnormalItemsForm
    extra = 0


class InfantSkinAbnormalItemsAdmin(BaseModelAdmin):
    form = form = InfantSkinAbnormalItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'skin_abnormality': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantSkinAbnormalItems, InfantSkinAbnormalItemsAdmin)


class InfantSkinAbnormalItemsInline(BaseTabularInline):

    model = InfantSkinAbnormalItems
    form = InfantSkinAbnormalItemsForm
    extra = 0


class InfantTrisomiesChromosomeItemsAdmin(BaseModelAdmin):
    form = InfantTrisomiesChromosomeItemsForm

    list_display = ('congenital_anomalies',)

    radio_fields = {
        'triso_chromo_abnormal': admin.VERTICAL,
        'abnormality_status': admin.VERTICAL
    }

admin.site.register(InfantTrisomiesChromosomeItems, InfantTrisomiesChromosomeItemsAdmin)


class InfantTrisomiesChromosomeItemsInline(BaseTabularInline):

    model = InfantTrisomiesChromosomeItems
    form = InfantTrisomiesChromosomeItemsForm
    extra = 0


class InfantCongenitalAnomaliesAdmin(BaseModelAdmin):

    form = InfantCongenitalAnomaliesForm
    dashboard_type = 'infant'
    visit_model_name = 'infantvisit'

    list_display = ('infant_visit',)

    inlines = [
        InfantCnsAbnormalityItemsInline,
        InfantFacialDefectItemsInline,
        InfantCleftDisorderItemsInline,
        InfantMouthUpGastrointestinalItemsInline,
        InfantCardiovascularDisorderItemsInline,
        InfantRespiratoryDefectItemsInline,
        InfantLowerGastrointestinalItemsInline,
        InfantFemaleGenitalAnomalyItemsInline,
        InfantMaleGenitalAnomalyItemsInline,
        InfantRenalAnomalyItemsInline,
        InfantMusculoskeletalAbnormalItemsInline,
        InfantSkinAbnormalItemsInline,
        InfantTrisomiesChromosomeItemsInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
            if request.GET.get('infant_visit'):
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantCongenitalAnomaliesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantCongenitalAnomalies, InfantCongenitalAnomaliesAdmin)
