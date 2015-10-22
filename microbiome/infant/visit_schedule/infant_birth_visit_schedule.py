from collections import OrderedDict

from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules, EntryTuple, MembershipFormTuple, ScheduleGroupTuple, RequisitionPanelTuple
from edc.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL

from ..models import InfantVisit, InfantBirth


class InfantBirthVisitSchedule(VisitScheduleConfiguration):

    name = 'birth visit schedule'
    app_label = 'infant'
    # membership forms
    # (name, model, visible)
    membership_forms = OrderedDict({
        'infant_birth_record': MembershipFormTuple('infant_birth_record', InfantBirth, True),
    })

    # schedule groups
    # (name, membership_form_name, grouping_key, comment)
    schedule_groups = OrderedDict({
        'Infant Birth': ScheduleGroupTuple('Infant Birth', 'infant_birth_record', None, None),
    })

    # visit_schedule
    # see edc.subject.visit_schedule.models.visit_defintion
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
            # (entry_order, app_label, model_name, requisition_panel_name, panel_type, aliquot_type_alpha_code, form_visible)
            RequisitionPanelTuple(300L, u'mpepu_lab', u'infantrequisition',
                                  'DNA PCR', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(400L, u'mpepu_lab', u'infantrequisition',
                                  'Stool storage', 'STORAGE', 'ST', NOT_REQUIRED, ADDITIONAL),
        ),
        'entries': (
            EntryTuple(10L, u'mpepu_infant', u'infantbirthdata', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(20L, u'mpepu_infant', u'infantbirthexam', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(30L, u'mpepu_infant', u'infantbirtharv', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(40L, u'mpepu_infant', u'infantbirthfeed', NOT_REQUIRED, ADDITIONAL),
            # following are additional forms
            EntryTuple(100L, u'mpepu_infant', u'infantcongenitalanomalies', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(200L, u'mpepu_infant', u'infantdeath', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(201L, u'mpepu_infant', u'infantsurvival', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(210L, u'mpepu_infant', u'infantverbalautopsy', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(220L, u'mpepu_infant', u'infantprerandoloss', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(230L, u'mpepu_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL),
        )}
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
            # (entry_order, app_label, model_name, panel.name, panel.edc_name, panel.panel_type, aliquot_type)
            RequisitionPanelTuple(300L, u'mpepu_lab', u'infantrequisition',
                                  'DNA PCR', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(400L, u'mpepu_lab', u'infantrequisition',
                                  'Stool storage', 'STORAGE', 'ST', NOT_REQUIRED, ADDITIONAL),
        ),
        'entries': (
            EntryTuple(30L, u'infant', u'infantfu', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(40L, u'infant', u'infantfuphysical', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(50L, u'infant', u'infantfudx', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'infant', u'infantfunewmed', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(80L, u'infant', u'infantfuimmunizations', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(120L, u'infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(120L, u'infant', u'infantfeeding', REQUIRED, NOT_ADDITIONAL),

            # following are additional forms
            EntryTuple(200L, u'mpepu_infant', u'infantdeath', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(201L, u'mpepu_infant', u'infantsurvival', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(210L, u'mpepu_infant', u'infantverbalautopsy', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(230L, u'mpepu_infant', u'infantoffdrug', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(240L, u'mpepu_infant', u'infantoffstudy', NOT_REQUIRED, ADDITIONAL),
        )}

site_visit_schedules.register(InfantBirthVisitSchedule)
