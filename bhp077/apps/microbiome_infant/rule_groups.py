from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, Logic,
                                             ScheduledDataRule, RequisitionRule)

from bhp077.apps.microbiome_infant.models import InfantBirthData, InfantVisit

from edc_constants.constants import POS, YES, NEW, NOT_REQUIRED
from edc.subject.registration.models import RegisteredSubject


class InfantBirthDataRuleGroup(RuleGroup):

    congenital_anomalities_yes = ScheduledDataRule(
        logic=Logic(
            predicate=('congenital_anomalities', 'equals', YES),
            consequence=NEW,
            alternative=NOT_REQUIRED),
        target_model=['infantcongenitalanomalies'])

    class Meta:
        app_label = 'microbiome_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantBirthData

site_rule_groups.register(InfantBirthDataRuleGroup)
