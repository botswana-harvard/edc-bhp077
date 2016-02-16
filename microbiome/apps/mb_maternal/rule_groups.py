from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule

from .models import MaternalVisit, ReproductiveHealth, MaternalClinicalHistory


class ReproductiveHealthRuleGroup(RuleGroup):

    is_srh_referral = CrfRule(
        logic=Logic(
            predicate=('srh_referral', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['maternalsrh'])

    class Meta:
        app_label = 'mb_maternal'
        source_fk = (MaternalVisit, 'maternal_visit')
        source_model = ReproductiveHealth

site_rule_groups.register(ReproductiveHealthRuleGroup)


class MaternalArvHistoryRuleGroup(RuleGroup):

    is_srh_referral = CrfRule(
        logic=Logic(
            predicate=(('prior_health_haart', 'equals', YES), ('prev_pregnancy_arv', 'equals', YES, 'or')),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['maternalarvhistory'])

    class Meta:
        app_label = 'mb_maternal'
        source_fk = (MaternalVisit, 'maternal_visit')
        source_model = MaternalClinicalHistory

site_rule_groups.register(MaternalArvHistoryRuleGroup)
