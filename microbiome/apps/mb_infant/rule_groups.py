from edc_constants.constants import YES, NOT_REQUIRED, POS, UNKEYED, MALE
from edc_meta_data.models import CrfMetaData
from edc_registration.models import RegisteredSubject
from edc_rule_groups.classes import (RuleGroup, site_rule_groups, Logic, CrfRule, RequisitionRule)
from edc_visit_schedule.models import VisitDefinition

from microbiome.apps.mb_maternal.models import PostnatalEnrollment

from .models import (InfantBirthData, InfantVisit, InfantFu, InfantStoolCollection, InfantArvProph)


def func_maternal_hiv_pos(visit_instance):
    """Returns true if mother is hiv positive."""
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.appointment.registered_subject.relative_identifier)
    postnatal_enrollment = PostnatalEnrollment.objects.get(
        registered_subject=registered_subject)
    return postnatal_enrollment.enrollment_hiv_status == POS


def func_infant_hiv_exposed(visit_instance):
    """Returns true if the infant is HIV-exposed uninfected"""
    visit_def = VisitDefinition.objects.filter(grouping='infant')
    visit = []
    for x in visit_def:
        visit.append(x.code)

    if not (visit_instance.appointment.visit_definition.code in ['2000']):
        prev_visit_index = visit.index(visit_instance.appointment.visit_definition.code) - 1

        prev_infant_visit = InfantVisit.objects.get(
            appointment__registered_subject=visit_instance.appointment.registered_subject,
            appointment__visit_definition__code=visit[prev_visit_index])

        try:
            prev_crf_entry = CrfMetaData.objects.get(
                registered_subject=visit_instance.appointment.registered_subject,
                appointment=prev_infant_visit.appointment,
                crf_entry__model_name='infantarvproph')

            if prev_crf_entry.entry_status == NOT_REQUIRED:
                return True
        except CrfMetaData.DoesNotExist:
            pass

        try:
            infant_arv_proph = InfantArvProph.objects.get(infant_visit=prev_infant_visit)
            if func_maternal_hiv_pos(visit_instance) and infant_arv_proph.arv_status == 'discontinued':
                return True
        except InfantArvProph.DoesNotExist:
            """If InfantArvProph does not exist then it was not_required in previous visit"""
            pass
    return False


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


class RegisteredSubjectRuleGroup(RuleGroup):

    arv_proph = CrfRule(
        logic=Logic(
            predicate=func_infant_hiv_exposed,
            consequence=NOT_REQUIRED,
            alternative=UNKEYED),
        target_model=[('mb_infant', 'infantarvproph')])

    class Meta:
        app_label = 'mb_infant'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(RegisteredSubjectRuleGroup)
