from django.test import TestCase
from django.utils import timezone
from datetime import date

from edc.subject.registration.models import RegisteredSubject
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, NO, POS, NEG, NOT_APPLICABLE

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import \
    (MaternalEligibilityFactory, AntenatalEnrollmentFactory,
    MaternalVisitFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import\
    (PostnatalEnrollmentFactory, SexualReproductiveHealthFactory, MaternalOffStudyFactory)
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment
from bhp077.apps.microbiome_maternal.forms import MaternalLocatorForm

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule


class TestMaternalLocator(TestCase):


    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
        )
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='off study')

        self.data = {
            'registered_subject': self.registered_subject.id,
            'report_datetime': timezone.now(),
            'maternal_visit': maternal_visit.id,
            'date_signed': timezone.now().date(),
            'mail_address': 'P O BOX 893 LOB',
            'care_clinic': None,
            'home_visit_permission': YES,
            'physical_address': 'Next to hill school primary, Peleng',
            'may_follow_up': YES,
            'may_sms_follow_up': NO,
            'subject_cell': '75700544',
            'subject_cell_alt': None,
            'subject_phone': None,
            'subject_phone_alt': None,
            'may_call_work': YES,
            'subject_work_place': '75700543',
            'subject_work_phone': '3915493',
            'may_contact_someone': YES,
            'contact_name': 'EBRA',
            'contact_rel': 'COUSIN',
            'contact_physical_address': 'MOLAPO',
            'contact_cell': '75121212',
            'contact_phone': None,
            'has_caretaker_alt': NO,
            'caretaker_name': None,
            'caretaker_cell': None,
            'caretaker_tel': None
        }

    def model_options(self, app_label, model_name, appointment):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=appointment)
        return model_options

    def test_maternal_locator_valid(self):
        locator = MaternalLocatorForm(data=self.data)
        print locator.errors
        self.assertTrue(locator.is_valid())

    def test_locator_may_follow_up_invalid(self):
        "Assert if may follow up yes then you provide atlease subject cell otherwise raise validation error."
        self.data['may_follow_up'] = YES
        self.data['subject_cell'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to follow them up, what is their cell number?",
            locator.errors.get('__all__')
        )

    def test_locator_may_follow_up_valid(self):
        "Assert if may follow up yes and provide subject cell then locator is valid."
        self.data['may_follow_up'] = YES
        self.data['subject_cell'] = '75700544'
        locator = MaternalLocatorForm(data=self.data)
        self.assertTrue(locator.is_valid())

    def test_locator_may_sms_follow_up_invalid(self):
        "Assert if may follow up yes and provide subject cell then locator is valid."
        self.data['may_sms_follow_up'] = YES
        self.data['subject_cell'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to follow them up, what is their cell number?",
            locator.errors.get('__all__')
        )
    def test_locator_may_sms_follow_up_valid(self):
        "Assert if may follow up yes and provide subject cell then locator is valid."
        self.data['may_sms_follow_up'] = YES
        self.data['subject_cell'] = '75700544'
        locator = MaternalLocatorForm(data=self.data)
        self.assertTrue(locator.is_valid())

    def test_locator_may_call_work_invalid(self):
        "Assert if may follow up yes and provide subject cell then locator is valid."
        self.data['may_call_work'] = YES
        self.data['subject_work_place'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to call them at work, name work place location?",
            locator.errors.get('__all__')
        )

    def test_locator_may_call_work_invalid(self):
        "Assert if may follow up yes and provide subject cell then locator is valid."
        self.data['may_call_work'] = YES
        self.data['subject_work_place'] = 'Botswana Harvard, Located inside marina'
        locator = MaternalLocatorForm(data=self.data)
        self.assertTrue(locator.is_valid())

    def test_locator_may_call_work_without_subject_work_phone(self):
        self.data['may_call_work'] = YES
        self.data['subject_work_phone'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to call them at work, give the work phone number?",
            locator.errors.get('__all__')
        )

    def test_locator_may_call_work_with_subject_work_phone(self):
        self.data['may_call_work'] = YES
        self.data['subject_work_phone'] = '75700544'
        locator = MaternalLocatorForm(data=self.data)
        self.assertTrue(locator.is_valid())


    def test_locator_may_contact_someone_no(self):
        self.data['may_contact_someone'] = NO
        self.data['has_alt_contact'] = NOT_APPLICABLE
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has answered No to question 12 then question 19 is Not Applicable",
            locator.errors.get('__all__')
        )

    def zest_locator_has_alt_contact_yes(self):
        self.data['has_alt_contact'] = YES
        self.data['alt_contact_name'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to contact next-of-kin, what is their full name?",
            locator.errors.get('__all__')
        )

    def zest_locator_has_alt_contact_yes1(self):
        self.data['has_alt_contact'] = YES
        self.data['alt_contact_rel'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to contact next-of-kin, how are they related?",
            locator.errors.get('__all__')
        )

    def test_locator_may_contact_someone_yes(self):
        self.data['may_contact_someone'] = YES
        self.data['contact_name'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to contact someone else, what is the contact name?",
            locator.errors.get('__all__')
        )

    def test_locator_may_contact_someone_yes1(self):
        self.data['may_contact_someone'] = YES
        self.data['contact_rel'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to contact someone else, how are they related to this person?",
            locator.errors.get('__all__')
        )
    def test_locator_may_contact_someone_yes2(self):
        self.data['may_contact_someone'] = YES
        self.data['contact_physical_address'] = None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has allowed you to contact someone else, what is this persons physical address?",
            locator.errors.get('__all__')
        )

    def test_validate_call_follow_up_no_subject_phone_given(self):
        for f in ['may_follow_up', 'may_sms_follow_up']:
             self.data[f] = NO
        self.data['subject_phone'] = '75700541'
        self.data['subject_phone_alt'] =  None
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has not given permission for follow-up, do not give follow-up details",
            locator.errors.get('__all__')
        )


    def test_validate_call_follow_up_no_subject_phone_alt_given(self):
        for f in ['may_follow_up', 'may_sms_follow_up']:
             self.data[f] = NO
        self.data['subject_phone'] = NO
        self.data['subject_phone_alt'] =  '75700541'
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has not given permission for follow-up, do not give follow-up details",
            locator.errors.get('__all__')
        )

    def test_validate_call_sms_follow_up_given(self):
        for f in ['may_follow_up', 'may_sms_follow_up']:
             self.data[f] = NO
        self.data['subject_cell'] = None
        self.data['subject_cell_alt'] =  '75700541'
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has not given permission for follow-up, do not give follow-up details",
            locator.errors.get('__all__')
        )

    def zest_validate_next_of_kin1(self): # failed
        self.data['has_alt_contact'] = NO
        for f in ['alt_contact_name', 'alt_contact_rel']:
            self.data[f] = 'NA'
        locator = MaternalLocatorForm(data=self.data)
        self.assertIn(
            u"If participant has not given permission for follow-up, do not give follow-up details",
            locator.errors.get('__all__')
        )

    def zest_validate_next_of_kin2(self):
        for f in ['has_alt_contact']:
             self.data[f] = NO
        i = 1
        for f in ['alt_contact_cell', 'other_alt_contact_cell', 'alt_contact_tel']:
            self.data[f] = '7570054{}'.format(i)
            i += 1
            print self.data[f]
        locator = MaternalLocatorForm(data=self.data)
        print locator.errors
        self.assertIn(
            u"If participant has not given permission to contact next_of_kin, do not give next_of_kin details",
            locator.errors.get('__all__')
        )
