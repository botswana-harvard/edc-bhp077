from edc_admin_exclude import AdminExcludeFieldsMixin

from ..models import InfantVisit


class InfantStoolExcludeFieldsMixin(AdminExcludeFieldsMixin):

    visit_model = InfantVisit
    visit_attr = 'infant_visit'
    visit_codes = {'visit': ['2000']}
