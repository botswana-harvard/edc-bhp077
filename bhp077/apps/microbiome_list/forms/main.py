from django import forms
from microbiome.list.models import (ChronicConditions, Contraceptives,
                                    DiseasesAtEnrollment, HouseholdGoods, PriorArv)


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
