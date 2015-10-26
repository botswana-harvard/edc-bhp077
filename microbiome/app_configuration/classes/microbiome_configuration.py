from datetime import datetime, date

from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc_device import device
from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

study_start_datetime = datetime(2015, 10, 01, 7, 30, 00)
study_end_datetime = datetime(2020, 06, 30, 7, 30, 00)

try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None


class MicrobiomeConfiguration(BaseAppConfiguration):

    def prepare(self):
        super(MicrobiomeConfiguration, self).prepare()

    global_configuration = {
        'dashboard':
            {'show_not_required_metadata': False,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': True},
        'appointment':
            {'allowed_iso_weekdays': '12345',
             'use_same_weekday': True,
             'default_appt_type': 'default'}, }

    study_variables_setup = {
        'protocol_number': 'BHP071',
        'protocol_code': '071',
        'protocol_title': 'BHP071',
        'research_title': 'Gut Microbiome Evolution',
        'study_start_datetime': study_start_datetime,
        'minimum_age_of_consent': 18,
        'maximum_age_of_consent': 130,
        'gender_of_consent': 'F',
        'subject_identifier_seed': '10000',
        'subject_identifier_prefix': '000',
        'subject_identifier_modulus': '7',
        'subject_type': 'subject',
        'machine_type': 'SERVER',
        'hostname_prefix': '0000',
        'device_id': device.device_id}

    holidays_setup = {
        'New Year': date(2015, 1, 01),
        'New Year Holiday': date(2015, 1, 02),
        'Good Fiday': date(2015, 4, 3),
        'Easter Monday': date(2015, 4, 6),
        'Labour Day': date(2015, 5, 1),
        'Ascension Day': date(2015, 5, 14),
        'Sir Seretse Khama Day': date(2015, 7, 01),
        'President\'s Day': date(2015, 7, 20),
        'President\'s Day Holiday': date(2015, 7, 21),
        'Independence Day': date(2015, 9, 30),
        'Botswana Day Holiday': date(2015, 10, 01),
        'Christmas Day': date(2015, 12, 25),
        'Boxing Day': date(2015, 12, 26), }

    consent_catalogue_setup = {
        'name': 'microbiome',
        'content_type_map': 'maternaleligibility',
        'consent_type': 'study',
        'version': 1,
        'start_datetime': study_start_datetime,
        'end_datetime': study_end_datetime,
        'add_for_app': 'microbiome'}

    study_site_setup = [{'site_name': 'Gaborone', 'site_code': '001'}]

    consent_catalogue_list = [consent_catalogue_setup]

#     lab_clinic_api_setup = {
#         'panel': [],
#         'aliquot_type': []}
# 
#     lab_setup = {'microbiome': {
#         'panel': [],
#         'aliquot_type': [],
#         'profile': [],
#         'profile_item': []}}

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                  PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                  PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                  PanelTuple('Skin Flora (Storage)', 'STORAGE', 'SF'),
                  PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VSM')],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16')]}

    lab_setup = {
        'microbiome': {
            'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                      PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                      PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                      PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                      PanelTuple('Skin Flora (Storage)', 'STORAGE', 'SF'),
                      PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VSM')],
            'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                             AliquotTypeTuple('Plasma', 'PL', '32'),
                             AliquotTypeTuple('Buffy Coat', 'BC', '16')],
            'profile': [ProfileTuple('Viral Load', 'WB')],
            'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 2),
                             ProfileItemTuple('Viral Load', 'BC', 0.5, 3)]}}

    labeling_setup = {
        'label_printer': [LabelPrinterTuple
                          ('Zebra_Technologies_ZTC_GK420t', 'hostname', 'localhost', False), ],
        'client': [ClientTuple(hostname='hostname',
                               printer_name='Zebra_Technologies_ZTC_GK420t',
                               cups_hostname='hostname',
                               ip=None,
                               aliases=None), ],
        'zpl_template': [
            aliquot_label or ZplTemplateTuple(
                'aliquot_label', (
                    ('^XA\n'
                     '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
                     '${aliquot_type} ${aliquot_count}${primary}^FS\n'
                     '^FO300,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${aliquot_identifier}^FS\n'
                     '^FO300,92^A0N,20,20^FD${aliquot_identifier}^FS\n'
                     '^FO300,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO300,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO300,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                     '^XZ')), True),
            ZplTemplateTuple(
                'requisition_label', (
                    ('^XA\n'
                     '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
                     '${aliquot_type} ${aliquot_count}${primary}^FS\n'
                     '^FO300,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${requisition_identifier}^FS\n'
                     '^FO300,92^A0N,20,20^FD${requisition_identifier} ${panel}^FS\n'
                     '^FO300,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO300,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO300,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                     '^XZ')), False), ]}

    def update_or_create_study_variables(self):
        if StudySpecific.objects.all().count() == 0:
            StudySpecific.objects.create(**self.study_variables_setup)
        else:
            StudySpecific.objects.all().update(**self.study_variables_setup)
        self._setup_study_sites()

    def _setup_study_sites(self):
        for site in self.study_site_setup:
            try:
                StudySite.objects.get(**site)
            except StudySite.DoesNotExist:
                StudySite.objects.create(**site)
microbiome_configuration = MicrobiomeConfiguration()
