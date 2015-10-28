from collections import OrderedDict

from edc.core.bhp_common.utils import convert_from_camel
from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from apps.microbiome_maternal.models import (MaternalVisit, MaternalEligibility,
                                             MaternalLocator, MaternalConsent)
from bhp077.apps.microbiome_lab.models.maternal_requisition import MaternalRequisition


class MaternalDashboard(RegisteredSubjectDashboard):

    view = 'maternal_dashboard'
    dashboard_url_name = 'subject_dashboard_url'
    dashboard_name = 'Maternal Dashboard'
    urlpattern_view = 'apps.microbiome_dashboard.views'
    template_name = 'maternal_dashboard.html'
    urlpatterns = [
        RegisteredSubjectDashboard.urlpatterns[0][:-1] +
        '(?P<appointment_code>{appointment_code})/$'] + RegisteredSubjectDashboard.urlpatterns
    urlpattern_options = dict(
        RegisteredSubjectDashboard.urlpattern_options,
        dashboard_model=RegisteredSubjectDashboard.urlpattern_options['dashboard_model'] + '|maternal_eligibility',
        dashboard_type='maternal',
        appointment_code='1000M|2000M|2010M|2030M|2060M|2090M|2120M', )

    def __init__(self, **kwargs):
        super(MaternalDashboard, self).__init__(**kwargs)
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.visit_model = MaternalVisit
        self.dashboard_type_list = ['maternal']
        self.membership_form_category = ['postnatal', 'childbirth', 'after_birth']
        self.dashboard_models['maternal_eligibility'] = MaternalEligibility
        self.dashboard_models['maternal_consent'] = MaternalConsent
        self.requisition_model = MaternalRequisition
        self._locator_model = None

    def get_context_data(self, **kwargs):
        super(MaternalDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='microbiome',
            search_name='maternal',
            title='Maternal Dashboard', )
        return self.context

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['maternal']

    def get_visit_model(self):
        return MaternalVisit

    def get_locator_model(self):
        return MaternalLocator
