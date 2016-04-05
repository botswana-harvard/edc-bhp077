from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.choices import YES, NO, POS, NOT_APPLICABLE, OTHER

from microbiome.apps.mb_maternal.forms import MaternalPostFuMedItemsForm

from .base_test_case import BaseTestCase
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory, MaternalPostFuMedFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory, MaternalPostFuFactory)


class TestMaternalPostFuMedItems(BaseTestCase):
    """Test eligibility of a mother for postnatal followup medications."""

    def setUp(self):
        super(TestMaternalPostFuMedItems, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject,
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
            'medication_other': '',
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

    def test_other_meds_1(self):
        self.data['medication'] = OTHER
        form = MaternalPostFuMedItemsForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If medication is \'OTHER\', please specify', errors)

    def test_other_meds_2(self):
        self.data['medication_other'] = 'Doxy'
        form = MaternalPostFuMedItemsForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated listed medication. You cannot specify other.', errors)
