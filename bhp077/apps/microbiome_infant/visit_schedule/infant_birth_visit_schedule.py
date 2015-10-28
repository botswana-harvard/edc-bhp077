from collections import OrderedDict

from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                EntryTuple, MembershipFormTuple, ScheduleGroupTuple,
                                                RequisitionPanelTuple)
from edc_constants.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL

from ..models import InfantVisit, InfantBirth


class InfantBirthVisitSchedule(VisitScheduleConfiguration):

    name = 'birth visit schedule'
    app_label = 'microbiome_infant'

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
            # EntryTuple(10L, u'infant', u'infantbirthdata', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(20L, u'microbiome_infant', u'infantbirthexam', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(30L, u'microbiome_infant', u'infantbirtharv', NOT_REQUIRED, ADDITIONAL),
            # EntryTuple(40L, u'infant', u'infantbirthfeed', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(100L, u'microbiome_infant', u'infantcongenitalanomalies', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(200L, u'microbiome_infant', u'infantdeath', NOT_REQUIRED, ADDITIONAL),
            # EntryTuple(210L, u'infant', u'infantverbalautopsy', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(230L, u'microbiome_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}
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
            EntryTuple(30L, u'microbiome_infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(40L, u'microbiome_infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(50L, u'microbiome_infant', u'infantfudx', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'microbiome_infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'microbiome_infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
            # EntryTuple(120L, u'infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            # EntryTuple(120L, u'infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(200L, u'microbiome_infant', u'infantdeath', NOT_REQUIRED, ADDITIONAL),
            # EntryTuple(210L, u'infant', u'infantverbalautopsy', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(240L, u'microbiome_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}
    visit_definitions['2030'] = {
        'title': 'Infant 3 Month Visit',
        'time_point': 30,
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
            EntryTuple(30L, u'microbiome_infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(40L, u'microbiome_infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(50L, u'microbiome_infant', u'infantfudx', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'microbiome_infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'microbiome_infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
            # EntryTuple(120L, u'infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            # EntryTuple(120L, u'infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(200L, u'microbiome_infant', u'infantdeath', NOT_REQUIRED, ADDITIONAL),
            # EntryTuple(210L, u'infant', u'infantverbalautopsy', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(240L, u'microbiome_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL))}

site_visit_schedules.register(InfantBirthVisitSchedule)
