# from django.test import TestCase
# from django.utils import timezone
# 
# from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
# from edc.lab.lab_profile.classes import site_lab_profiles
# from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
# from edc.lab.lab_clinic_api.tests.factories import PanelFactory
# from edc.subject.appointment.models import Appointment
# from edc.subject.lab_tracker.classes import site_lab_tracker
# from edc.subject.rule_groups.classes import site_rule_groups
# from edc.subject.code_lists.models import WcsDxAdult
# from edc_constants.choices import YES, NO
# from edc.entry_meta_data.models.requisition_meta_data import RequisitionMetaData
# 
# from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
# from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
# from bhp077.apps.microbiome_list.models.chronic_conditions import ChronicConditions
# from bhp077.apps.microbiome_maternal.forms import (MaternalPostFuForm, MaternalPostFuDxForm)
# from bhp077.apps.microbiome_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule
# from bhp077.apps.microbiome_maternal.tests.factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
#                         MaternalEligibilityFactory, MaternalConsentFactory)
# 
# from ..forms import MaternalRequisitionForm
# from ..models import Panel
# 
# 
# class TestMaternalRequisition(TestCase):
#     """Test eligibility of a mother for postnatal followup."""
# 
#     def setUp(self):
#         try:
#             site_lab_profiles.register(MaternalProfile())
#         except AlreadyRegisteredLabProfile:
#             pass
#         MicrobiomeConfiguration().prepare()
#         site_lab_tracker.autodiscover()
#         PostnatalEnrollmentVisitSchedule().build()
#         site_rule_groups.autodiscover()
#         self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
#         self.maternal_eligibility = MaternalEligibilityFactory()
#         self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
#                                                        study_site=self.study_site)
#         self.registered_subject = self.maternal_consent.registered_subject
#         self.postnatal_enrollment = PostnatalEnrollmentFactory(
#             registered_subject=self.registered_subject,
#             will_breastfeed=YES
#         )
#         self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
#                                                    visit_definition__code='2000M')
#         self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
# #         self.chronic_cond = ChronicConditions.objects.create(name='N/A', short_name='N/A', display_index=10,
# #                                                              field_name='chronic_cond')
#         self.panel = Panel.objects.get(name='Breast Milk (Storage)')
#         self.data = {
#             'maternal_visit': self.maternal_visit.id,
#             'requisition_datetime': timezone.now(),
#             'is_drawn': NO,
#             'reason_not_drawn': 'collection_failed',
#             'drawn_datetime': '',
#             'site': '',
#             'panel': self.panel.id,
#             'aliquot_type': '',
#             'item_type': '',
#             'item_count_total': '',
#             'estimated_volume': '',
#             'priority': '',
#             'comments': '',
#         }
# 
#     def test_dates(self):
# #         pr = RequisitionMetaData.objects.filter(appointment=self.maternal_visit.appointment)
# #         print pr[0].__dict__
#         self.data['drawn_datetime'] = timezone.now() + timezone.timedelta(days=2)
#         form = MaternalRequisitionForm(data=self.data)
#         errors = ''.join(form.errors.get('__all__'))
#         self.assetIn('Requisition date cannot be in future of specimen date.', errors)
