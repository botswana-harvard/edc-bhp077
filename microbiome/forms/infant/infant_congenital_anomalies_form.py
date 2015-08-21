from django.forms.models import ModelForm

from microbiome.models.microbiome_infant import (
    InfantCongenitalAnomalies, InfantCnsAbnormalityItems, InfantFacialDefectItems,
    InfantCleftDisorderItems, InfantMouthUpGastrointestinalItems,
    InfantCardiovascularDisorderItems, InfantRespiratoryDefectItems, InfantLowerGastrointestinalItems,
    InfantFemaleGenitalAnomalyItems, InfantMaleGenitalAnomalyItems, InfantMusculoskeletalAbnormalItems,
    InfantTrisomiesChromosomeItems, InfantOtherAbnormalityItems, InfantSkinAbnormalItems,
    InfantRenalAnomalyItems)


class InfantCongenitalAnomaliesForm(ModelForm):

    class Meta:
        model = InfantCongenitalAnomalies
        fields = '__all__'


class InfantCnsAbnormalityItemsForm(ModelForm):

    class Meta:
        model = InfantCnsAbnormalityItems
        fields = '__all__'


class InfantFacialDefectItemsForm(ModelForm):

    class Meta:
        model = InfantFacialDefectItems
        fields = '__all__'


class InfantCleftDisorderItemsForm(ModelForm):

    class Meta:
        model = InfantCleftDisorderItems
        fields = '__all__'


class InfantMouthUpGastrointestinalItemsForm(ModelForm):

    class Meta:
        model = InfantMouthUpGastrointestinalItems
        fields = '__all__'


class InfantCardiovascularDisorderItemsForm(ModelForm):

    class Meta:
        model = InfantCardiovascularDisorderItems
        fields = '__all__'


class InfantRespiratoryDefectItemsForm(ModelForm):

    class Meta:
        model = InfantRespiratoryDefectItems
        fields = '__all__'


class InfantLowerGastrointestinalItemsForm(ModelForm):

    class Meta:
        model = InfantLowerGastrointestinalItems
        fields = '__fields__'


class InfantFemaleGenitalAnomalyItemsForm(ModelForm):

    class Meta:
        model = InfantFemaleGenitalAnomalyItems
        fields = '__all__'


class InfantMaleGenitalAnomalyItemsForm(ModelForm):

    class Meta:
        model = InfantMaleGenitalAnomalyItems
        fields = '__all__'


class InfantRenalAnomalyItems(ModelForm):

    class Meta:
        model = InfantRenalAnomalyItems
        fields = '__all__'


class InfantMusculoskeletalAbnormalItemsForm(ModelForm):

    class Meta:
        model = InfantMusculoskeletalAbnormalItems
        fields = '__all__'


class InfantSkinAbnormalItemsForm(ModelForm):

    class Meta:
        model = InfantSkinAbnormalItems
        fields = '__all__'


class InfantTrisomiesChromosomeItemsForm(ModelForm):

    class Meta:
        model = InfantTrisomiesChromosomeItems
        fields = '__all__'


class InfantOtherAbnormalityItemsForm(ModelForm):

    class Meta:
        model = InfantOtherAbnormalityItems
        fields = '__all__'
