from django.test import TestCase

from .factories import PostnatalEnrollmentFactory, SexualReproductiveHealthFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory

class TestRuleGroup(TestCase):

    def setUp(self):
        pass

    def Atest_hiv_status_pos_on_postnatal_enrollment(self):
        """
        """
        registered_subject = RegisteredSubjectFactory()
        PostnatalEnrollmentFactory(registered_subject=registered_subject)

        maternalinfected_options = {}
        maternalinfected_options.update(
            entry__app_label='microbiome_maternal',
            entry__model_name='maternalinfected',
            appointment__registered_subject=registered_subject)

        maternalarvhistory_options = {}
        maternalarvhistory_options.update(
            entry__app_label='microbiome_maternal',
            entry__model_name='maternalarvhistory',
            appointment__registered_subject=registered_subject)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **maternalinfected_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **maternalarvhistory_options).count(), 1)


    def Btest_hiv_status_pos_on_postnatal_enrollment1(self):
        """
        """
        registered_subject = RegisteredSubjectFactory()
        PostnatalEnrollmentFactory(
            registered_subject=registered_subject, process_rapid_test=YES, rapid_test_result=POS
        )

        maternalarvhistory_options = {}
        maternalarvhistory_options.update(
            entry__app_label='microbiome_maternal',
            entry__model_name='maternalarvhistory',
            appointment__registered_subject=registered_subject)

        maternalarvpost_options = {}
        maternalarvpost_options.update(
            entry__app_label='microbiome_maternal',
            entry__model_name='maternalarvpost',
            appointment__registered_subject=registered_subject)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **maternalarvhistory_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **maternalarvpost_options).count(), 1)

    def test_sexualreproductivehealth(self):
        """
        """
        registered_subject = RegisteredSubjectFactory()
        maternal_visit = MaternalVisitFactory(registered_subject=registered_subject)
        SexualReproductiveHealthFactory(maternal_visit=maternal_visit)

        srhservicesutilization = {}
        srhservicesutilization.update(
            entry__app_label='microbiome_maternal',
            entry__model_name='srhservicesutilization',
            appointment=maternal_visit.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **srhservicesutilization).count(), 1)
