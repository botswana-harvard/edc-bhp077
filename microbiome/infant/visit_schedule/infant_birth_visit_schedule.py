from collections import OrderedDict

from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                EntryTuple, MembershipFormTuple, ScheduleGroupTuple,
                                                RequisitionPanelTuple)
from edc_constants.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL

from ..models import InfantVisit, InfantBirth


class InfantBirthVisitSchedule(VisitScheduleConfiguration):

    name = 'birth visit schedule'
    app_label = 'infant'

    membership_forms = OrderedDict({
        'infant_birth_record': MembershipFormTuple('infant_birth_record', InfantBirth, True)})

    schedule_groups = OrderedDict({
        'Infant Birth': ScheduleGroupTuple('Infant Birth', 'infant_birth_record', None, None)})

    visit_definitions = OrderedDict()
    visit_definitions['2000'] = {
        'title': 'Birth',
        'time_point': 0,
        'base_interval': 0,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'infant',
        'visit_tracking_model': InfantVisit,
        'schedule_group': 'Infant Birth',
        'instructions': None,
        'requisitions': (
            RequisitionPanelTuple(300L, u'microbiome_lab', u'infantrequisition',
                                  'DNA PCR', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(400L, u'microbiome_lab', u'infantrequisition',
                                  'Stool storage', 'STORAGE', 'ST', NOT_REQUIRED, ADDITIONAL)),
        'entries': (
            EntryTuple(20L, u'infant', u'infantbirthexam', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(30L, u'infant', u'infantbirtharv', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(100L, u'infant', u'infantcongenitalanomalies', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(200L, u'infant', u'infantdeath', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(230L, u'infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}
    visit_definitions['2010'] = {
        'title': 'Infant 1 Month Visit',
        'time_point': 10,
        'base_interval': 27,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'infant',
        'visit_tracking_model': InfantVisit,
        'schedule_group': 'Infant Birth',
        'instructions': None,
        'requisitions': (
            RequisitionPanelTuple(300L, u'microbiome_lab', u'infantrequisition',
                                  'DNA PCR', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(400L, u'microbiome_lab', u'infantrequisition',
                                  'Stool storage', 'STORAGE', 'ST', NOT_REQUIRED, ADDITIONAL)),
        'entries': (
            EntryTuple(30L, u'infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(40L, u'infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(50L, u'infant', u'infantfudx', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(200L, u'infant', u'infantdeath', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(240L, u'infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}

site_visit_schedules.register(InfantBirthVisitSchedule)
