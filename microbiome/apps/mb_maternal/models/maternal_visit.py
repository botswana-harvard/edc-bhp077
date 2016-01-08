from django.core.exceptions import ValidationError
from django.db import models

from edc_meta_data.models import CrfMetaDataMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_constants.constants import (
    YES, POS, UNSCHEDULED, NEG, DEATH_VISIT, COMPLETED_PROTOCOL_VISIT, FAILED_ELIGIBILITY)
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.constants import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from edc_visit_tracking.models import VisitModelMixin, PreviousVisitMixin
from edc_visit_tracking.models.caretaker_fields_mixin import CaretakerFieldsMixin

from microbiome.apps.mb.choices import VISIT_REASON

from ..models import MaternalConsent, PostnatalEnrollment, AntenatalEnrollment


class MaternalVisit(OffStudyMixin, SyncModelMixin, PreviousVisitMixin, CrfMetaDataMixin, RequiresConsentMixin,
                    CaretakerFieldsMixin, VisitModelMixin, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    consent_model = MaternalConsent

    off_study_model = ('mb_maternal', 'MaternalOffStudy')

    history = AuditTrail()

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        if not self.is_eligible():
            self.reason = FAILED_ELIGIBILITY
        self.subject_failed_eligibility()
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

    def subject_failed_eligibility(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if self.is_eligible() and self.reason == FAILED_ELIGIBILITY:
            raise exception_cls(
                "Subject is eligible. Visit reason cannot be 'Failed Eligibility'")

    def get_visit_reason_no_follow_up_choices(self):
        """ Returns the visit reasons that do not imply any data
        collection; that is, the subject is not available. """
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        del dct[DEATH_VISIT]
        return dct

    def custom_post_update_crf_meta_data(self):
        """Custom methods that manipulate meta data on the post save.

        This method is called in the edc_meta_data signal."""
        if self.reason == FAILED_ELIGIBILITY:
            self.change_to_off_study_visit(self.appointment, 'mb_maternal', 'maternaloffstudy')
        elif self.reason == DEATH_VISIT:
            self.change_to_death_visit(
                self.appointment, 'mb_maternal', 'maternaloffstudy', 'maternaldeathreport')
        elif self.reason == UNSCHEDULED:
            self.change_to_unscheduled_visit(self.appointment)
        elif self.reason == COMPLETED_PROTOCOL_VISIT:
            self.crf_is_required(self.appointment, 'mb_maternal', 'maternaloffstudy')
        else:
            self.required_for_maternal_pos()
            self.required_for_maternal_not_pos()
            self.required_labs_for_maternal_neg()
            self.required_forms_for_maternal_neg()

    def required_forms_for_maternal_neg(self):
        """If attempt to change an offstudy to scheduled visit has been successful, ensure that
        necessary forms at 1000M are REQUIRED"""
        if self.enrollment_hiv_status == NEG or self.scheduled_rapid_test == NEG:
            if self.appointment.visit_definition.code == '1000M':
                model_names = [
                    'maternallocator', 'maternaldemographics', 'maternalmedicalhistory',
                    'maternalobstericalhistory']
                for model_name in model_names:
                    self.crf_is_required(
                        self.appointment,
                        'mb_maternal',
                        model_name,
                        message=self.appointment.visit_definition.code)
                self.crf_is_not_required(
                    self.appointment,
                    'mb_maternal',
                    'maternaloffstudy')

    def required_for_maternal_pos(self):
        if self.enrollment_hiv_status == POS or self.scheduled_rapid_test == POS:
            if self.appointment.visit_definition.code == '1000M':
                model_names = ['maternalclinicalhistory', 'maternalarvhistory', 'maternalarvpreg']
                for model_name in model_names:
                    self.crf_is_required(
                        self.appointment,
                        'mb_maternal',
                        model_name,
                        message=self.appointment.visit_definition.code)
            elif self.appointment.visit_definition.code == '2000M':
                model_names = ['maternalarvpreg', 'maternallabdelclinic']
                for model_name in model_names:
                    self.crf_is_required(
                        self.appointment,
                        'mb_maternal',
                        model_name,
                        message=self.appointment.visit_definition.code)
                    for labs in ['Viral Load', 'Breast Milk (Storage)', 'Vaginal swab (Storage)',
                                 'Rectal swab (Storage)', 'Skin Swab (Storage)',
                                 'Vaginal Swab (multiplex PCR)', 'Hematology (ARV)',
                                 'CD4 (ARV)']:
                        self.requisition_is_required(
                            self.appointment,
                            'mb_lab',
                            'maternalrequisition',
                            labs)
            elif self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                model_names = ['maternalarvpost', 'maternalarvpostadh']
                for model_name in model_names:
                    self.crf_is_required(
                        self.appointment,
                        'mb_maternal',
                        model_name,
                        message=self.appointment.visit_definition.code)
                self.requisition_is_required(
                    self.appointment,
                    'mb_lab',
                    'maternalrequisition',
                    'Viral Load')

    def required_for_maternal_not_pos(self):
        if self.enrollment_hiv_status == NEG and self.scheduled_rapid_test != POS:
            if self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                self.crf_is_required(
                    self.appointment,
                    'mb_maternal',
                    'rapidtestresult',
                    message=self.appointment.visit_definition.code)

    def required_labs_for_maternal_neg(self):
        if self.enrollment_hiv_status == NEG and self.scheduled_rapid_test != POS:
            if self.appointment.visit_definition.code == '2000M':
                for labs in ['Breast Milk (Storage)', 'Vaginal swab (Storage)',
                             'Rectal swab (Storage)', 'Skin Swab (Storage)',
                             'Vaginal Swab (multiplex PCR)', 'Hematology (ARV)',
                             'CD4 (ARV)']:
                    self.requisition_is_required(
                        self.appointment,
                        'mb_lab',
                        'maternalrequisition',
                        labs)
            if self.appointment.visit_definition.code == '2010M':
                self.requisition_is_required(
                    self.appointment,
                    'mb_lab',
                    'maternalrequisition',
                    'Breast Milk (Storage)')

    @property
    def scheduled_rapid_test(self):
        """Returns the value of the \'result\' field of the RapidTestResult.

        This is a scheduled maternal form for on-study participants."""
        RapidTestResult = models.get_model('mb_maternal', 'rapidtestresult')
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
        app_label = 'mb_maternal'
        verbose_name = 'Maternal Visit'
