from collections import OrderedDict

from edc.subject.visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleGroupTuple)

from ..models import MaternalVisit, PostnatalEnrollment

from .entries import (
    maternal_delivery_entries, maternal_history_entries, maternal_monthly_entries, maternal_requisition_entries)


class PostnatalEnrollmentVisitSchedule(VisitScheduleConfiguration):

    name = 'postnatal visit schedule'
    app_label = 'microbiome_maternal'

    membership_forms = OrderedDict({'postnatal': MembershipFormTuple(
        'postnatal', PostnatalEnrollment, True), })

    schedule_groups = OrderedDict({
        'Postnatal Enrollment': ScheduleGroupTuple('Postnatal Enrollment',
                                                   'postnatal', None, None), })

    visit_definitions = OrderedDict()

    visit_definitions['1000M'] = {
        'title': 'Maternal Patient History',
        'time_point': 0,
        'base_interval': 0,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Postnatal Enrollment',
        'instructions': '',
        'requisitions': maternal_requisition_entries,
        'entries': maternal_history_entries}

    visit_definitions['2000M'] = {
        'title': 'Maternal Delivery',
        'time_point': 1,
        'base_interval': 0,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Postnatal Enrollment',
        'instructions': '',
        'requisitions': maternal_requisition_entries,
        'entries': maternal_delivery_entries}

    visit_definitions['2010M'] = {
        'title': '1 Month Visit',
        'time_point': 10,
        'base_interval': 1,
        'base_interval_unit': 'M',
        'window_lower_bound': 15,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 60,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Postnatal Enrollment',
        'instructions': None,
        'requisitions': maternal_requisition_entries,
        'entries': maternal_monthly_entries}

    visit_definitions['2030M'] = {
        'title': '3 Months Visit',
        'time_point': 30,
        'base_interval': 3,
        'base_interval_unit': 'M',
        'window_lower_bound': 29,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Postnatal Enrollment',
        'instructions': None,
        'requisitions': maternal_requisition_entries,
        'entries': maternal_monthly_entries}

    visit_definitions['2060M'] = {
        'title': '6 Months Visit',
        'time_point': 60,
        'base_interval': 6,
        'base_interval_unit': 'M',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Postnatal Enrollment',
        'instructions': None,
        'requisitions': maternal_requisition_entries,
        'entries': maternal_monthly_entries}

    visit_definitions['2090M'] = {
        'title': '9 Months Visit',
        'time_point': 90,
        'base_interval': 9,
        'base_interval_unit': 'M',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Postnatal Enrollment',
        'instructions': None,
        'requisitions': maternal_requisition_entries,
        'entries': maternal_monthly_entries}

    visit_definitions['2120M'] = {
        'title': '12 Months Visit',
        'time_point': 120,
        'base_interval': 12,
        'base_interval_unit': 'M',
        'window_lower_bound': 44,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 45,
        'window_upper_bound_unit': 'D',
        'grouping': 'maternal',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Postnatal Enrollment',
        'instructions': None,
        'requisitions': maternal_requisition_entries,
        'entries': maternal_monthly_entries}

site_visit_schedules.register(PostnatalEnrollmentVisitSchedule)
