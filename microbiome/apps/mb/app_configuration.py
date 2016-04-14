from datetime import datetime, date

from edc_lab.lab_packing.models import DestinationTuple
from edc_lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc_configuration.base_app_configuration import BaseAppConfiguration
from edc_device import Device

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from .constants import MIN_AGE_OF_CONSENT

try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2015, 12, 1, 0, 0, 0)
study_end_datetime = datetime(2016, 12, 1, 0, 0, 0)


class AppConfiguration(BaseAppConfiguration):

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': True},
        'appointment':
            {'allowed_iso_weekdays': ('12345', False),
             'use_same_weekday': True,
             'default_appt_type': 'clinic',
             'appointments_per_day_max': 20,
             'appointments_days_forward': 15},
        'protocol': {
            'start_datetime': study_start_datetime,
            'end_datetime': study_end_datetime},
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
        'device_id': Device().device_id}

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
         'end_datetime': datetime(2016, 4, 13, 23, 59),
         'version': '1'},
        {'app_label': 'mb_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': datetime(2016, 4, 14),
         'end_datetime': study_end_datetime,
         'version': '2'}
    ]

    study_site_setup = []

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Breast Milk (Storage)', 'STORAGE', 'BM'),
                  PanelTuple('Vaginal swab (Storage)', 'STORAGE', 'VS'),
                  PanelTuple('Rectal swab (Storage)', 'STORAGE', 'RS'),
                  PanelTuple('Skin Swab (Storage)', 'STORAGE', 'SW'),
                  PanelTuple('Vaginal STI Swab (Storage)', 'TEST', 'VS'),
                  PanelTuple('DNA PCR', 'TEST', 'WB'),
                  PanelTuple('PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                  PanelTuple('Stool storage', 'STORAGE', 'ST'),
                  PanelTuple('Inflammatory Cytokines', 'STORAGE', 'WB'),
                  PanelTuple('Hematology (ARV)', 'TEST', 'WB'),
                  PanelTuple('CD4/ CD8', 'TEST', 'WB'),
                  PanelTuple('Chemistry', 'TEST', 'WB')],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Serum', 'SERUM', '06'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                         AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                         AliquotTypeTuple('Breast Milk: Fluid', 'BMF', '21'),
                         AliquotTypeTuple('Breast Milk: Pellet', 'BMP', '22'),
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
                           PanelTuple('Vaginal STI Swab (Storage)', 'TEST', 'VS'),
                           PanelTuple('DNA PCR', 'TEST', 'WB'),
                           PanelTuple('PBMC Plasma (STORE ONLY)', 'STORAGE', 'WB'),
                           PanelTuple('Stool storage', 'STORAGE', 'ST'),
                           PanelTuple('Inflammatory Cytokines', 'STORAGE', 'WB'),
                           PanelTuple('Hematology (ARV)', 'TEST', 'WB'),
                           PanelTuple('CD4/ CD8', 'TEST', 'WB'),
                           PanelTuple('Chemistry', 'TEST', 'WB')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Serum', 'SERUM', '06'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                                  AliquotTypeTuple('Breast Milk: Whole', 'BM', '20'),
                                  AliquotTypeTuple('Breast Milk: Fluid', 'BMF', '21'),
                                  AliquotTypeTuple('Breast Milk: Pellet', 'BMP', '22'),
                                  AliquotTypeTuple('Vaginal swab', 'VS', '61'),
                                  AliquotTypeTuple('Rectal swab', 'RS', '62'),
                                  AliquotTypeTuple('Skin Swab', 'SW', '63'),
                                  AliquotTypeTuple('Stool', 'ST', '01')],
                 'profile': [ProfileTuple('Viral Load', 'WB'),
                             ProfileTuple('Stool', 'ST'),
                             ProfileTuple('Breast Milk (Storage)', 'BM')],
                 'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                  ProfileItemTuple('Viral Load', 'BC', 0.5, 1),
                                  ProfileItemTuple('Stool', 'ST', 1, 1),
                                  ProfileItemTuple('Breast Milk (Storage)', 'BM', 2, 3),
                                  ProfileItemTuple('Breast Milk (Storage)', 'BMF', 2, 5),
                                  ProfileItemTuple('Breast Milk (Storage)', 'BMP', 1, 2)]}}

    labeling_setup = {
        'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t',
                                            'mpepu02', '192.168.1.230', True),
                          LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t',
                                            'kseamolo', '192.168.1.225', True)],
        'client': [
            ClientTuple(
                hostname='mpepu02',
                printer_name='Zebra_Technologies_ZTC_GK420t',
                cups_hostname='mpepu02',
                ip='192.168.1.230',
                aliases=None),
            ClientTuple(
                hostname='kseamolo',
                printer_name='Zebra_Technologies_ZTC_GK420t',
                cups_hostname='kseamolo',
                ip='192.168.1.225',
                aliases=None)],
        'zpl_template': [
            aliquot_label or ZplTemplateTuple(
                'aliquot_label', (
                    ('^XA\n' +
                     ('^FO315,15^A0N,17,20^FD${protocol} Site ${site} ${clinician_initials}   '
                      '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
                     '^FO320,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${aliquot_identifier}^FS\n'
                     '^FO315,92^A0N,18,20^FD${aliquot_identifier}^FS\n'
                     '^FO315,109^A0N,16,20^FD${panel}^FS\n'
                     '^FO315,125^A0N,19,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO315,145^A0N,18,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO315,165^A0N,18,20^FD${drawn_datetime}^FS\n'
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
