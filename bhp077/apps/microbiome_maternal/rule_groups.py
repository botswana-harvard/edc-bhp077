from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, Logic,
                                             ScheduledDataRule)

from .models import PostnatalEnrollment, MaternalVisit, SexualReproductiveHealth

from edc_constants.constants import POS, YES


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
            rapid_test_done=YES,
            rapid_test_result=POS
        )
    except PostnatalEnrollment.DoesNotExist:
        return False
    return True


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
