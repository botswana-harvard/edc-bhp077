from django.test import TestCase
from django.utils import timezone

from edc.subject.registration.models import RegisteredSubject
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, NO, POS, NEG, NOT_REQUIRED

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory,
                                                             AntenatalEnrollmentFactory,
                                                             MaternalVisitFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import (
        PostnatalEnrollmentFactory, SexualReproductiveHealthFactory
    )
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule


class TestRuleGroup(TestCase):

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

    def model_options(self, app_label, model_name, appointment):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=appointment)
        return model_options

    def test_hiv_status_pos_on_postnatal_enrollment(self):
        """
        """
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            breastfeed_for_a_year=YES,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            valid_regimen=YES,
        )
        visit_codes = [
            ['1000M', ['maternalarvhistory', 'maternalarvpreg']],
#             ['2000M', ['maternalarvpreg', 'maternalarv', 'maternallabdelclinic']],
#             ['2010M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2030M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2060M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2090M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2120M', ['maternalarvpost', 'maternalarvpostadh']],
        ]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code
            )
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **self.model_options(
                    app_label='microbiome_maternal', model_name=model_name, appointment=appointment
                )).count(), 1)

    def test_hiv_rapid_test_pos(self):
        """
        """
        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
        )
        visit_codes = [
            ['1000M', ['maternalarvhistory', 'maternalarvpreg']],
#             ['2000M', ['maternalarvpreg', 'maternalarv', 'maternallabdelclinic']],
#             ['2010M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2030M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2060M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2090M', ['maternalarvpost', 'maternalarvpostadh']],
#             ['2120M', ['maternalarvpost', 'maternalarvpostadh']],
        ]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code
            )
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **self.model_options(
                    app_label='microbiome_maternal', model_name=model_name, appointment=appointment
                )).count(), 1)

    def test_hiv_rapid_test_neg(self):
        """
        """
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            process_rapid_test=YES,
            rapid_test_result=NEG,
        )
        visit_codes = [
            ['2010M', ['rapidtestresult']],
            ['2030M', ['rapidtestresult']],
            ['2060M', ['rapidtestresult']],
            ['2090M', ['rapidtestresult']],
            ['2120M', ['rapidtestresult']]
        ]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code
            )
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **self.model_options(
                    app_label='microbiome_maternal', model_name=model_name, appointment=appointment
                )).count(), 1)

    def test_srh_referral_yes_on_srhservicesutilization(self):
        """
        """
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject, process_rapid_test=YES,
            breastfeed_for_a_year=YES, rapid_test_result=POS
        )
        for code in ['2010M', '2030M']: #, '2030M', '2090M', '2120M']: 
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code
            )
            SexualReproductiveHealthFactory(
                maternal_visit=MaternalVisitFactory(appointment=appointment)
            )
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **self.model_options(
                app_label='microbiome_maternal', model_name='srhservicesutilization', appointment=appointment
            )).count(), 1)
