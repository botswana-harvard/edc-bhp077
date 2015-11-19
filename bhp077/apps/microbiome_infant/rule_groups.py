from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, Logic,
                                             ScheduledDataRule)

from bhp077.apps.microbiome_infant.models import InfantBirthData, InfantVisit, InfantFu

from edc_constants.constants import YES, NEW, NOT_REQUIRED


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


class InfantFuRuleGroup(RuleGroup):

    physical_assessment_yes = ScheduledDataRule(
        logic=Logic(
            predicate=('physical_assessment', 'equals', YES),
            consequence=NEW,
            alternative=NOT_REQUIRED),
        target_model=['infantfuphysical'])

    has_dx_yes = ScheduledDataRule(
        logic=Logic(
            predicate=('has_dx', 'equals', YES),
            consequence=NEW,
            alternative=NOT_REQUIRED),
        target_model=['infantfudx'])

    class Meta:
        app_label = 'microbiome_infant'
        source_fk = (InfantVisit, 'infant_visit')
        source_model = InfantFu

site_rule_groups.register(InfantFuRuleGroup)
