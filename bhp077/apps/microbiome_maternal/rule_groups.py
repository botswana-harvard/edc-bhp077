from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, Logic,
                                             ScheduledDataRule, RequisitionRule)

from .models import PostnatalEnrollment, MaternalVisit, SexualReproductiveHealth

from edc_constants.constants import POS, YES, NEW, NOT_REQUIRED
from edc.subject.registration.models import RegisteredSubject


_targe_list = []

def hiv_status_pos_and_evidence_yes(visit_instance):
    try:
        PostnatalEnrollment.objects.get(
            registered_subject=visit_instance.appointment.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES
        )
    except PostnatalEnrollment.DoesNotExist:
        return False
    return True

def has_rapid_test_is_pos(visit_instance):
    try:
        PostnatalEnrollment.objects.get(
            registered_subject=visit_instance.appointment.registered_subject,
            process_rapid_test=YES,
            rapid_test_result=POS
        )
    except PostnatalEnrollment.DoesNotExist:
        return False
    return True

def hiv_pos_verbal_or_rapid_test_pos(visit_instance):
    print "hiv_pos_verbal_or_rapid_test_pos(visit_instance):"
    if has_rapid_test_is_pos(visit_instance) or \
            hiv_status_pos_and_evidence_yes(visit_instance):
        if visit_instance.visit_definition.code == '1000M':
            _targe_list = ['maternalinfected', 'maternalarvhistory', 'maternalarvpreg']
        elif visit_instance.visit_definition.code == '2000M':
            _targe_list = ['maternalarvpreg', 'maternallabdelclinic']
        elif visit_instance.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
            _targe_list = ['maternalarvpost']
        return True
    return False


class ReproductiveHealthRuleGroup(RuleGroup):

    is_srh_referral = ScheduledDataRule(
        logic=Logic(
            predicate=('srh_referral', 'equals', YES),
            consequence='new',
            alternative='not_required'),
        target_model=['srhservicesutilization'])

    class Meta:
        app_label = 'microbiome_maternal'
        source_fk = (MaternalVisit, 'maternal_visit')
        source_model = SexualReproductiveHealth

site_rule_groups.register(ReproductiveHealthRuleGroup)


class RegisteredSubjectRuleGroup(RuleGroup):

    has_rapid_test_is_positive = ScheduledDataRule(
        logic=Logic(
            predicate=hiv_pos_verbal_or_rapid_test_pos,
            consequence=NEW,
            alternative=NOT_REQUIRED),
        target_model=_targe_list)

    class Meta:
        app_label = 'microbiome_maternal'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(RegisteredSubjectRuleGroup)
