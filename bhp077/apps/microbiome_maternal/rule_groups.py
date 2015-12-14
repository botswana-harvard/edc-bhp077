
from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED
from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, Logic, ScheduledDataRule

from .models import MaternalVisit, SexualReproductiveHealth


class ReproductiveHealthRuleGroup(RuleGroup):

    is_srh_referral = ScheduledDataRule(
        logic=Logic(
            predicate=('srh_referral', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['maternalsrh'])

    class Meta:
        app_label = 'microbiome_maternal'
        source_fk = (MaternalVisit, 'maternal_visit')
        source_model = SexualReproductiveHealth

site_rule_groups.register(ReproductiveHealthRuleGroup)
