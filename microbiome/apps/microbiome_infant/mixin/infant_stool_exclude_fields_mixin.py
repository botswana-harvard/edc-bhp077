from edc_admin_exclude import AdminExcludeFieldsMixin

from bhp077.apps.microbiome_infant.models.infant_visit import InfantVisit


class InfantStoolExcludeFieldsMixin(AdminExcludeFieldsMixin):

    visit_model = InfantVisit
    visit_attr = 'infant_visit'
    visit_codes = {'visit': ['2000']}
