from collections import OrderedDict

from edc.core.bhp_common.utils import convert_from_camel
from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from bhp077.apps.microbiome_infant.models import InfantVisit, InfantBirth
from bhp077.apps.microbiome_maternal.models import MaternalVisit
from bhp077.apps.microbiome_lab.models import InfantRequisition
from bhp077.apps.microbiome_maternal.models import MaternalLocator, MaternalConsent, MaternalEligibility


class InfantDashboard(RegisteredSubjectDashboard):

    view = 'infant_dashboard'
    dashboard_url_name = 'subject_dashboard_url'
    dashboard_name = 'Infant Dashboard'
    urlpattern_view = 'apps.microbiome_dashboard.views'
    template_name = 'infant_dashboard.html'
    urlpatterns = [
        RegisteredSubjectDashboard.urlpatterns[0][:-1] + '(?P<appointment_code>{appointment_code})/$'] + RegisteredSubjectDashboard.urlpatterns
    urlpattern_options = dict(
        RegisteredSubjectDashboard.urlpattern_options,
        dashboard_model=RegisteredSubjectDashboard.urlpattern_options['dashboard_model'] + '|infant_birth',
        dashboard_type='infant',
        appointment_code='2000|2010|2030|2060|2090|2120')

    def __init__(self, **kwargs):
        super(InfantDashboard, self).__init__(**kwargs)
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.visit_model = InfantVisit
        self.dashboard_type_list = ['infant']
        self.dashboard_models['registered_subject'] = RegisteredSubject
        self.dashboard_models['infant_birth'] = InfantBirth
        self.dashboard_models['visit'] = InfantVisit
        self.membership_form_category = ['infant_enrollment']
        self.requisition_model = InfantRequisition
        self._locator_model = None
        self._maternal_identifier = None
        self._infant_birth = None
        #self._visit_model = None

    def get_context_data(self, **kwargs):
        super(InfantDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='microbiome',
            search_name='infant',
            title='Infant Dashboard',
            subject_dashboard_url=self.subject_dashboard_url,
            infant_hiv_status=self.infant_hiv_status,
            maternal_consent=self.maternal_consent,
            maternal_eligibility=self.maternal_eligibility,
            local_results=self.render_labs(),
            infant_birth=self.infant_birth, )
        return self.context

    @property
    def maternal_consent(self):
        return MaternalConsent.objects.get(subject_identifier=self.maternal_identifier)

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    @property
    def maternal_identifier(self):
        return self.registered_subject.relative_identifier

    @RegisteredSubjectDashboard.locator_model.getter
    def locator_model(self):
        return MaternalLocator

    @property
    def locator_visit_model(self):
        return MaternalVisit

    @property
    def locator_registered_subject(self):
        return RegisteredSubject.objects.get(
            subject_identifier=self.maternal_identifier)

    @property
    def maternal_eligibility(self):
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=self.maternal_identifier)
        except MaternalEligibility.DoesNotExist:
            pass

    @property
    def infant_birth(self):
        try:
            self._infant_birth = InfantBirth.objects.get(
                registered_subject__subject_identifier=self.subject_identifier)
        except InfantBirth.DoesNotExist:
            self._infant_birth = None
        return self._infant_birth

    @property
    def registered_subject(self):
        if not self._registered_subject:
            try:
                self._registered_subject = RegisteredSubject.objects.get(pk=self.dashboard_id)
            except RegisteredSubject.DoesNotExist:
                try:
                    self._registered_subject = self.dashboard_model_instance.registered_subject
                except AttributeError:
                    try:
                        self._registered_subject = self.dashboard_model_instance.appointment.registered_subject
                    except AttributeError:
                        try:
                            self._infant_birth = InfantBirth.objects.get(pk=self.dashboard_id)
                            self._registered_subject = self._infant_birth.registered_subject
                        except InfantBirth.DoesNotExist:
                            pass
        return self._registered_subject

    @property
    def infant_hiv_status(self):
        return None
