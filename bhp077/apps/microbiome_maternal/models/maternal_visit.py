from django.db import models

from edc.entry_meta_data.models import MetaDataMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_constants.constants import OFF_STUDY, YES, POS, UNSCHEDULED, NEG, DEATH_VISIT
from edc_visit_tracking.constants import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from edc_visit_tracking.models import BaseVisitTracking
from edc_visit_tracking.models import PreviousVisitMixin

from bhp077.apps.microbiome.choices import VISIT_REASON
from bhp077.apps.microbiome_maternal.models import MaternalConsent, PostnatalEnrollment, AntenatalEnrollment

from .maternal_off_study_mixin import MaternalOffStudyMixin


class MaternalVisit(MaternalOffStudyMixin, PreviousVisitMixin, MetaDataMixin, RequiresConsentMixin,
                    BaseVisitTracking, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    CONSENT_MODEL = MaternalConsent

    history = AuditTrail()

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        if not self.is_eligible():
            self.reason = OFF_STUDY
        super(MaternalVisit, self).save(*args, **kwargs)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def is_eligible(self):
        """Returns True if participant is either eligible ante or post natal."""
        eligible = False
        try:
            eligible = self.postnatal_enrollment.is_eligible
        except AttributeError:
            try:
                eligible = self.antenatal_enrollment.is_eligible
            except AttributeError:
                pass
        return eligible

    def get_visit_reason_no_follow_up_choices(self):
        """ Returns the visit reasons that do not imply any data
        collection; that is, the subject is not available. """
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        del dct[DEATH_VISIT]
        return dct

    def custom_post_update_entry_meta_data(self):
        """Custom methods that manipulate meta data on the post save.

        This method is called in the edc.entry_meta_data signal."""
        if self.reason == OFF_STUDY:
            self.change_to_off_study_visit(self.appointment, 'microbiome_maternal', 'maternaloffstudy')
        elif self.reason == DEATH_VISIT:
            self.change_to_death_visit(
                self.appointment, 'microbiome_maternal', 'maternaloffstudy', 'maternaldeath')
        elif self.reason == UNSCHEDULED:
            self.change_to_unscheduled_visit(self.appointment)
        else:
            self.required_for_maternal_pos()
            self.required_for_maternal_not_pos()

    def required_for_maternal_pos(self):
        if self.enrollment_hiv_status == POS or self.scheduled_rapid_test == POS:
            if self.appointment.visit_definition.code == '1000M':
                model_names = ['maternalclinicalhistory', 'maternalarvhistory', 'maternalarvpreg']
                for model_name in model_names:
                    self.form_is_required(
                        self.appointment,
                        'microbiome_maternal',
                        model_name,
                        message=self.appointment.visit_definition.code)
            elif self.appointment.visit_definition.code == '2000M':
                model_names = ['maternalarvpreg', 'maternallabdelclinic']
                for model_name in model_names:
                    self.form_is_required(
                        self.appointment,
                        'microbiome_maternal',
                        model_name,
                        message=self.appointment.visit_definition.code)
            elif self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                model_names = ['maternalarvpost', 'maternalarvpostadh']
                for model_name in model_names:
                    self.form_is_required(
                        self.appointment,
                        'microbiome_maternal',
                        model_name,
                        message=self.appointment.visit_definition.code)
                self.requisition_is_required(
                    self.appointment,
                    'microbiome_lab',
                    'maternalrequisition',
                    'Viral Load')

    def required_for_maternal_not_pos(self):
        if self.enrollment_hiv_status == NEG and self.scheduled_rapid_test != POS:
            if self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                self.form_is_required(
                    self.appointment,
                    'microbiome_maternal',
                    'rapidtestresult',
                    message=self.appointment.visit_definition.code)

    @property
    def scheduled_rapid_test(self):
        """Returns the value of the \'result\' field of the RapidTestResult.

        This is a scheduled maternal form for on-study participants."""
        RapidTestResult = models.get_model('microbiome_maternal', 'rapidtestresult')
        try:
            obj = RapidTestResult.objects.filter(
                maternal_visit__appointment__registered_subject=self.appointment.registered_subject,
                rapid_test_done=YES,
                result__in=[POS, NEG]).order_by('created').last()
            scheduled_rapid_test = obj.result
        except AttributeError as e:
            if 'result' not in str(e):
                raise AttributeError(str(e))
            scheduled_rapid_test = None
        return scheduled_rapid_test

    @property
    def enrollment_hiv_status(self):
        enrollment_hiv_status = None
        try:
            enrollment_hiv_status = self.postnatal_enrollment.enrollment_hiv_status
        except AttributeError:
            try:
                enrollment_hiv_status = self.antenatal_enrollment.enrollment_hiv_status
            except AttributeError:
                pass
        return enrollment_hiv_status

    @property
    def antenatal_enrollment(self):
        try:
            return AntenatalEnrollment.objects.get(
                registered_subject=self.appointment.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return None

    @property
    def postnatal_enrollment(self):
        try:
            return PostnatalEnrollment.objects.get(
                registered_subject=self.appointment.registered_subject)
        except PostnatalEnrollment.DoesNotExist:
            return None

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Visit'
        verbose_name_plural = 'Maternal Visit'
