from datetime import datetime, date

from edc.apps.app_configuration.classes import BaseAppConfiguration
from edc_device import device
from edc.lab.lab_packing.models import DestinationTuple
from edc.lab.lab_profile.classes import ProfileItemTuple, ProfileTuple

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from ...constants import MIN_AGE_OF_CONSENT

try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2013, 10, 18, 0, 0, 0)
study_end_datetime = datetime(2016, 10, 17, 23, 0, 0)


class MicrobiomeConfiguration(BaseAppConfiguration):

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': True},
        'appointment':
            {'allowed_iso_weekdays': '12345',
             'use_same_weekday': True,
             'default_appt_type': 'clinic',
             'appointments_per_day_max': 20,
             'appointments_days_forward': 15},
    }

    study_variables_setup = {
        'protocol_number': 'BHP077',
        'protocol_code': '077',
        'protocol_title': 'BHP077',
        'research_title': 'Gut Microbiome Evolution',
        'study_start_datetime': study_start_datetime,
        'minimum_age_of_consent': MIN_AGE_OF_CONSENT,
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
        'New Year': date(2016, 1, 1),
        'New Year Holiday': date(2016, 1, 2),
        'Good Friday': date(2016, 3, 25),
        'Easter Monday': date(2016, 3, 28),
        'Labour Day': date(2016, 5, 1),
        'Labour Day Holiday': date(2016, 5, 2),
        'Ascension Day': date(2016, 5, 5),
        'Sir Seretse Khama Day': date(2016, 7, 1),
        'President\'s Day': date(2016, 7, 18),
        'President\'s Day Holiday': date(2016, 7, 19),
        'Independence Day': date(2016, 9, 30),
        'Botswana Day Holiday': date(2016, 10, 1),
        'Christmas Day': date(2015, 12, 25),
        'Boxing Day': date(2015, 12, 26)}

    consent_type_setup = [
        {'app_label': 'mb_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'version': '1'}]

    study_site_setup = [{'site_name': 'Gaborone', 'site_code': '40'},
                        {'site_name': 'Mogoditshane', 'site_code': '50'}]

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                  PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                  PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                  PanelTuple('Skin Swab (Storage)', 'STORAGE', 'SW'),
                  PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VS'),
                  PanelTuple('DNA PCR', 'TEST', 'WB'),
                  PanelTuple('PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                  PanelTuple('Stool storage', 'STORAGE', 'ST'),
                  PanelTuple('ELISA', 'TEST', 'WB'),
                  PanelTuple('Hematology (ARV)', 'TEST', 'WB'),
                  PanelTuple('CD4 (ARV)', 'TEST', 'WB'),
                  PanelTuple('Chemistry', 'TEST', 'WB')],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Serum', 'SERUM', '06'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                         AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                         AliquotTypeTuple('Vaginal swab', 'VS', '61'),
                         AliquotTypeTuple('Rectal swab', 'RS', '62'),
                         AliquotTypeTuple('Skin Swab', 'SW', '63'),
                         AliquotTypeTuple('Stool', 'ST', '01')]}

    lab_setup = {'microbiome': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                           PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                           PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                           PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                           PanelTuple('Skin Swab (Storage)', 'STORAGE', 'SW'),
                           PanelTuple('Vaginal Swab (multiplex PCR)', 'TEST', 'VS'),
                           PanelTuple('DNA PCR', 'TEST', 'WB'),
                           PanelTuple('PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                           PanelTuple('Stool storage', 'STORAGE', 'ST'),
                           PanelTuple('ELISA', 'TEST', 'WB'),
                           PanelTuple('Hematology (ARV)', 'TEST', 'WB'),
                           PanelTuple('CD4 (ARV)', 'TEST', 'WB'),
                           PanelTuple('Chemistry', 'TEST', 'WB')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Serum', 'SERUM', '06'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                                  AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                                  AliquotTypeTuple('Vaginal swab', 'VS', '61'),
                                  AliquotTypeTuple('Rectal swab', 'RS', '62'),
                                  AliquotTypeTuple('Skin Swab', 'SW', '63'),
                                  AliquotTypeTuple('Stool', 'ST', '01')],
                 'profile': [ProfileTuple('Viral Load', 'WB'),
                             ProfileTuple('Stool', 'ST')],
                 'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                  ProfileItemTuple('Viral Load', 'BC', 0.5, 1),
                                  ProfileItemTuple('Stool', 'ST', 1, 1)]}}

    labeling_setup = {
        'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t',
                                            'localhost', '127.0.0.1', True)],
        'client': [
            ClientTuple(
                hostname='localhost',
                printer_name='Zebra_Technologies_ZTC_GK420t',
                cups_hostname='localhost',
                ip=None,
                aliases=None)],
        'zpl_template': [
            aliquot_label or ZplTemplateTuple(
                'aliquot_label', (
                    ('^XA\n' +
                     ('^FO300,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
                      '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
                     '^FO300,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${aliquot_identifier}^FS\n'
                     '^FO300,92^A0N,20,20^FD${aliquot_identifier}^FS\n'
                     '^FO300,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO300,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO300,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                     '^XZ')), False),
            ZplTemplateTuple(
                'requisition_label', (
                    ('^XA\n' +
                     ('^FO310,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
                      '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
                     '^FO310,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${requisition_identifier}^FS\n'
                     '^FO310,92^A0N,20,20^FD${requisition_identifier} ${panel}^FS\n'
                     '^FO310,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO310,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO310,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                     '^XZ')), True)]
    }

microbiome_configuration = MicrobiomeConfiguration()
