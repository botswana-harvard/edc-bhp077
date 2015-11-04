from django import forms
from bhp077.apps.microbiome_list.models import (ChronicConditions, Contraceptives,
                                                DiseasesAtEnrollment, HouseholdGoods,
                                                PriorArv, AutopsyInfoSource,
                                                Suppliments)


class ChronicConditionsForm (forms.ModelForm):

    class Meta:
        model = ChronicConditions


class ContraceptivesForm (forms.ModelForm):

    class Meta:
        model = Contraceptives


class DiseasesAtEnrollmentForm (forms.ModelForm):

    class Meta:
        model = DiseasesAtEnrollment


class HouseholdGoodsForm (forms.ModelForm):

    class Meta:
        model = HouseholdGoods


class PriorArvForm (forms.ModelForm):

    class Meta:
        model = PriorArv


class AutopsyInfoSourceForm (forms.ModelForm):

    class Meta:
        model = AutopsyInfoSource


class SupplimentsForm (forms.ModelForm):

    class Meta:
        model = Suppliments
