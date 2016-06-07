from edc_constants.constants import YES, NOT_REQUIRED, POS, UNKEYED, MALE
from edc_meta_data.models import CrfMetaData
from edc_registration.models import RegisteredSubject
from edc_rule_groups.classes import (RuleGroup, site_rule_groups, Logic, CrfRule, RequisitionRule)
from edc_visit_schedule.models import VisitDefinition

from microbiome.apps.mb_maternal.rule_groups import get_previous_visit
from microbiome.apps.mb_maternal.models import PostnatalEnrollment

from ..mb.constants import DISCONTINUED, NEVER_STARTED
from .models import (InfantBirthData, InfantVisit, InfantFu, InfantStoolCollection, InfantArvProph)


def func_maternal_hiv_pos(visit_instance):
    """Returns true if mother is hiv positive."""
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.appointment.registered_subject.relative_identifier)
    postnatal_enrollment = PostnatalEnrollment.objects.get(
        registered_subject=registered_subject)
    return postnatal_enrollment.enrollment_hiv_status == POS


def func_show_infant_arv_proph(visit_instance):
    previous_visit = get_previous_visit(visit_instance,
                                        ['2000', '2010', '2030', '2060', '2090', '2120'],
                                        InfantVisit)
    if not previous_visit:
        return False
    try:
        intant_arv_proph = InfantArvProph.objects.get(infant_visit=previous_visit)
        return intant_arv_proph.arv_status == DISCONTINUED or intant_arv_proph.arv_status == NEVER_STARTED
    except InfantArvProph.DoesNotExist:
        if visit_instance.appointment.visit_definition.code == '2010':
            return False
        return True


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


class InfantRegisteredSubjectRuleGroup(RuleGroup):

    arv_proph = CrfRule(
        logic=Logic(
            predicate=func_show_infant_arv_proph,
            consequence=NOT_REQUIRED,
            alternative=UNKEYED),
        target_model=[('mb_infant', 'infantarvproph')])

    class Meta:
        app_label = 'mb_infant'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(InfantRegisteredSubjectRuleGroup)
