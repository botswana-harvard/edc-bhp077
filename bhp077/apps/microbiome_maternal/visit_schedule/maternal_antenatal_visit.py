from collections import OrderedDict

from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                EntryTuple, MembershipFormTuple,
                                                ScheduleGroupTuple, RequisitionPanelTuple)
from edc_constants.constants import REQUIRED, NOT_REQUIRED, ADDITIONAL, NOT_ADDITIONAL

from ..models import AntenatalEnrollment, MaternalVisit


class AntenatalEnrollmentVisitSchedule(VisitScheduleConfiguration):

    name = 'antenatal visit schedule'
    app_label = 'microbiome_maternal'

    membership_forms = OrderedDict({'antenatal': MembershipFormTuple(
        'antenatal', AntenatalEnrollment, True), })

    schedule_groups = OrderedDict({
        'Antenatal Enrollment': ScheduleGroupTuple('Antenatal Enrollment',
                                                   'antenatal', None, None), })

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
        'grouping': '',
        'visit_tracking_model': MaternalVisit,
        'schedule_group': 'Antenatal Enrollment',
        'instructions': '',
        'requisitions': (
            RequisitionPanelTuple(10L, u'microbiome_lab', u'maternalrequisition',
                                  'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(20L, u'microbiome_lab', u'maternalrequisition',
                                  'Breast Milk (Storage)', 'STORAGE', 'BM', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(30L, u'microbiome_lab', u'maternalrequisition',
                                  'Vaginal swab (Storage)', 'STORAGE', 'VS', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(40L, u'microbiome_lab', u'maternalrequisition',
                                  'Rectal swab (Storage)', 'STORAGE', 'RS', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(50L, u'microbiome_lab', u'maternalrequisition',
                                  'Skin Swab (Storage)', 'STORAGE', 'SW', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(60L, u'microbiome_lab', u'maternalrequisition',
                                  'Vaginal Swab (multiplex PCR)', 'TEST', 'VS', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(70L, u'microbiome_lab', u'maternalrequisition',
                                  'Hematology (ARV)', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
            RequisitionPanelTuple(80L, u'microbiome_lab', u'maternalrequisition',
                                  'CD4 (ARV)', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
        ),
        'entries': (
            EntryTuple(10L, u'microbiome_maternal', u'maternallocator', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(20L, u'microbiome_maternal', u'maternaldemographics', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(40L, u'microbiome_maternal', u'maternalmedicalhistory', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(50L, u'microbiome_maternal', u'maternalobstericalhistory', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(60L, u'microbiome_maternal', u'maternalclinicalhistory', NOT_REQUIRED, NOT_ADDITIONAL),
            EntryTuple(70L, u'microbiome_maternal', u'maternalarvhistory', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(80L, u'microbiome_maternal', u'maternalarvpreg', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(90L, u'microbiome_maternal', u'maternalbreasthealth', REQUIRED, NOT_ADDITIONAL),
            EntryTuple(200L, u'microbiome_maternal', u'maternaldeath', NOT_REQUIRED, ADDITIONAL),
            EntryTuple(210L, u'microbiome_maternal', u'maternaloffstudy', NOT_REQUIRED, ADDITIONAL), )}

site_visit_schedules.register(AntenatalEnrollmentVisitSchedule)
