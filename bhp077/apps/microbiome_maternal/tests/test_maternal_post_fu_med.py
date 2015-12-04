from django.test import TestCase
from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.code_lists.models import WcsDxAdult
from edc_constants.choices import YES, NO

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_list.models.chronic_conditions import ChronicConditions
from bhp077.apps.microbiome_maternal.forms import (MaternalPostFuMedForm, MaternalPostFuMedItemsForm)

from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory, MaternalPostFuFactory)
from bhp077.apps.microbiome_maternal.tests.factories.maternal_postnatal_fu_factory import MaternalPostFuMedFactory


class TestMaternalPostFuMedItems(TestCase):
    """Test eligibility of a mother for postnatal followup medications."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
                                                       study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
#         self.chronic_cond = ChronicConditions.objects.create(name='N/A', short_name='N/A', display_index=10,
#                                                              field_name='chronic_cond')
        self.post_fu = MaternalPostFuFactory(maternal_visit=self.maternal_visit)
        self.post_fu_med = MaternalPostFuMedFactory(maternal_post_fu=self.post_fu, has_taken_meds=YES)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'maternal_post_fu_med': self.post_fu_med.id,
            'date_first_medication': timezone.now() - timezone.timedelta(days=1),
            'medication': 'Amoxicillin',
            'drug_route': "1",
            'date_stoped': timezone.now()
        }

    def test_date(self):
        form = MaternalPostFuMedItemsForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Date stopped medication is before date started medications. Please correct", errors)
