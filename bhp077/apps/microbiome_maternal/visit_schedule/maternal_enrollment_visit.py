from collections import OrderedDict

from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                EntryTuple, MembershipFormTuple,
                                                ScheduleGroupTuple, RequisitionPanelTuple)
from edc_constants.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL

from ..models import MaternalVisit, AntenatalEnrollment, PostnatalEnrollment


class AntenatalEnrollmentVisitSchedule(VisitScheduleConfiguration):

    name = 'antenatal visit schedule'
    app_label = 'microbiome_maternal'

    membership_forms = OrderedDict({'antenatal': MembershipFormTuple(
        'antenatal', AntenatalEnrollment, True), })

    schedule_groups = OrderedDict({
        'Antenatal Enrollment': ScheduleGroupTuple(
            'Antenatal Enrollment', 'antenatal', '', None), })

    visit_definitions = OrderedDict()

site_visit_schedules.register(AntenatalEnrollmentVisitSchedule)


class PostnatalEnrollmentVisitSchedule(VisitScheduleConfiguration):

    name = 'postnatal visit schedule'
    app_label = 'microbiome_maternal'

    membership_forms = OrderedDict({'postnatal': MembershipFormTuple(
        'postnatal', PostnatalEnrollment, True), })

    schedule_groups = OrderedDict({
        'Postnatal Enrollment': ScheduleGroupTuple('Postnatal Enrollment',
                                                   'postnatal', '', None), })

    visit_definitions = OrderedDict(
        {'1000M': {
            'title': 'Maternal Postnatal Enrollment',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': '',
            'visit_tracking_model': MaternalVisit,
            'schedule_group': 'Postnatal Enrollment',
            'instructions': '',
            'requisitions': (),
            'entries': (
                EntryTuple(10L, u'microbiome_maternal', u'maternallocator', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(20L, u'microbiome_maternal', u'maternaldemographics', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(30L, u'microbiome_maternal', u'maternalmedicalhistory', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(40L, u'microbiome_maternal', u'maternalobstericalhistory', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(50L, u'microbiome_maternal', u'maternalclinicalhistory', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(60L, u'microbiome_maternal', u'maternalarvhistory', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(70L, u'microbiome_maternal', u'maternalarvpreg', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(200L, u'microbiome_maternal', u'maternaldeath', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(210L, u'microbiome_maternal', u'maternaloffstudy', NOT_REQUIRED, ADDITIONAL), )}}
    )
site_visit_schedules.register(PostnatalEnrollmentVisitSchedule)
