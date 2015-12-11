from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc.subject.code_lists.models import WcsDxAdult
from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from bhp077.apps.microbiome.choices import DX_MATERNAL
from bhp077.apps.microbiome_list.models import Suppliments, HealthCond, ObComp
from bhp077.apps.microbiome_maternal.models import MaternalConsent

from ..maternal_choices import DELIVERY_HEALTH_FACILITY

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel


class MaternalLabourDel(MaternalScheduledVisitModel):

    """ A model completed by the user on Maternal Labor and Delivery which triggers registration of infants. """

    CONSENT_MODEL = MaternalConsent

    delivery_datetime = models.DateTimeField(
        verbose_name="Date and time of delivery :",
        help_text="If TIME unknown, estimate",
        validators=[
            datetime_not_future, ])

    delivery_time_estimated = models.CharField(
        verbose_name="Is the delivery TIME estimated?",
        max_length=3,
        choices=YES_NO,
        help_text="")

    labour_hrs = models.CharField(
        verbose_name="How long prior to to delivery, in HRS, did labour begin? ",
        max_length=10,
        help_text="")

    delivery_hospital = models.CharField(
        verbose_name="Where did the participant deliver? ",
        max_length=65,
        choices=DELIVERY_HEALTH_FACILITY,
        help_text="If 'OTHER', specify below",)
    delivery_hospital_other = OtherCharField()

    has_uterine_tender = models.CharField(
        max_length=10,
        choices=YES_NO_UNKNOWN,
        verbose_name="Was uterine tenderness recorded? ",
        help_text="")

    has_temp = models.CharField(
        verbose_name="Is the maximum temparature known?",
        max_length=3,
        choices=YES_NO,
        help_text="")

    labour_max_temp = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="Indicate the maximum temperature of mother during labour",
        help_text="",
        validators=[MinValueValidator(36.5), MaxValueValidator(39.0), ],
        blank=True,
        null=True,
    )

    has_chorioamnionitis = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was chorio-amnionitis suspected? ",
        help_text="")

    delivery_complications = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Were there other complications at delivery? ",
        help_text="")

    live_infants_to_register = models.IntegerField(
        verbose_name="How many babies are you registering to the study? ",
        help_text="")

    delivery_comment = models.TextField(
        max_length=250,
        verbose_name="List any additional information about the labour and delivery (mother only) ",
        blank=True,
        null=True)

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information ",
        blank=True,
        null=True)

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Labour & Delivery"
        verbose_name_plural = "Maternal Labour & Delivery"


class MaternalLabDelMed(MaternalScheduledVisitModel):

    """ Medical history collected during labor and delivery. """

    CONSENT_MODEL = MaternalConsent

    has_health_cond = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Has the mother been newly diagnosed (during this pregnancy) "
        "with any major chronic health condition(s) that remain ongoing?",
        help_text="")

    health_cond = models.ManyToManyField(
        HealthCond,
        verbose_name="Select all that apply ",
        help_text="",
    )

    health_cond_other = OtherCharField()

    has_ob_comp = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy, did the mother have any of the following "
        "obstetrical complications?",
        help_text="")

    ob_comp = models.ManyToManyField(
        ObComp,
        verbose_name="Select all that apply",
        help_text="",
    )

    ob_comp_other = OtherCharField()

    took_suppliments = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother take any of the following medications during this pregnancy?",
        help_text="")

    suppliments = models.ManyToManyField(
        Suppliments,
        verbose_name="Please select relevant medications taken:",
        help_text="Select all that apply")

    suppliments_other = OtherCharField()

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information ",
        blank=True,
        null=True)

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Labour & Delivery: Medical History"
        verbose_name_plural = "Maternal Labour & Delivery: Medical History"


class MaternalLabDelClinic(MaternalScheduledVisitModel):

    """ Laboratory and other clinical information collected during labor and delivery.
    for HIV +ve mothers ONLY"""

    CONSENT_MODEL = MaternalConsent

#     maternal_lab_del = models.OneToOneField(MaternalLabourDel)

    has_cd4 = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("During this pregnancy did the mother have at least one CD4 count"
                      " performed (outside the study)? "),
        help_text="")

    cd4_date = models.DateField(
        verbose_name="Date of most recent CD4 test? ",
        help_text="",
        blank=True,
        null=True)

    cd4_result = models.CharField(
        max_length=35,
        verbose_name="Result of most recent CD4 test",
        blank=True,
        null=True)

    has_vl = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("During this pregnancy did the mother have a viral load perfomed"
                      " (outside the study)? "),
        help_text="(if 'YES' continue. Otherwise go to question 9)")

    vl_date = models.DateField(
        verbose_name="If yes, Date of most recent VL test? ",
        help_text="",
        blank=True,
        null=True)

    vl_detectable = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        verbose_name="Was the viral load detectable?",
        help_text="")

    vl_result = models.CharField(
        max_length=35,
        verbose_name="Result of most recent VL test",
        blank=True,
        null=True)

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information ",
        blank=True,
        null=True)

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Labour & Delivery: Clinical History"
        verbose_name_plural = "Maternal Labour & Delivery: Clinical History"


class MaternalLabDelDx(MaternalScheduledVisitModel):

    """ Diagnosis during pregnancy collected during labor and delivery.
    This is for HIV positive mothers only"""

    CONSENT_MODEL = MaternalConsent

    has_who_dx = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy, did the mother have any new diagnoses "
        "listed in the WHO Adult/Adolescent HIV clinical staging document which "
        "is/are NOT reported?",
        help_text="")

    wcs_dx_adult = models.ManyToManyField(
        WcsDxAdult,
        verbose_name="List any new WHO Stage III/IV diagnoses that are not reported in Question 3 below:  ",
    )

    has_preg_dx = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy, did the mother have any of the following diagnoses? ",
        help_text="If yes, Select all that apply in the table, only report grade 3 or 4 diagnoses")

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Labour & Delivery: Preg Dx"
        verbose_name_plural = "Maternal Labour & Delivery: Preg Dx"


class MaternalLabDelDxT (BaseUuidModel):

    """ Diagnosis during pregnancy collected during labor and delivery (transactions). """

    CONSENT_MODEL = MaternalConsent

    maternal_lab_del_dx = models.OneToOneField(MaternalLabDelDx)

    lab_del_dx = models.CharField(
        max_length=175,
        verbose_name="Diagnosis",
        choices=DX_MATERNAL,
        help_text=""
    )

    lab_del_dx_specify = models.CharField(
        max_length=50,
        verbose_name="Diagnosis specification",
        help_text="",
        blank=True,
        null=True
    )

    grade = models.IntegerField(
        verbose_name="Grade",
    )

    hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Hospitalized",
        help_text="")

    objects = models.Manager()

    history = AuditTrail()

    def get_visit(self):
        return self.maternal_lab_del_dx.maternal_visit

    def get_report_datetime(self):
        return self.maternal_lab_del_dx.maternal_visit.report_datetime

    def get_subject_identifier(self):
        return self.maternal_lab_del_dx.maternal_visit.subject_identifier

    def __unicode__(self):
        return unicode(self.get_visit())

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Labour & Delivery: Preg DxT"
        verbose_name_plural = "Maternal Labour & Delivery: Preg DxT"
