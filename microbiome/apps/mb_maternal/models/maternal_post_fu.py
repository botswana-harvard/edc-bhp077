from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc.subject.code_lists.models import WcsDxAdult
from edc_base.audit_trail import AuditTrail
from edc_base.model.fields.custom_fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import YES_NO, GRADING_SCALE
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfInlineModelMixin

from microbiome.apps.mb_list.models import ChronicConditions

from ..managers import MaternalPostFuDxTManager
from ..maternal_choices import DX

from .maternal_crf_model import MaternalCrfModel


class MaternalPostFu(MaternalCrfModel):

    """ A model completed by the user on the mother's General post-partum follow-up. """

    weight_measured = models.CharField(
        verbose_name="Was the mother's weight measured at this visit?",
        max_length=3,
        choices=YES_NO)

    weight_kg = models.DecimalField(
        verbose_name="Enter mother's weight  ",
        max_digits=4,
        decimal_places=1,
        help_text="kg",
        blank=True,
        null=True)

    systolic_bp = models.IntegerField(
        verbose_name="Mother's systolic blood pressure?",
        max_length=3,
        validators=[MinValueValidator(75), MaxValueValidator(220), ],
        help_text="in mm e.g. 120, should be between 75 and 220.")

    diastolic_bp = models.IntegerField(
        verbose_name="Mother's diastolic blood pressure?",
        max_length=3,
        validators=[MinValueValidator(35), MaxValueValidator(130), ],
        help_text="in hg e.g. 80, should be between 35 and 130.")

    breastfed_since = models.CharField(
        verbose_name="Has the mother breastfed since the last attended visit?",
        max_length=3,
        choices=YES_NO)

    mastitis_since = models.CharField(
        verbose_name="If yes,since the last attended scheduled visit,has the mother had mastitis at any time?",
        max_length=3,
        choices=YES_NO)

    chronic_since = models.CharField(
        verbose_name=(
            "Since the last attended scheduled visit, has the mother had any of the "
            "following chronic health conditions, which were NEW diagnoses (never previously reported)?"),
        max_length=3,
        choices=YES_NO)

    chronic = models.ManyToManyField(
        ChronicConditions,
        verbose_name="Select all that apply")

    chronic_other = OtherCharField()

    comment = models.CharField(
        verbose_name="Comment if any additional pertinent information: ",
        max_length=350,
        blank=True,
        null=True)

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Postnatal Follow-Up"
        verbose_name_plural = "Maternal Postnatal Follow-Up"


class MaternalPostFuDx(MaternalCrfModel):

    """ Post-partum follow up of diagnosis. """

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
    who = models.ManyToManyField(
        WcsDxAdult,
        verbose_name="List any new WHO Stage III/IV diagnoses that are not reported")

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Postnatal Follow-Up: Dx"
        verbose_name_plural = "Maternal Postnatal Follow-Up: Dx"


class MaternalPostFuDxT(CrfInlineModelMixin, SyncModelMixin, BaseUuidModel):

    """ Post-partum follow up of diagnosis (transactions). """

    fk_model_attr = 'maternal_post_fu_dx'

    maternal_post_fu_dx = models.ForeignKey(MaternalPostFuDx)

    post_fu_dx = models.CharField(
        verbose_name="Diagnosis",
        max_length=100,
        choices=DX,
        blank=True,
        null=True)

    post_fu_specify = models.CharField(
        verbose_name="Diagnosis specification",
        max_length=100,
        blank=True,
        null=True)

    grade = models.IntegerField(
        verbose_name="Grade",
        max_length=3,
        choices=GRADING_SCALE,
        blank=True,
        null=True)

    hospitalized = models.CharField(
        verbose_name="Hospitalized",
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    objects = MaternalPostFuDxTManager()

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Postnatal Follow-Up: DxT"
        verbose_name_plural = "Maternal Postnatal Follow-Up: DxT"
