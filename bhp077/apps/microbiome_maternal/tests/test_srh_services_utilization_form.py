from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG, NOT_APPLICABLE, SCHEDULED

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_list.models import Contraceptives

from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.forms import SrhServicesUtilizationForm

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule


class TestSrhServiceUtilizationForm(TestCase):

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
        c = Contraceptives.objects.create(
            name='Chrome chronic',
            short_name='Chrome'
        )
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': None,
            'seen_at_clinic': YES,
            'is_contraceptive_initiated': YES,
            'contraceptive_methods': [c.id],
            'reason_not_initiated': None,
            'srh_referral': YES,
            'srh_referral_other': None
        }

    def test_srh_services_utilization_form_valid(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='scheduled')

        self.data['maternal_visit'] = maternal_visit.id

        maternal_medicalHistory_form = SrhServicesUtilizationForm(data=self.data)

        self.assertTrue(maternal_medicalHistory_form.is_valid())

    def test_srh_services_utilization_form_valid1(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='scheduled')

        self.data['maternal_visit'] = maternal_visit.id

        maternal_medicalHistory_form = SrhServicesUtilizationForm(data=self.data)

        self.assertTrue(maternal_medicalHistory_form.is_valid())

    def test_srh_services_utilization_form_valid2(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='scheduled')
        self.data['seen_at_clinic'] = NO
        self.data['maternal_visit'] = maternal_visit.id

        maternal_medicalHistory_form = SrhServicesUtilizationForm(data=self.data)

        self.data['reason_unseen_clinic'] = ''

        self.assertIn(
            'If you have not been seen in that clinic since your last visit with us, why not?',
            maternal_medicalHistory_form.errors.get('__all__'))

    def test_srh_services_utilization_form_valid3(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['seen_at_clinic'] = NO
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        self.data['is_contraceptive_initiated'] = NO
        self.data['maternal_visit'] = maternal_visit.id
        contraceptives = Contraceptives.objects.create(
            name=NOT_APPLICABLE,
            short_name=NOT_APPLICABLE)
        self.data['contraceptive_methods'] = [contraceptives.id]
        form = SrhServicesUtilizationForm(data=self.data)
        self.assertIn(
            'If have not initiated contraceptive method, please provide reason.',
            form.errors.get('__all__'))

    def test_srh_services_utilization_form_valid4(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['seen_at_clinic'] = NO
        self.data['is_contraceptive_initiated'] = YES
        self.data['reason_not_initiated'] = "no_options"
        self.data['maternal_visit'] = maternal_visit.id
        maternal_medicalHistory_form = SrhServicesUtilizationForm(data=self.data)
        contraceptives = Contraceptives.objects.create(
            name='Chrome chronic1',
            short_name='chrome1')
        self.data['contraceptive_methods'] = [contraceptives.id]
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        self.assertIn("Don't answer this question, since you have initiated contraceptive.",
                      maternal_medicalHistory_form.errors.get('__all__'))
