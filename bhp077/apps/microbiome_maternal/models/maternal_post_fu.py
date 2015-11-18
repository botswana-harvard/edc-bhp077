from django.db import models
from django.core.urlresolvers import reverse

from edc_constants.choices import YES_NO
from edc.subject.adverse_event.choices import GRADING_SCALE
from edc.subject.code_lists.models import WcsDxAdult
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel

from ..managers import MaternalPostFuDxTManager
from ..maternal_choices import DX
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class MaternalPostFu(MaternalScheduledVisitModel):

    """ General post-partum follow-up. """

    CONSENT_MODEL = MaternalConsent

    mother_weight = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was the mother's weight measured at this visit?",
        help_text="",)
    enter_weight = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name="Enter mother's weight  ",
        help_text="kg",
        blank=True,
        null=True,)
    systolic_bp = models.CharField(
        max_length=3,
        verbose_name="Mother's systolic blood pressure?",
        help_text="in mm e.g. 120",)
    diastolic_bp = models.CharField(
        max_length=3,
        verbose_name="Mother's diastolic blood pressure?",
        help_text="in hg e.g. 80",
    )
    had_mastitis = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("If yes,since the last attended scheduled visit,has the mother had"
                      " mastitis at any time?"),
        help_text="",
        blank=True,
        null=True,)
    comment = models.CharField(
        max_length=350,
        verbose_name="Comment if any additional pertinent information: ",
        blank=True,
        null=True,)

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up"
        verbose_name_plural = "Maternal Postnatal Follow-Up"


class MaternalPostFuDx(MaternalScheduledVisitModel):

    """ Post-partum follow up of diagnosis. """

    maternal_post_fu = models.OneToOneField(MaternalPostFu)

    mother_hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("Has the mother been hospitalized overnight since the last scheduled"
                      " visit (or since discharge after delivery, if this is the"
                      " randomization visit)?"),
        help_text="",)

    new_diagnoses = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("Since the last attended scheduled visit, has the mother had any of"
                      " the following which were NEW (never previously reported, or a NEW"
                      " episode of a previously resolved* diagnosis)"),
        help_text="",)

    who_clinical_stage = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("Since the last attended scheduled visit, has the mother ever had any of"
                      " the diagnoses listed in the WHO Adult/Adolescent HIV clinical staging"
                      " document which are NEW?"),
        help_text="",)
    wcs_dx_adult = models.ManyToManyField(
        WcsDxAdult,
        verbose_name="List any new WHO Stage III/IV diagnoses that are not reported")

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternalpostfudx_change', args=(self.id,))

    def get_report_datetime(self):
        return self.maternal_post_fu.get_report_datetime()

    def get_subject_identifier(self):
        return self.maternal_post_fu.get_subject_identifier()

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up: Dx"
        verbose_name_plural = "Maternal Postnatal Follow-Up: Dx"


class MaternalPostFuDxT(BaseUuidModel):

    """ Post-partum follow up of diagnosis (transactions). """

    maternal_post_fu = models.ForeignKey(MaternalPostFuDx)

    post_fu_dx = models.CharField(
        max_length=100,
        choices=DX,
        verbose_name="Diagnosis",
        blank=True,
        null=True,
        help_text="",)
    post_fu_specify = models.CharField(
        max_length=100,
        verbose_name="Diagnosis specification",
        help_text="",
        blank=True,
        null=True,)
    grade = models.IntegerField(
        max_length=3,
        choices=GRADING_SCALE,
        verbose_name="Grade",
        blank=True,
        null=True,)
    hospitalized = models.CharField(
        choices=YES_NO,
        max_length=3,
        verbose_name="Hospitalized",
        blank=True,
        null=True,
        help_text="",)

    history = AuditTrail()

    objects = MaternalPostFuDxTManager()

    def natural_key(self):
        return (self.post_fu_dx, ) + self.maternal_post_fu.natural_key()

    def get_visit(self):
        return self.maternal_post_fu.get_visit()

    def get_report_datetime(self):
        return self.maternal_post_fu.get_report_datetime()

    def get_subject_identifier(self):
        return self.maternal_post_fu.get_subject_identifier()

    def __unicode__(self):
        return unicode(self.get_visit())

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternalpostfudxt_change', args=(self.id,))

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up: DxT"
        verbose_name_plural = "Maternal Postnatal Follow-Up: DxT"
