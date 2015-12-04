from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from edc.subject.adverse_event.choices import GRADING_SCALE
from edc.subject.code_lists.models import WcsDxAdult
from edc_base.audit_trail import AuditTrail
from edc_base.model.fields.custom_fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import YES_NO

from bhp077.apps.microbiome_list.models import ChronicConditions

from ..managers import MaternalPostFuDxTManager
from ..maternal_choices import DX

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class MaternalPostFu(MaternalScheduledVisitModel):

    """ A model completed by the user on the mother's General post-partum follow-up. """

    CONSENT_MODEL = MaternalConsent

    weight_measured = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was the mother's weight measured at this visit?",
        help_text="",)

    weight_kg = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name="Enter mother's weight  ",
        help_text="kg",
        blank=True,
        null=True,)

    systolic_bp = models.IntegerField(
        max_length=3,
        verbose_name="Mother's systolic blood pressure?",
        validators=[MinValueValidator(75), MaxValueValidator(220), ],
        help_text="in mm e.g. 120, should be between 75 and 220.",
    )

    diastolic_bp = models.IntegerField(
        max_length=3,
        verbose_name="Mother's diastolic blood pressure?",
        validators=[MinValueValidator(35), MaxValueValidator(130), ],
        help_text="in hg e.g. 80, should be between 35 and 130.",
    )

    breastfed_since = models.CharField(
        max_length=3,
        verbose_name="Has the mother breastfed since the last attended visit?",
        choices=YES_NO,
        help_text="",
    )

    mastitis_since = models.CharField(
        max_length=3,
        verbose_name="If yes,since the last attended scheduled visit,has the mother had mastitis at any time?",
        choices=YES_NO,
        help_text="",
    )

    chronic_cond_since = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=(
            "Since the last attended scheduled visit, has the mother had any of the "
            "following chronic health conditions, which were NEW diagnoses (never previously reported)?"),
        help_text="",
    )

    chronic_cond = models.ManyToManyField(
        ChronicConditions,
        verbose_name="Select all that apply",
        help_text="",
    )

    chronic_cond_other = OtherCharField()

    comment = models.CharField(
        max_length=350,
        verbose_name="Comment if any additional pertinent information: ",
        blank=True,
        null=True,)

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up"
        verbose_name_plural = "Maternal Postnatal Follow-Up"


class MaternalPostFuDx(MaternalScheduledVisitModel):

    """ Post-partum follow up of diagnosis. """

    maternal_post_fu = models.OneToOneField(MaternalPostFu)

    hospitalized_since = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("Has the mother been hospitalized overnight since the last scheduled"
                      " visit (or since discharge after delivery, if this is the"
                      " randomization visit)?"),
        help_text="",)

    new_dx_since = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("Since the last attended scheduled visit, has the mother had any of"
                      " the following which were NEW (never previously reported, or a NEW"
                      " episode of a previously resolved* diagnosis)"),
        help_text="",)

    new_wcs_dx_since = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("Since the last attended scheduled visit, has the mother ever had any of"
                      " the diagnoses listed in the WHO Adult/Adolescent HIV clinical staging"
                      " document which are NEW?"),
        help_text="",)
    wcs_dx_adult = models.ManyToManyField(
        WcsDxAdult,
        verbose_name="List any new WHO Stage III/IV diagnoses that are not reported")

    objects = models.Manager()

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

    objects = MaternalPostFuDxTManager()

    history = AuditTrail()

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

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up: DxT"
        verbose_name_plural = "Maternal Postnatal Follow-Up: DxT"
