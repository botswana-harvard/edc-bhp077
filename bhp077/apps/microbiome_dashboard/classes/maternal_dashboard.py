from collections import OrderedDict

from edc.core.bhp_common.utils import convert_from_camel
from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from apps.microbiome_maternal.models import MaternalVisit, MaternalEligibility, MaternalLocator


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

    def __init__(self, *args, **kwargs):
        super(MaternalDashboard, self).__init__(*args, **kwargs)
        self._visit_model = MaternalVisit
        self._registered_subject = None
        self._dashboard_type_list = ['maternal']
        self.extra_url_context = ""
        kwargs.update({'dashboard_models': {'maternal_eligibility': MaternalEligibility},
                       'membership_form_category': ['postnatal', 'childbirth', 'after_birth']})
        self._locator_model = None
        self._requisition_model = None

    def get_context_data(self):
        super(MaternalDashboard, self).add_to_context()
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
