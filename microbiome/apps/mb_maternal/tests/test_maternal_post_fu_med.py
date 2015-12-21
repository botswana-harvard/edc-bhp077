from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.subject.appointment.models import Appointment
from edc_constants.choices import YES, NO, POS, NOT_APPLICABLE

from microbiome.apps.mb_maternal.forms import MaternalPostFuMedItemsForm

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory, MaternalPostFuMedFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory, MaternalPostFuFactory)


class TestMaternalPostFuMedItems(BaseMaternalTestCase):
    """Test eligibility of a mother for postnatal followup medications."""

    def setUp(self):
        super(TestMaternalPostFuMedItems, self).setUp()
        self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
                                                       study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2010M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.post_fu = MaternalPostFuFactory(maternal_visit=self.maternal_visit)
        self.post_fu_med = MaternalPostFuMedFactory(maternal_visit=self.maternal_visit, has_taken_meds=YES)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'maternal_post_fu_med': self.post_fu_med.id,
            'date_first_medication': timezone.now() - timezone.timedelta(days=2),
            'medication': 'Amoxicillin',
            'drug_route': "1",
            'date_stoped': timezone.now()
        }

    def test_medications(self):
        self.post_fu_med.has_taken_meds = NO
        self.post_fu_med.save()
        form = MaternalPostFuMedItemsForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('therefore you cannot provide medication', errors)

    def test_date(self):
        self.data['date_stoped'] = timezone.now() - timezone.timedelta(days=5)
        form = MaternalPostFuMedItemsForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Date stopped medication is before date started medications.', errors)
