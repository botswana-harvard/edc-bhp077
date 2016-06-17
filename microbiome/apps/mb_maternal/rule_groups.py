from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule
from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment

from .models import MaternalVisit, ReproductiveHealth, MaternalClinicalHistory, MaternalConsent


def get_previous_visit(visit_instance, timepoints, visit_model):
    registered_subject = visit_instance.appointment.registered_subject
    position = timepoints.index(visit_instance.appointment.visit_definition.code)
    timepoints_slice = timepoints[:position]
    if len(timepoints_slice) > 1:
        timepoints_slice.reverse()
    for point in timepoints_slice:
        try:
            previous_appointment = Appointment.objects.get(registered_subject=registered_subject,
                                                           visit_definition__code=point)
            return visit_model.objects.filter(appointment=previous_appointment).order_by('-created').first()
        except Appointment.DoesNotExist:
            pass
        except visit_model.DoesNotExist:
            pass
        except AttributeError:
            pass
    return None


def func_show_srh_forms(visit_instance):
    """ Returns True if participant has a version2 consent."""
    return MaternalConsent.objects.filter(subject_identifier=visit_instance.subject_identifier,
                                          version__gte=2).exists()


def func_show_srh_services_utilization(visit_instance):
    """Returns True if participant was referred to shr in the last visit."""
    previous_visit = get_previous_visit(visit_instance,
                                        ['1000M', '2000M', '2010M', '2030M', '2060M', '2090M', '2120M'],
                                        MaternalVisit)
    if not previous_visit:
        return False
    try:
        rep_health_previous = ReproductiveHealth.objects.get(maternal_visit=previous_visit)
        return rep_health_previous.srh_referral == YES
    except ReproductiveHealth.DoesNotExist:
        return False


class MaternalRegisteredSubjectRuleGroup(RuleGroup):

    srh_forms = CrfRule(
        logic=Logic(
            predicate=func_show_srh_forms,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['reproductivehealth'])

    srh_utilization = CrfRule(
        logic=Logic(
            predicate=func_show_srh_services_utilization,
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['maternalsrh'])

    class Meta:
        app_label = 'mb_maternal'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(MaternalRegisteredSubjectRuleGroup)


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
