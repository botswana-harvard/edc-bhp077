from django.db import models

from edc.entry_meta_data.models import RequisitionMetaData
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_constants.constants import OFF_STUDY, YES, POS, UNSCHEDULED, NEG, DEAD
from edc.subject.visit_tracking.settings import VISIT_REASON_NO_FOLLOW_UP_CHOICES

from bhp077.apps.microbiome.choices import VISIT_REASON
from bhp077.apps.microbiome_maternal.models import MaternalConsent, PostnatalEnrollment
from bhp077.apps.microbiome_maternal.models.antenatal_enrollment import AntenatalEnrollment
from bhp077.apps.microbiome.classes import MetaDataMixin

from .maternal_off_study_mixin import MaternalOffStudyMixin


class MaternalVisit(MetaDataMixin, MaternalOffStudyMixin, RequiresConsentMixin, BaseVisitTracking, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    CONSENT_MODEL = MaternalConsent

    objects = models.Manager()

    history = AuditTrail(True)

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    @property
    def postnatal_enrollment(self):
        try:
            return PostnatalEnrollment.objects.get(registered_subject=self.appointment.registered_subject)
        except PostnatalEnrollment.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        super(MaternalVisit, self).save(*args, **kwargs)

    def update_entry_meta_data(self):
        """Updates entry meta data if subject is ineligible for Ante/Post natal enrollment."""
        if PostnatalEnrollment.objects.filter(registered_subject=self.appointment.registered_subject).exists():
            if not self.postnatal_enrollment.postnatal_eligible:
                self.maternal_visit_reason_offstudy(self.appointment)
        else:
            antenatal = AntenatalEnrollment.objects.get(registered_subject=self.appointment.registered_subject)
            if not antenatal.antenatal_eligible:
                self.maternal_visit_reason_offstudy(self.appointment)
        if self.reason == UNSCHEDULED:
            self.meta_data_visit_unscheduled(self.appointment)

    def maternal_visit_reason_offstudy(self, appointment):
        """Removes meta data for scheduled forms except for off study."""
        meta_data = self.query_scheduled_meta_data(appointment, appointment.registered_subject)
        for meta in meta_data:
            if not meta.entry.model_name == 'maternaloffstudy':
                meta.delete()
        self.remove_scheduled_requisition(
            RequisitionMetaData.objects.filter(appointment=appointment,
                                               registered_subject=appointment.registered_subject)
        )

    def get_visit_reason_no_follow_up_choices(self):
        """ Returns the visit reasons that do not imply any data
        collection; that is, the subject is not available. """
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        del dct['death']
        return dct

    def rapidtest_result_pos(self):
        RapidTestResult = models.get_model('microbiome_maternal', 'rapidtestresult')
        try:
            return RapidTestResult.objects.get(
                maternal_visit__appointment__registered_subject=self.appointment.registered_subject,
                rapid_test_done=YES,
                rapid_test_result=POS)
        except AttributeError:
            return None

    def rapidtest_result_neg(self):
        RapidTestResult = models.get_model('microbiome_maternal', 'rapidtestresult')
        try:
            rapidtest_result_neg = RapidTestResult.objects.filter(
                maternal_visit__appointment__registered_subject=self.appointment.registered_subject,
                rapid_test_done=YES,
                rapid_test_result=NEG).order_by('created').last()
        except AttributeError:
            return None
        return rapidtest_result_neg

    @property
    def hiv_status_pos_and_evidence_yes(self):
        try:
            return PostnatalEnrollment.objects.get(
                registered_subject=self.appointment.registered_subject,
                current_hiv_status=POS,
                evidence_hiv_status=YES)
        except PostnatalEnrollment.DoesNotExist:
            try:
                return AntenatalEnrollment.objects.get(
                    registered_subject=self.appointment.registered_subject,
                    current_hiv_status=POS,
                    evidence_hiv_status=YES)
            except AntenatalEnrollment.DoesNotExist:
                pass
        return False

    def update_maternal_scheduled_entry_meta_data(self):
        if self.postnatal_enrollment.maternal_hiv_status or self.rapidtest_result_pos:
            if self.appointment.visit_definition.code == '1000M':
                model_names = ['maternalclinicalhistory', 'maternalarvhistory', 'maternalarvpreg']
                for model_name in model_names:
                    self.scheduled_entry_meta_data_required('microbiome_maternal', model_name)
            elif self.appointment.visit_definition.code == '2000M':
                model_names = ['maternalarvpreg', 'maternalarv', 'maternallabdelclinic']
                for model_name in model_names:
                    self.scheduled_entry_meta_data_required('microbiome_maternal', model_name)
            elif self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                model_names = ['maternalarvpost', 'maternalarvpostadh']
                for model_name in model_names:
                    self.scheduled_entry_meta_data_required('microbiome_maternal', model_name)
            self.requisition_is_required('maternalrequisition', 'Viral Load')

        if (
            self.postnatal_enrollment.maternal_rapid_test_result_neg or
            not self.postnatal_enrollment.maternal_hiv_status
        ):
            if self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                self.scheduled_entry_meta_data_required('microbiome_maternal', 'rapidtestresult')

    @property
    def is_participant_off_study(self):
        visit_codes = ['1000M', '2000M', '2010M', '2030M', '2060M', '2090M', '2120M']
        is_off = False
        for i, code in enumerate(visit_codes):
            if self.appointment.visit_definition.code == "1000M":
                break
            else:
                if code == self.appointment.visit_definition.code:
                    MaternalVisit = models.get_model('microbiome_maternal', 'maternalvisit')
                    try:
                        MaternalVisit.objects.get(
                            appointment__registered_subject=self.appointment.registered_subject,
                            appointment__visit_definition__code=visit_codes[i - 1],
                            reason=OFF_STUDY
                        )
                        is_off = True
                        break
                    except MaternalVisit.DoesNotExist:
                        return False
        return is_off

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
