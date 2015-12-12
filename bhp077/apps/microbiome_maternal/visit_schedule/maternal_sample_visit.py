from collections import OrderedDict

from edc.subject.visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleGroupTuple)

from ..models import SpecimenConsent


class SpecimenConsentVisitSchedule(VisitScheduleConfiguration):

    name = 'specimen visit schedule'

    app_label = 'microbiome_maternal'

    membership_forms = OrderedDict({
        'specimen': MembershipFormTuple('specimen', SpecimenConsent, True)
    })

    schedule_groups = OrderedDict({
        'Specimen Consent': ScheduleGroupTuple('Specimen Consent', 'specimen', None, None)
    })

    visit_definitions = OrderedDict()

site_visit_schedules.register(SpecimenConsentVisitSchedule)
