from __future__ import print_function

from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, Logic,
                                             ScheduledDataRule)

from bhp077.apps.microbiome_infant.models import InfantBirthData, InfantVisit, InfantFu
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment

from edc_constants.constants import YES, NOT_REQUIRED, POS, UNKEYED, MALE
from edc.subject.registration.models.registered_subject import RegisteredSubject


def func_maternal_hiv_pos(visit_instance):
    """Returns true if mother is hiv positive."""
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.appointment.registered_subject.relative_identifier)
    postnatal_enrollment = PostnatalEnrollment.objects.get(registered_subject=registered_subject)
    return postnatal_enrollment.maternal_hiv_status == POS


class InfantBirthDataRuleGroup(RuleGroup):

    congenital_anomalities_yes = ScheduledDataRule(
        logic=Logic(
            predicate=('congenital_anomalities', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantcongenitalanomalies'])

    class Meta:
        app_label = 'microbiome_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantBirthData

site_rule_groups.register(InfantBirthDataRuleGroup)


class InfantFuRuleGroup(RuleGroup):

    physical_assessment_yes = ScheduledDataRule(
        logic=Logic(
            predicate=('physical_assessment', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantfuphysical'])

    has_dx_yes = ScheduledDataRule(
        logic=Logic(
            predicate=('has_dx', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantfudx'])

    class Meta:
        app_label = 'microbiome_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantFu

site_rule_groups.register(InfantFuRuleGroup)


class InfantCircumcisionRuleGroup(RuleGroup):

    circumcision = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', MALE),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantcircumcision'])

    class Meta:
        app_label = 'microbiome_infant'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(InfantCircumcisionRuleGroup)
