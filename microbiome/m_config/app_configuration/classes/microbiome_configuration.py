from datetime import datetime, date
from django.conf import settings

from edc.core.bhp_variables.models import StudySpecific, StudySite

from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc_device import device
from edc.lab.lab_packing.models import DestinationTuple
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc_consent.models import ConsentType

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2013, 10, 18, 0, 0, 0)
study_end_datetime = datetime(2016, 10, 17, 23, 0, 0)


class MicrobiomeConfiguration(BaseAppConfiguration):

    def prepare(self):
        self.update_or_create_consent_type()
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
        'Boxing Day': date(2015, 12, 26)}

    consent_type_setup = [
        {'app_label': 'maternal',
         'model_name': 'postnatalenrollment',
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'version': '1'}]

    consent_catalogue_setup = {
        'name': 'microbiome',
        'content_type_map': 'postnatalenrollment',
        'consent_type': 'study',
        'version': 1,
        'start_datetime': study_start_datetime,
        'end_datetime': study_end_datetime,
        'add_for_app': 'maternal'}

    study_site_setup = [{'site_name': 'Gaborone', 'site_code': '001'}]

    consent_catalogue_list = [consent_catalogue_setup]

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                  PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                  PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                  PanelTuple('Skin Flora (Storage)', 'STORAGE', 'SF'),
                  PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VM'),
                  PanelTuple('DNA PCR', 'TEST', 'WB'),
                  PanelTuple('Stool storage', 'STORAGE', 'ST')],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                         AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                         AliquotTypeTuple('Vaginal swab', 'VS', '10'),
                         AliquotTypeTuple('Rectal swab', 'RS', '12'),
                         AliquotTypeTuple('Skin Flora', 'SF', '11'),
                         AliquotTypeTuple('Vaginal swab multiplex', 'VM', '13'),
                         AliquotTypeTuple('Stool', 'ST', '01')]}

    lab_setup = {'microbiome': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                           PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                           PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                           PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                           PanelTuple('Skin Flora (Storage)', 'STORAGE', 'SF'),
                           PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VM'),
                           PanelTuple('DNA PCR', 'TEST', 'WB'),
                           PanelTuple('Stool storage', 'STORAGE', 'ST')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                                  AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                                  AliquotTypeTuple('Vaginal swab', 'VS', '10'),
                                  AliquotTypeTuple('Rectal swab', 'RS', '12'),
                                  AliquotTypeTuple('Skin Flora', 'SF', '11'),
                                  AliquotTypeTuple('Vaginal swab multiplex', 'VM', '13'),
                                  AliquotTypeTuple('Stool', 'ST', '01')],
                 'profile': [ProfileTuple('Viral Load', 'WB')],
                 'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                  ProfileItemTuple('Viral Load', 'BC', 0.5, 1)]}}

    labeling_setup = {'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t', 'localhost', '127.0.0.1', True)],
                      'client': [ClientTuple(hostname='localhost',
                                             printer_name='Zebra_Technologies_ZTC_GK420t',
                                             cups_hostname='localhost',
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
                                   '^XZ')), False)]
                      }

    def update_or_create_consent_type(self):
        for item in self.consent_type_setup:
            try:
                consent_type = ConsentType.objects.get(
                    version=item.get('version'),
                    app_label=item.get('app_label'),
                    model_name=item.get('model_name'))
                consent_type.start_datetime = item.get('start_datetime')
                consent_type.end_datetime = item.get('end_datetime')
                consent_type.save()
            except ConsentType.DoesNotExist:
                ConsentType.objects.create(**item)

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
