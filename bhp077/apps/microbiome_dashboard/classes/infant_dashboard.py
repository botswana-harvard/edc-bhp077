from collections import OrderedDict

from edc.core.bhp_common.utils import convert_from_camel
from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from bhp077.apps.microbiome_infant.models import InfantVisit, InfantBirth
from bhp077.apps.microbiome_lab.models import InfantRequisition
from bhp077.apps.microbiome_maternal.models import MaternalLocator, MaternalConsent


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
        appointment_code='2000|2010|2030')

    def __init__(self, **kwargs):
        super(InfantDashboard, self).__init__(**kwargs)
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.visit_model = InfantVisit
        self.dashboard_type_list = ['infant']
        self.dashboard_models['registered_subject'] = RegisteredSubject
        self.dashboard_models['infant_birth'] = InfantBirth
        self.dashboard_models['visit'] = InfantVisit
        self.membership_form_category = ['infant_birth_record']
        self.requisition_model = InfantRequisition
        self._locator_model = None
        self._maternal_identifier = None

    def get_context_data(self, **kwargs):
        super(InfantDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='microbiome',
            search_name='infant',
            title='Infant Dashboard',
            subject_dashboard_url=self.subject_dashboard_url,
            maternal_consent=self.maternal_consent, )
        return self.context

    def get_locator_model(self):
        return MaternalLocator

    @RegisteredSubjectDashboard.locator_model.getter
    def locator_model(self):
        return self.get_locator_model()

    @property
    def maternal_consent(self):
        return MaternalConsent.objects.get(subject_identifier=self.maternal_identifier)

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    @property
    def maternal_identifier(self):
        return self.registered_subject.relative_identifier
