from __future__ import print_function

from edc_constants.constants import YES, NOT_REQUIRED, POS, UNKEYED, MALE
from edc_registration.models import RegisteredSubject
from edc_rule_groups.classes import (RuleGroup, site_rule_groups, Logic, CrfRule, RequisitionRule)

from microbiome.apps.mb_maternal.models import PostnatalEnrollment

from .models import (InfantBirthData, InfantVisit, InfantFu, InfantStoolCollection)


def func_maternal_hiv_pos(visit_instance):
    """Returns true if mother is hiv positive."""
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.appointment.registered_subject.relative_identifier)
    postnatal_enrollment = PostnatalEnrollment.objects.get(
        registered_subject=registered_subject)
    return postnatal_enrollment.enrollment_hiv_status == POS


class InfantBirthDataRuleGroup(RuleGroup):

    congenital_anomalities_yes = CrfRule(
        logic=Logic(
            predicate=('congenital_anomalities', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantcongenitalanomalies'])

    class Meta:
        app_label = 'mb_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantBirthData

site_rule_groups.register(InfantBirthDataRuleGroup)


class InfantFuRuleGroup(RuleGroup):

    physical_assessment_yes = CrfRule(
        logic=Logic(
            predicate=('physical_assessment', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantfuphysical'])

    has_dx_yes = CrfRule(
        logic=Logic(
            predicate=('has_dx', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantfudx'])

    class Meta:
        app_label = 'mb_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantFu

site_rule_groups.register(InfantFuRuleGroup)


class InfantCircumcisionRuleGroup(RuleGroup):

    circumcision = CrfRule(
        logic=Logic(
            predicate=('gender', 'equals', MALE),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['infantcircumcision'])

    class Meta:
        app_label = 'mb_infant'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(InfantCircumcisionRuleGroup)


class StoolStorageRequisitionRuleGroup(RuleGroup):

    initiation = RequisitionRule(
        logic=Logic(
            predicate=('sample_obtained', 'equals', YES),
            consequence='new',
            alternative='not_required'),
        target_model=[('mb_lab', 'infantrequisition')],
        target_requisition_panels=['Stool storage'])

    class Meta:
        app_label = 'mb_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantStoolCollection
site_rule_groups.register(StoolStorageRequisitionRuleGroup)
