from collections import OrderedDict

from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                EntryTuple, MembershipFormTuple,
                                                ScheduleGroupTuple, RequisitionPanelTuple)
from edc_constants.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL

from ..models import MaternalVisit, PostnatalEnrollment


class MaternalDeliveryVisitSchedule(VisitScheduleConfiguration):

    name = 'delivery visit schedule'
    app_label = 'microbiome'

    membership_forms = OrderedDict({'postnatal': MembershipFormTuple(
        'postnatal', PostnatalEnrollment, True), })

    schedule_groups = OrderedDict({
        'delivery': ScheduleGroupTuple(
            'delivery', 'postnatal', '', None), })

    visit_definitions = OrderedDict(
        {'2000M': {
            'title': 'Maternal Delivery',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': 'maternal',
            'visit_tracking_model': MaternalVisit,
            'schedule_group': 'delivery',
            'instructions': '',
            'requisitions': (
#                 RequisitionPanelTuple(100L, u'microbiome', u'maternalrequisition',
#                                       'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
#                 RequisitionPanelTuple(200L, u'microbiome', u'maternalrequisition',
#                                       'Breast Milk (Storage)', 'STORAGE', 'BM', REQUIRED, NOT_ADDITIONAL),
#                 RequisitionPanelTuple(300L, u'microbiome', u'maternalrequisition',
#                                       'Vaginal swab (Storage)', 'STORAGE', 'VS', REQUIRED, NOT_ADDITIONAL),
#                 RequisitionPanelTuple(400L, u'microbiome', u'maternalrequisition',
#                                       'Rectal swab (Storage)', 'STORAGE', 'RS', REQUIRED, NOT_ADDITIONAL),
#                 RequisitionPanelTuple(500L, u'microbiome', u'maternalrequisition',
#                                       'Skin Flora (Storage)', 'STORAGE', 'SF', REQUIRED, NOT_ADDITIONAL),
#                 RequisitionPanelTuple(600L, u'microbiome', u'maternalrequisition',
#                                       'Vaginal Swab (multiplex PCR)', 'TEST', 'VSM', REQUIRED, NOT_ADDITIONAL)
                ),
            'entries': (
                EntryTuple(10L, u'maternal', u'maternallabourdel', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(20L, u'maternal', u'maternallabdelmed', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(30L, u'maternal', u'maternallabdelclinic', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(40L, u'maternal', u'maternallabdeldx', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(50L, u'maternal', u'maternallabdeldxt', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(60L, u'maternal', u'maternalarvpreg', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(70L, u'maternal', u'maternalarv', REQUIRED, NOT_ADDITIONAL),
                # EntryTuple(200L, u'microbiome', u'maternaldeath', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(210L, u'maternal', u'maternaloffstudy', NOT_REQUIRED, ADDITIONAL), )}}
    )
site_visit_schedules.register(MaternalDeliveryVisitSchedule)
