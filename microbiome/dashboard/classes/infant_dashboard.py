from datetime import timedelta, date, datetime

from edc.dashboard.subject.classes import RegisteredSubjectDashboard
from edc.subject.registration.models import RegisteredSubject

from microbiome.infant.models import InfantBirth, InfantVisit
from microbiome.maternal.models import MaternalConsent
from microbiome.microbiome_lab.models import InfantRequisition, PackingList, Panel


class InfantDashboard(RegisteredSubjectDashboard):

    view = 'infant_dashboard'
    dashboard_name = 'Infant Dashboard'
    dashboard_url_name = 'subject_dashboard_url'
    urlpatterns = [
        RegisteredSubjectDashboard.urlpatterns[0][:-1] + '(?P<appointment_code>{appointment_code})/$'
        ] + RegisteredSubjectDashboard.urlpatterns
    urlpattern_options = dict(
        RegisteredSubjectDashboard.urlpattern_options,
        dashboard_model=RegisteredSubjectDashboard.urlpattern_options['dashboard_model'] + '|infant_birth_record',
        dashboard_type='infant',
        appointment_code='1000|1001|1002|1003|1004|1006|1008|1012|1024|1036|1048|1060|1072|1084|1096|1108|1120|1132|1144|1156|1168|1180|1192')

    template_name = 'infant_dashboard.html'

    def __init__(self, *args, **kwargs):
        super(InfantDashboard, self).__init__(*args, **kwargs)
        self._infant_birth = None
        self.dashboard_type_list = ['infant']
        self.dashboard_models['infant_birth'] = InfantBirth
        self.membership_form_category = ['infant_birth_record']
        self.visit_model = InfantVisit
        self._locator_model = None
        self._requisition_model = InfantRequisition

    def get_context_data(self, **kwargs):
        self.context = super(InfantDashboard, self).get_context_data(**kwargs)
        panels = Panel.objects.all()
        self.context.update(
            home='microbiome',
            search_name='infant',
            maternal_dashboard_url=self.get_maternal_dashboard_url(),
            title='Infant Dashboard',
            delivery_datetime=self.get_delivery_datetime(),
            infant_birth=self.birth,
            delivery_date=self.get_delivery_date(),
            maternal_consent=self.get_maternal_consent(),
            panels=panels,
            local_results=self.render_labs(),
            subject_identifier=self.registered_subject.subject_identifier,
        )
        return self.context

    @property
    def registered_subject(self):
        if not self._registered_subject:
            try:
                self._registered_subject = RegisteredSubject.objects.get(pk=self.dashboard_id)
            except RegisteredSubject.DoesNotExist:
                try:
                    self._registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
                except RegisteredSubject.DoesNotExist:
                    try:
                        self._registered_subject = self.appointment.registered_subject
                    except AttributeError:
                        pass
        return self._registered_subject

    @property
    def subject_identifier(self):
        self._subject_identifier = None
        if self.birth:
            self._subject_identifier=self.birth.registered_subject.subject_identifier
        return self._subject_identifier

    @property
    def birth(self):
        if InfantBirth.objects.filter(id=self.dashboard_id):
            self._infant_birth = InfantBirth.objects.get(id=self.dashboard_id)
        elif self.appointment:
            self._infant_birth = InfantBirth.objects.get(registered_subject=self.appointment.registered_subject)
        elif self.registered_subject:
            try:
                self._infant_birth = InfantBirth.objects.get(registered_subject=self.registered_subject)
            except Exception as e:
                self._infant_birth = InfantBirth.objects.none()
        else:
            self._infant_birth = InfantBirth.objects.none()
        return self._infant_birth

    def set_membership_form_category(self):
        self._membership_form_category = 'infant'

    def get_maternal_dashboard_url(self):
        return 'subject_dashboard_url'

    def set_dashboard_type_list(self):
        self._dashboard_type_list = ['infant']

    def set_consent(self):
        """Sets to the subject consent, if it has been completed."""
        self._consent = self.get_maternal_consent()

    def get_visit_model(self):
        return InfantVisit

    def get_subject_identifier(self):
        return self.subject_identifier

    def get_maternal_consent(self):
        consent = MaternalConsent.objects.get(subject_identifier=self.registered_subject.relative_identifier)
        return consent

    def get_infant_birth(self):
        return self.birth

    def get_days_alive(self):
        days_alive = None
        if self.get_infant_birth():
            if date.today() - self.get_infant_birth().dob <= timedelta(days=60):
                days_alive = (date.today() - self.get_infant_birth().dob + timedelta(days=1)).days
        return days_alive

    def subject_hiv_status(self):
        return 'POS'

