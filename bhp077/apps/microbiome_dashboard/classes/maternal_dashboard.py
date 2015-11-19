from collections import OrderedDict

from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject
from edc_base.utils import convert_from_camel
from edc_constants.constants import YES, POS, NEG, IND

from bhp077.apps.microbiome_lab.models.maternal_requisition import MaternalRequisition
from bhp077.apps.microbiome_maternal.models import (MaternalVisit, MaternalEligibility,
                                                    MaternalLocator, MaternalConsent,
                                                    AntenatalEnrollment, PostnatalEnrollment)
from bhp077.apps.microbiome_infant.models import InfantBirth


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
        self.membership_form_category = ['sample', 'antenatal', 'postnatal']
        self.dashboard_models['maternal_eligibility'] = MaternalEligibility
        self.dashboard_models['maternal_consent'] = MaternalConsent
        self.dashboard_models['visit'] = MaternalVisit
        self.requisition_model = MaternalRequisition
        self._locator_model = MaternalLocator

    def get_context_data(self, **kwargs):
        super(MaternalDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='microbiome',
            search_name='maternal',
            title='Maternal Dashboard',
            subject_dashboard_url=self.subject_dashboard_url,
            infants=self.get_registered_infant_identifier(),
            maternal_consent=self.consent,
            antenatal_hiv_status=self.antenatal_maternal_hiv_status(),
            postnatal_hiv_status=self.postnatal_maternal_hiv_status())
        return self.context

    @property
    def consent(self):
        self._consent = None
        if MaternalConsent.objects.filter(subject_identifier=self.subject_identifier):
            self._consent = MaternalConsent.objects.get(subject_identifier=self.subject_identifier)
        return self._consent

    def antenatal_maternal_hiv_status(self):
        antenatal = AntenatalEnrollment.objects.filter(registered_subject=self.registered_subject)
        if antenatal:
            if antenatal[0].verbal_hiv_status == POS and antenatal[0].evidence_hiv_status == YES:
                self._maternal_hiv_status = 'HIV Infected'
            elif antenatal[0].verbal_hiv_status == NEG and antenatal[0].evidence_hiv_status == YES:
                self._maternal_hiv_status = 'HIV uninfected'
            elif antenatal[0].verbal_hiv_status == 'NEVER':
                self._maternal_hiv_status = 'Never Tested'
            elif antenatal[0].verbal_hiv_status == 'UNK':
                self._maternal_hiv_status = 'UNK'
            elif antenatal[0].verbal_hiv_status == 'REFUSED':
                self._maternal_hiv_status = 'REFUSED'
            elif antenatal[0].rapid_test_result == POS:
                self._maternal_hiv_status = 'POS ANT rapid test'
            elif antenatal[0].rapid_test_result == NEG:
                self._maternal_hiv_status = 'NEG ANT rapid test'
            elif antenatal[0].rapid_test_result == IND:
                self._maternal_hiv_status = 'IND ANT rapid test'
            return self._maternal_hiv_status

    def postnatal_maternal_hiv_status(self):
        postnatal = PostnatalEnrollment.objects.filter(registered_subject=self.registered_subject)
        if postnatal:
            if postnatal[0].verbal_hiv_status == POS and postnatal[0].evidence_hiv_status == YES:
                self._maternal_hiv_status = 'HIV Infected'
            elif postnatal[0].verbal_hiv_status == NEG and postnatal[0].evidence_hiv_status == YES:
                self._maternal_hiv_status = 'HIV uninfected'
            elif postnatal[0].verbal_hiv_status == 'NEVER':
                self._maternal_hiv_status = 'Never Tested'
            elif postnatal[0].verbal_hiv_status == 'UNK':
                self._maternal_hiv_status = 'UNK'
            elif postnatal[0].verbal_hiv_status == 'REFUSED':
                self._maternal_hiv_status = 'REFUSED'
            elif postnatal[0].rapid_test_result == POS:
                self._maternal_hiv_status = 'POS PNT rapid test'
            elif postnatal[0].rapid_test_result == NEG:
                self._maternal_hiv_status = 'NEG PNT rapid test'
            elif postnatal[0].rapid_test_result == IND:
                self._maternal_hiv_status = 'IND PNT rapid test'
            return self._maternal_hiv_status

    def get_locator_model(self):
        return MaternalLocator

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    @RegisteredSubjectDashboard.locator_model.getter
    def locator_model(self):
        return self.get_locator_model()

    def get_registered_infant_identifier(self):
        """Returns an infant identifier associated with the maternal identifier"""
        infants = OrderedDict()
        infant_registered_subject = None
        try:
            infant_registered_subject = RegisteredSubject.objects.get(
                subject_type='infant', relative_identifier__iexact=self.subject_identifier
            )
            try:
                infant_birth = InfantBirth.objects.get(registered_subject__exact=infant_registered_subject)
                dct = infant_birth.__dict__
                dct['dashboard_model'] = convert_from_camel(infant_birth._meta.object_name)
                dct['dashboard_id'] = convert_from_camel(infant_birth.pk)
                dct['dashboard_type'] = 'infant'
                infants[infant_registered_subject.subject_identifier] = dct
            except InfantBirth.DoesNotExist:
                dct = {'subject_identifier': infant_registered_subject.subject_identifier}
                dct['dashboard_model'] = 'registered_subject'
                dct['dashboard_id'] = infant_registered_subject.pk
                dct['dashboard_type'] = 'infant'
                infants[infant_registered_subject.subject_identifier] = dct
        except RegisteredSubject.DoesNotExist:
            pass
        return infants
