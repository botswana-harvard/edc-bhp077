from collections import OrderedDict

from edc_constants.constants import REQUIRED, NOT_ADDITIONAL, ADDITIONAL, NOT_REQUIRED
from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                EntryTuple, MembershipFormTuple,
                                                ScheduleGroupTuple, RequisitionPanelTuple)
from ..models import SampleConsent


class SampleConsentVisitSchedule(VisitScheduleConfiguration):

    name = 'sample visit schedule'
    app_label = 'microbiome_maternal'
    membership_forms = OrderedDict({
        'sample': MembershipFormTuple('sample', SampleConsent, True),
    })

    schedule_groups = OrderedDict({
        'Sample Consent': ScheduleGroupTuple('Sample Consent', 'sample', None, None),
    })

    visit_definitions = OrderedDict()

site_visit_schedules.register(SampleConsentVisitSchedule)
