from django.test import TestCase
from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantVisit
from bhp077.apps.microbiome_infant.forms import InfantBirthArvForm

from edc.subject.registration.models import RegisteredSubject
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, NO, POS, NEG, NOT_REQUIRED

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory, AntenatalEnrollmentFactory,
    MaternalVisitFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory, SexualReproductiveHealthFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment

from bhp077.apps.microbiome_maternal.visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_infant.tests.factories import \
    (InfantBirthFactory, InfantBirthDataFactory, InfantVisitFactory, InfantBirthFeedVaccineFactory)
from bhp077.apps.microbiome_infant.models import InfantBirth


class TestInfantBirthArv(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
            site_lab_profiles.register(InfantProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        InfantBirthVisitSchedule().build()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier
        )
        self.infant_birth = InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
        )
        self.appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000'
        )
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_birth': self.infant_birth.id,
            'infant_visit': self.infant_visit.id,
            'azt_after_birth': YES,
            'azt_dose_date': timezone.now().date(),
            'azt_additional_dose': YES,
            'sdnvp_after_birth': YES,
            'nvp_dose_date': timezone.now().date(),
            'additional_nvp_doses': YES,
            'nvp_discharge_supply': YES,
        }

    def test_validate_azt_after_birth_azt_dose_date_empty(self):
        del self.data['azt_dose_date']
        infant_birth_arv = InfantBirthArvForm(data=self.data)
        self.assertIn(u'Provide date of the first dose for AZT.', infant_birth_arv.errors.get('__all__'))

    def test_validate_azt_additional_dose(self):
        self.data['azt_additional_dose'] = 'N/A'
        infant_birth_arv = InfantBirthArvForm(data=self.data)
        self.assertIn(u'Do not select Not applicatable for Q6 if Q4 answer was yes.', infant_birth_arv.errors.get('__all__'))

    def test_validate_sdnvp_after_birth(self):
        del self.data['nvp_dose_date']
        infant_birth_arv = InfantBirthArvForm(data=self.data)
        self.assertIn(u'If infant has received single dose NVP then provide NVP date.', infant_birth_arv.errors.get('__all__'))

    def test_validate_sdnvp_after_birth_breastfeeding(self):
        InfantBirthFeedVaccineFactory(infant_visit=self.infant_visit, feeding_after_delivery='Breastfeeding only')
        self.data['nvp_discharge_supply'] = 'N/A'
        infant_birth_arv = InfantBirthArvForm(data=self.data)
        self.assertIn(u'If the infant is breast feeding then do not select not applicaticable for Q11.', infant_birth_arv.errors.get('__all__'))
