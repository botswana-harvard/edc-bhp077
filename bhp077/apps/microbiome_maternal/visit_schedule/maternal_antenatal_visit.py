from collections import OrderedDict

from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                MembershipFormTuple, ScheduleGroupTuple)

from ..models import AntenatalEnrollment


class AntenatalEnrollmentVisitSchedule(VisitScheduleConfiguration):

    name = 'antenatal visit schedule'
    app_label = 'microbiome_maternal'

    membership_forms = OrderedDict({'antenatal': MembershipFormTuple(
        'antenatal', AntenatalEnrollment, True), })

    schedule_groups = OrderedDict({
        'Antenatal Enrollment': ScheduleGroupTuple('Antenatal Enrollment',
                                                   'antenatal', None, None), })

    visit_definitions = OrderedDict()

site_visit_schedules.register(AntenatalEnrollmentVisitSchedule)
