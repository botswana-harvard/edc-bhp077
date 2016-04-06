from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule
from edc_registration.models import RegisteredSubject

from .models import MaternalVisit, ReproductiveHealth, MaternalClinicalHistory, MaternalConsent


def func_show_srh_forms(visit_instance):
    """ Return True if participant has a version2 consent."""
    return MaternalConsent.objects.filter(subject_identifier=visit_instance.subject_identifier,
                                          version__gte=2).exists()


class MaternalRegisteredSubjectRuleGroup(RuleGroup):

    srh_forms = CrfRule(
        logic=Logic(
            predicate=func_show_srh_forms,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['maternalsrh', 'reproductivehealth'])

    class Meta:
        app_label = 'mb_maternal'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(MaternalRegisteredSubjectRuleGroup)


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

    arv_history_required = CrfRule(
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
