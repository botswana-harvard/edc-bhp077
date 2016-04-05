import factory

from django.utils import timezone

from edc_constants.constants import YES

from microbiome.apps.mb_maternal.models import MaternalDemographics

from ..factories import MaternalVisitFactory


class MaternalDemographicsFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalDemographics

    report_datetime = timezone.now()
    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    marital_status = 'Single'
    ethnicity = 'Black African'
    highest_education = 'Tertiary'
    current_occupation = 'Student'
    provides_money = 'Mother'
    money_earned = 'P1001-5000 per month / P212 - 1157 per week'
    own_phone = YES
    house_electrified = YES
    house_fridge = YES
    cooking_method = 'Gas or electric stove'
    toilet_facility = 'Indoor toilet'
    house_people_number = 1
    house_type = 'Formal: Tin-roofed, concrete walls'
