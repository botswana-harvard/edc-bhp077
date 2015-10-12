from collections import OrderedDict
from datetime import datetime, date
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.lab.lab_packing.models import DestinationTuple
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc_consent.models import ConsentType
from edc_device import device

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2015, 10, 1, 0, 0, 0)
study_end_datetime = datetime(2016, 10, 31, 17, 0, 0)


class MicrobiomeConfiguration(BaseAppConfiguration):

    def prepare(self):
        super(MicrobiomeConfiguration, self).prepare()

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': False},
        'appointment':
            {'allowed_iso_weekdays': '12345',
             'use_same_weekday': True,
             'default_appt_type': 'home',
             'appointments_per_day_max': 20,
             'appointments_days_forward': 15},
    }

    study_variables_setup = {
        'protocol_number': 'BHP071',
        'protocol_code': '071',
        'protocol_title': 'Microbiome',
        'research_title': 'Gut Microbiome Evolution',
        'study_start_datetime': study_start_datetime,
        'minimum_age_of_consent': 16,
        'maximum_age_of_consent': 100,
        'gender_of_consent': 'F',
        'subject_identifier_seed': '10000',
        'subject_identifier_prefix': '071',
        'subject_identifier_modulus': '7',
        'subject_type': 'subject',
        'machine_type': 'SERVER',
        'hostname_prefix': 's030',
        'device_id': device.device_id}

    holidays_setup = {
        'New Year': date(2015, 1, 1),
        'New Year Holiday': date(2015, 1, 2),
        'Good Fiday': date(2015, 4, 3),
        'Easter Monday': date(2015, 4, 6),
        'Labour Day': date(2015, 5, 1),
        'Ascension Day': date(2015, 5, 14),
        'Sir Seretse Khama Day': date(2015, 7, 1),
        'President\'s Day': date(2015, 7, 20),
        'President\'s Day Holiday': date(2015, 7, 21),
        'Independence Day': date(2015, 9, 30),
        'Botswana Day Holiday': date(2015, 10, 1),
        'Christmas Day': date(2015, 12, 25),
        'Boxing Day': date(2015, 12, 26),
    }

    study_site_setup = [{'site_name': 'Gaborone', 'site_code': '001'},
                        {'site_name': 'site2', 'site_code': '002'}, ]

    consent_catalogue_setup = {
        'name': 'microbiome',
        'content_type_map': 'maternalconsent',
        'consent_type': 'study',
        'version': 1,
        'start_datetime': study_start_datetime,
        'end_datetime': study_end_datetime,
        'add_for_app': 'microbiome'}

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                  PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                  PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                  PanelTuple('Skin Flora (Storage)', 'STORAGE', 'WB'),
                  PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VSM'),
                  PanelTuple('Stool (storage)', 'STORAGE', 'ST')],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                         AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                         AliquotTypeTuple('Stool', 'ST', '01')]}

    lab_setup = {'microbiome': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                           PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                           PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                           PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                           PanelTuple('Skin Flora (Storage)', 'STORAGE', 'WB'),
                           PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VSM'),
                           PanelTuple('Stool (storage)', 'STORAGE', 'ST')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                                  AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                                  AliquotTypeTuple('Stool', 'ST', '01')],
                 'profile': [ProfileTuple('Viral Load', 'WB'),
                             ProfileTuple('Vaginal swab', 'VS'), ],
                 'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                  ProfileItemTuple('Viral Load', 'BC', 0.5, 1), ]}}

    labeling_setup = {'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t',
                                                          'localhost', '127.0.0.1', True), ],
                      'client': [ClientTuple(hostname='bcpplab1',
                                             printer_name='Zebra_Technologies_ZTC_GK420t',
                                             cups_hostname='bcpplab1',
                                             ip=None,
                                             aliases=None), ],
                      'zpl_template': [
                          aliquot_label or ZplTemplateTuple(
                              'aliquot_label', (
                                  ('^XA\n'
                                   '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} ${aliquot_count}${primary}^FS\n'
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
                                   '^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} ${aliquot_count}${primary}^FS\n'
                                   '^FO300,34^BY1,3.0^BCN,50,N,N,N\n'
                                   '^BY^FD${requisition_identifier}^FS\n'
                                   '^FO300,92^A0N,20,20^FD${requisition_identifier} ${panel}^FS\n'
                                   '^FO300,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                                   '^FO300,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                                   '^FO300,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                                   '^XZ')), False), ]
                      }

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
