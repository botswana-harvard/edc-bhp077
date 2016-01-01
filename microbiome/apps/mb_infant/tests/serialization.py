from django.utils import timezone
from datetime import date

from django.core import serializers
from django.test import TestCase

from edc_appointment.models import Appointment
from edc_constants.constants import YES, POS, COMPLETED_PROTOCOL_VISIT

from edc_lab.lab_profile.classes import site_lab_profiles
from edc_lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_rule_groups.classes import site_rule_groups
from edc.subject.lab_tracker.classes import site_lab_tracker

from edc_base.encrypted_fields import FieldCryptor
from edc_registration.models import RegisteredSubject

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory
from microbiome.apps.mb_infant.visit_schedule import InfantBirthVisitSchedule
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile, InfantProfile
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory
from microbiome.apps.mb_maternal.visit_schedule import (
    AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule)
from microbiome.apps.mb_infant.tests.factories.infant_visit_factory import InfantVisitFactory
from microbiome.apps.mb_infant.tests.factories.infant_birth_data_factory import InfantBirthDataFactory
from microbiome.apps.mb_infant.models.infant_birth_exam import InfantBirthExam
from ..models import (
    InfantBirthFeedVaccine, InfantStoolCollection, InfantCongenitalAnomalies, InfantDeathReport, InfantOffStudy)
from microbiome.apps.mb_infant.tests.factories.infant_fu_factory import InfantFuFactory


# TODO: need to rewrite these tests
class SerializeToTransaction(object):
    pass


class TestNaturalKey(TestCase):

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
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        self.registered_subject_infant = RegisteredSubject.objects.get(
            subject_type=INFANT, relative_identifier=self.registered_subject.subject_identifier)
#         self.infant_birth = InfantBirthFactory(
#             registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

    def test_serializing_deserialing_infant_birth(self):
        infant_birth = InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

        outgoing_tx = SerializeToTransaction().serialize(
            infant_birth.__class__, infant_birth, False, True, 'default')

        for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_tx.tx)):
            self.assertEqual(transaction.object.pk, infant_birth.pk)

    def test_serializing_deserialing_infant_visit(self):
        InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000')

        infant_visit = InfantVisitFactory(
            appointment=appointment)

        outgoing_tx = SerializeToTransaction().serialize(
            infant_visit.__class__, infant_visit, False, True, 'default')

        for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_tx.tx)):
            self.assertEqual(transaction.object.pk, infant_visit.pk)

    def test_serializing_deserialing_infant_birth_data(self):
        InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000')
        infant_visit = InfantVisitFactory(
            appointment=appointment)
        infant_birth_data = InfantBirthDataFactory(
            infant_visit=infant_visit
        )
        outgoing_tx = SerializeToTransaction().serialize(
            infant_birth_data.__class__, infant_birth_data, False, True, 'default')

        for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_tx.tx)):
            self.assertEqual(transaction.object.pk, infant_birth_data.pk)

    def test_serializing_deserialing_visit_models_2000(self):
        InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000')
        infant_visit = InfantVisitFactory(
            appointment=appointment)
        visit_model_classes = [
            InfantBirthExam, InfantBirthFeedVaccine, InfantStoolCollection, InfantCongenitalAnomalies]
        for visit_model_class in visit_model_classes:
            visit_model = visit_model_class.objects.create(
                infant_visit=infant_visit,
                report_datetime=timezone.now()
            )
            outgoing_tx = SerializeToTransaction().serialize(
                visit_model.__class__, visit_model, False, True, 'default')

            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_tx.tx)):
                self.assertEqual(transaction.object.pk, visit_model.pk)

    def test_serializing_deserialing_infant_death(self):
        InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000')
        infant_visit = InfantVisitFactory(
            appointment=appointment)

        infant_death = InfantDeathReport.objects.create(
            infant_visit=infant_visit,
            report_datetime=timezone.now(),
            death_date=date(2015, 12, 15),
            cause_id=5,
            cause_category_id=2,
            illness_duration=2,
            diagnosis_code_id=2,
            medical_responsibility_id=1,
            registered_subject=self.registered_subject_infant
        )
        out_tx = SerializeToTransaction().serialize(
            infant_death.__class__, infant_death, False, True, 'default')
        serialized_objects = serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(out_tx.tx))
        for transaction in serialized_objects:
            self.assertEqual(transaction.object.pk, infant_death.pk)

    def test_serializing_deserialing_infant_offstudy(self):
        InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000')
        infant_visit = InfantVisitFactory(
            appointment=appointment,
            reason=COMPLETED_PROTOCOL_VISIT)

        infant_offstudy = InfantOffStudy.objects.create(
            infant_visit=infant_visit,
            report_datetime=timezone.now(),
            registered_subject=self.registered_subject_infant,
            offstudy_date=date(2015, 12, 12),
        )
        outgoing_tx = SerializeToTransaction().serialize(
            infant_offstudy.__class__, infant_offstudy, False, True, 'default')

        for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_tx.tx)):
            self.assertEqual(transaction.object.pk, infant_offstudy.pk)

    def test_serializing_deserialing_visit_models_2010(self):
        InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=self.maternal_labour_del)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant, visit_definition__code='2000')
        InfantVisitFactory(appointment=appointment)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2010')
        infant_visit = InfantVisitFactory(appointment=appointment)
        infant_fu = InfantFuFactory(infant_visit=infant_visit)
        outgoing_tx = SerializeToTransaction().serialize(
            infant_fu.__class__, infant_fu, False, True, 'default')

        for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_tx.tx)):
            self.assertEqual(transaction.object.pk, infant_fu.pk)
