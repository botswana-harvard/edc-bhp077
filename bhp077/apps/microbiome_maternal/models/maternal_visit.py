from django.db import models

from edc.entry_meta_data.models import MetaDataMixin
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc.subject.visit_tracking.settings import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_constants.constants import OFF_STUDY, YES, POS, UNSCHEDULED, NEG, DEAD, DEATH_VISIT

from bhp077.apps.microbiome.choices import VISIT_REASON
from bhp077.apps.microbiome_maternal.models import MaternalConsent, PostnatalEnrollment

from .maternal_off_study_mixin import MaternalOffStudyMixin


class MaternalVisit(MetaDataMixin, MaternalOffStudyMixin, RequiresConsentMixin,
                    BaseVisitTracking, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    CONSENT_MODEL = MaternalConsent

    objects = models.Manager()

    history = AuditTrail(True)

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        if not self.check_if_eligible:
            self.reason = OFF_STUDY
        super(MaternalVisit, self).save(*args, **kwargs)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    @property
    def check_if_eligible(self):
        eligible = False
        if self.antenatal_enrollment:
            eligible = self.antenatal_enrollment.check_eligibility()
        if self.postnatal_enrollment:
            eligible = self.postnatal_enrollment.check_eligiblity()
        return eligible

    @property
    def antenatal_enrollment(self):
        AntenatalEnrollment = models.get_model('microbiome_maternal', 'antenatalenrollment')
        try:
            return AntenatalEnrollment.objects.get(registered_subject=self.appointment.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return False

    @property
    def postnatal_enrollment(self):
        try:
            return PostnatalEnrollment.objects.get(
                registered_subject=self.appointment.registered_subject)
        except PostnatalEnrollment.DoesNotExist:
            return False

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
        if self.maternal_hiv_status_pos or self.rapid_test_result_pos():
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
        if self.maternal_hiv_status_neg and self.rapid_test_result_status() in [None, NEG]:
            if self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                self.form_is_required(
                    self.appointment,
                    'microbiome_maternal',
                    'rapidtestresult',
                    message=self.appointment.visit_definition.code)

    def rapid_test_result_pos(self):
        RapidTestResult = models.get_model('microbiome_maternal', 'rapidtestresult')
        try:
            return RapidTestResult.objects.get(
                maternal_visit__appointment__registered_subject=self.appointment.registered_subject,
                rapid_test_done=YES,
                rapid_test_result=POS)
        except RapidTestResult.DoesNotExist:
            return False

    def rapid_test_result_neg(self):
        RapidTestResult = models.get_model('microbiome_maternal', 'rapidtestresult')
        try:
            rapid_test_result_neg = RapidTestResult.objects.filter(
                maternal_visit__appointment__registered_subject=self.appointment.registered_subject,
                rapid_test_done=YES,
                rapid_test_result=NEG).order_by('created').last()
        except AttributeError:
            return None
        return rapid_test_result_neg

    def rapid_test_result_status(self):
        if self.rapid_test_result_pos():
            return POS
        elif self.rapid_test_result_neg():
            return NEG
        return None

    @property
    def maternal_hiv_status_pos(self):
        AntenatalEnrollment = models.get_model('microbiome_maternal', 'antenatalenrollment')
        antenatal_enrollment = None
        maternal_hiv_status_pos = None
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(
                registered_subject=self.appointment.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            pass

        postnatal_enrollment = self.postnatal_enrollment if self.postnatal_enrollment else None
        if antenatal_enrollment:
            maternal_hiv_status_pos = True if (
                (antenatal_enrollment.current_hiv_status == POS and antenatal_enrollment.evidence_hiv_status == YES)
            ) else False
        if postnatal_enrollment:
            maternal_hiv_status_pos = True if (
                (postnatal_enrollment.current_hiv_status == POS and postnatal_enrollment.evidence_hiv_status == YES)
            ) else False
        return maternal_hiv_status_pos

    @property
    def maternal_hiv_status_neg(self):
        maternal_hiv_status_neg = None
        antenatal_enrollment = self.antenatal_enrollment
        postnatal_enrollment = self.postnatal_enrollment if self.postnatal_enrollment else None
        if antenatal_enrollment:
            maternal_hiv_status_neg = True if (
                (antenatal_enrollment.current_hiv_status == NEG and antenatal_enrollment.evidence_hiv_status == YES)
            ) else False
        if postnatal_enrollment:
            maternal_hiv_status_neg = True if (
                (postnatal_enrollment.current_hiv_status == NEG and postnatal_enrollment.evidence_hiv_status == YES)
            ) else False
        return maternal_hiv_status_neg

    def maternal_offstudy_required(self):
        try:
            self.reason = OFF_STUDY if not self.postnatal_enrollment.postnatal_eligible else self.reason
            if self.reason == OFF_STUDY:
                self.scheduled_entry_meta_data_required('microbiome_maternal', 'maternaloffstudy')
        except AttributeError:
            pass

    def maternal_death_required(self):
        if self.reason == DEAD:
            for model_name in ['maternaldeath', 'maternaloffstudy']:
                self.scheduled_entry_meta_data_required('microbiome_maternal', model_name)

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Visit'
        verbose_name_plural = 'Maternal Visit'
