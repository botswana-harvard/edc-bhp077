from collections import OrderedDict

from edc.core.bhp_common.utils import convert_from_camel
from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from apps.microbiome_infant.models import InfantVisit, InfantBirth
from apps.microbiome_lab.models import InfantRequisition


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
        self.dashboard_models['infant_birth'] = InfantBirth
        self.membership_form_category = ['infant_birth_record']
        self.requisition_model = InfantRequisition

    def get_context_data(self, **kwargs):
        super(InfantDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='microbiome',
            search_name='infant',
            title='Infant Dashboard', )
        return self.context

    def get_visit_model(self):
        return InfantVisit
