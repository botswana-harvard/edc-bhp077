from collections import OrderedDict

from edc.core.bhp_common.utils import convert_from_camel
from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from microbiome.infant.models import InfantVisit, InfantBirth
from microbiome.microbiome_lab.models import InfantRequisition


class InfantDashboard(RegisteredSubjectDashboard):

    view = 'infant_dashboard'
    dashboard_url_name = 'subject_dashboard_url'
    dashboard_name = 'Infant Dashboard'
    urlpattern_view = 'microbiome.dashboard.views'
    template_name = 'infant_dashboard.html'

    def __init__(self, *args, **kwargs):
        super(InfantDashboard, self).__init__(*args, **kwargs)
        self._visit_model = InfantVisit
        self._registered_subject = None
        self._dashboard_type_list = self.set_dashboard_type_list()
        self.extra_url_context = ""
        kwargs.update({'dashboard_models': {'infant_birth': InfantBirth},
                       'membership_form_category': ['infant_birth_record']})
        self._locator_model = None
        self._requisition_model = InfantRequisition

    def get_context_data(self):
        super(InfantDashboard, self).add_to_context()
        self.context.update(
            home='microbiome',
            search_name='infant',
            title='Infant Dashboard', )
        return self.context

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['infant']

    def get_visit_model(self):
        return InfantVisit
