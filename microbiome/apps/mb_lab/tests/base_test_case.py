from django.test.testcases import TestCase

from edc_constants.constants import POS, YES
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject
from edc_lab.lab_profile.classes import site_lab_profiles

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_maternal.tests.factories import (MaternalConsentFactory, PostnatalEnrollmentFactory,
                                                         MaternalVisitFactory, MaternalEligibilityFactory,
                                                         MaternalLabourDelFactory)
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory, InfantVisitFactory
from microbiome.load_edc import load_edc

from ..tests.factories import MaternalRequistionFactory, InfantRequistionFactory
from ..models import Panel, AliquotType, Receive, Aliquot


class BaseTestCase(TestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        load_edc()
        self.study_site = '40'

    def requisition_instances(self):
        instances = []
        maternal_eligibility = MaternalEligibilityFactory()
        instances.append(maternal_eligibility)
        maternal_consent = MaternalConsentFactory(
            registered_subject=maternal_eligibility.registered_subject)
        instances.append(maternal_consent)
        maternal_registered_subject = maternal_consent.registered_subject
        instances.append(maternal_registered_subject)
        post_natal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=maternal_registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        instances.append(post_natal_enrollment)
        maternal_appointment_1000 = Appointment.objects.get(registered_subject=maternal_registered_subject,
                                                            visit_definition__code='1000M')
        instances.append(maternal_appointment_1000)
        maternal_visit_1000 = MaternalVisitFactory(appointment=maternal_appointment_1000)
        instances.append(maternal_visit_1000)

        maternal_appointment_2000 = Appointment.objects.get(registered_subject=maternal_registered_subject,
                                                            visit_definition__code='2000M')
        instances.append(maternal_appointment_2000)
        maternal_visit_2000 = MaternalVisitFactory(appointment=maternal_appointment_2000)
        instances.append(maternal_visit_2000)

        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit_2000)
        instances.append(maternal_labour_del)
        infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=maternal_registered_subject.subject_identifier,
            subject_type=INFANT)
        instances.append(infant_registered_subject)
        infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=maternal_labour_del)
        instances.append(infant_birth)
        infant_appointment_2000 = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        instances.append(infant_appointment_2000)
        infant_visit_2000 = InfantVisitFactory(appointment=infant_appointment_2000)
        instances.append(infant_visit_2000)

        # Maternal Requisitions
        viral_load = MaternalRequistionFactory(panel=Panel.objects.get(name='Viral Load'),
                                               maternal_visit=maternal_visit_2000,
                                               aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        instances.append(viral_load)
        breast_milk = MaternalRequistionFactory(panel=Panel.objects.get(name='Breast Milk (Storage)'),
                                                maternal_visit=maternal_visit_2000,
                                                aliquot_type=AliquotType.objects.get(alpha_code='BMF'))
        instances.append(breast_milk)
        vaginal_swab = MaternalRequistionFactory(panel=Panel.objects.get(name='Vaginal swab (Storage)'),
                                                 maternal_visit=maternal_visit_2000,
                                                 aliquot_type=AliquotType.objects.get(alpha_code='VS'))
        instances.append(vaginal_swab)
        rectal_swap = MaternalRequistionFactory(panel=Panel.objects.get(name='Rectal swab (Storage)'),
                                                maternal_visit=maternal_visit_2000,
                                                aliquot_type=AliquotType.objects.get(alpha_code='RS'))
        instances.append(rectal_swap)
        vaginal_sti_swab = MaternalRequistionFactory(panel=Panel.objects.get(name='Vaginal STI Swab (Storage)'),
                                                     maternal_visit=maternal_visit_2000,
                                                     aliquot_type=AliquotType.objects.get(alpha_code='VS'))
        instances.append(vaginal_sti_swab)
        hematology = MaternalRequistionFactory(panel=Panel.objects.get(name='Hematology (ARV)'),
                                               maternal_visit=maternal_visit_2000,
                                               aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        instances.append(hematology)
        cd4 = MaternalRequistionFactory(panel=Panel.objects.get(name='CD4/ CD8'),
                                        maternal_visit=maternal_visit_2000,
                                        aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        instances.append(cd4)

        # Infant Requisitions
        dna_cpr = InfantRequistionFactory(panel=Panel.objects.get(name='DNA PCR'),
                                          infant_visit=infant_visit_2000,
                                          aliquot_type=AliquotType.objects.get(alpha_code='SW'))
        instances.append(dna_cpr)
        stool_storage = InfantRequistionFactory(panel=Panel.objects.get(name='Stool storage'),
                                                infant_visit=infant_visit_2000,
                                                aliquot_type=AliquotType.objects.get(alpha_code='ST'))
        instances.append(stool_storage)
        pbmc_plasma = InfantRequistionFactory(panel=Panel.objects.get(name='PBMC Plasma (STORE ONLY)'),
                                              infant_visit=infant_visit_2000,
                                              aliquot_type=AliquotType.objects.get(alpha_code='PL'))
        instances.append(pbmc_plasma)
        rectal_swab = InfantRequistionFactory(panel=Panel.objects.get(name='Rectal swab (Storage)'),
                                              infant_visit=infant_visit_2000,
                                              aliquot_type=AliquotType.objects.get(alpha_code='RS'))
        instances.append(rectal_swab)
        viral_load = InfantRequistionFactory(panel=Panel.objects.get(name='Viral Load'),
                                             infant_visit=infant_visit_2000,
                                             aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        instances.append(viral_load)
        chemistry = InfantRequistionFactory(panel=Panel.objects.get(name='Chemistry'),
                                            infant_visit=infant_visit_2000,
                                            aliquot_type=AliquotType.objects.get(alpha_code='BC'))
        instances.append(chemistry)
        haematology = InfantRequistionFactory(panel=Panel.objects.get(name='Hematology (ARV)'),
                                              infant_visit=infant_visit_2000,
                                              aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        instances.append(haematology)

        # Start processing the samples.
        stool_storage.is_receive = True
        stool_storage.save()
        lab_profile = site_lab_profiles.get(stool_storage._meta.object_name)
        receive = lab_profile().receive(stool_storage)
        self.assertEqual(Receive.objects.all().count(), 1)
        instances.append(receive)
        self.assertEqual(Aliquot.objects.all().count(), 1)
        return instances
