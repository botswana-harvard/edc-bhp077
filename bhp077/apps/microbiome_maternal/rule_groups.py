from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, Logic,
                                             ScheduledDataRule, RequisitionRule)

from .models import PostnatalEnrollment, MaternalVisit, SexualReproductiveHealth
from edc_constants.constants import POS, YES


class PostnatalEnrollmentRuleGroup(RuleGroup):

    is_pos_has_doc = ScheduledDataRule(
        logic=Logic(
            predicate=(('verbal_hiv_status', 'equals', POS), ('evidence_hiv_status', 'equals', YES, 'and')),
            consequence='new',
            alternative='not_required'),
        target_model=['maternalinfected', 'maternalarvhistory'])

    has_rapid_test_is_pos = ScheduledDataRule(
        logic=Logic(
            predicate=(('process_rapid_test', 'equals', YES), ('rapid_test_result', 'equals', POS, 'and')),
            consequence='new',
            alternative='not_required'),
        target_model=['maternalarvpost', 'maternalarvhistory'])

    class Meta:
        app_label = 'microbiome_maternal'
        source_fk = None
        source_model = PostnatalEnrollment
site_rule_groups.register(PostnatalEnrollmentRuleGroup)


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
