from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.validators import datetime_not_future
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import YES_NO, YES_NO_NA_SPECIFY, YES_NO_UNKNOWN


class MaternalLabourDel(BaseUuidModel):

    """ Maternal Labor and Delivery which triggers registration of infants.

    .. note:: This model allocates infant identifiers. Check admin.py :func:`save_model` method
              for bhp_identifier class access."""

    delivery_datetime = models.DateTimeField(
        verbose_name="Date and time of delivery :",
        help_text="If TIME unknown, estimate",
        validators=[
            datetime_not_future, ],
    )

    del_time_is_est = models.CharField(
        verbose_name="Is the delivery TIME estimated?",
        max_length=3,
        choices=YES_NO,
        help_text="",
    )

    labour_hrs = models.CharField(
        verbose_name="How long prior to to delivery, in HRS, did labour begin? ",
        max_length=10,
        help_text="For multiple births, time of delivery = time first infant born",
    )

    del_mode = models.CharField(
        verbose_name="Mode of delivery  ",
        max_length=25,
        help_text="",
    )

    has_ga = models.CharField(
        verbose_name='Is the gestational age at delivery known?',
        max_length=10,
        choices=YES_NO,
        help_text="If known, complete below",
    )

    ga = models.IntegerField(
        verbose_name="Gestational Age at Delivery  ",
        null=True,
        blank=True,
        help_text="in weeks",
    )

    del_hosp = models.CharField(
        verbose_name="Where did the participant deliver? ",
        max_length=25,
        help_text="If 'Other health facility' or 'Other', specify below",
    )

    del_hosp_other = OtherCharField()

    has_urine_tender = models.CharField(
        max_length=10,
        choices=YES_NO_UNKNOWN,
        verbose_name="Was uterine tenderness recorded? ",
        help_text="",
    )

    labr_max_temp = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="Indicate the maximum temperature of mother during labour",
        help_text="In degrees Celcius. -1 = unknown",
    )

    has_chorioamnionitis = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was chorio-amnionitis suspected? ",
        help_text="",
    )

    has_del_comp = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Were there other complications at delivery? ",
        help_text="( if 'YES' continue. Otherwise go to question 16 )",
    )

    del_comp = models.ManyToManyField(
        verbose_name="If so, select the complication ",
        help_text="",

    )

    del_comp_other = models.TextField(
        max_length=250,
        verbose_name="if other, describe the complication",
        blank=True,
        null=True,
    )

    live_infants = models.IntegerField(
        verbose_name="How many live babies did the mother deliver? ",
        help_text="",
    )

    live_infants_to_register = models.IntegerField(
        verbose_name="How many babies are registering to the study? ",
        help_text="",
    )

    still_borns = models.IntegerField(
        verbose_name="How many stillbirths did the mother deliver?  ",
        help_text="( if '>0' continue. Otherwise go to question 21 )",
    )

    still_born_has_congen_abn = models.CharField(
        max_length=3,
        choices=YES_NO_NA_SPECIFY,
        verbose_name="If any stillborns, did any have a congenital abnormality noted? ",
        help_text="",
        blank=True,
        null=True,
        default="N/A",
    )

    still_born_congen_abn = OtherCharField(
        verbose_name="If yes, specify;",
        blank=True,
        null=True,
    )

    del_comment = models.TextField(
        max_length=250,
        verbose_name="List any addtional information about the labour and delivery (mother only) ",
        blank=True,
        null=True,
    )

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information ",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = 'microbiome'
        verbose_name = "Maternal Labour & Delivery"


class MaternalLabDelMed(BaseUuidModel):

    """ Medical history collected during labor and delivery. """

    has_health_cond = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Has the mother been newly diagnosed (during this pregnancy) "
        "with any major chronic health condition(s) that remain ongoing?",
        help_text="if yes answer Question 4, otherwise go to Question 6",
    )

    health_cond = models.ManyToManyField(
        verbose_name="Select all that apply ",
        help_text="",
    )

    health_cond_other = OtherCharField()
    has_ob_comp = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy, did the mother have any of the following "
        "obstetrical complications? (in 7)",
        help_text="",
    )

    ob_comp = models.ManyToManyField(
        verbose_name="Select all that apply",
        help_text="",
    )

    ob_comp_other = models.TextField(
        max_length=250,
        blank=True,
        null=True,
    )

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information ",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Labour & Delivery: MedHistory"


class MaternalLabDelClinic(BaseUuidModel):

    """ Laboratory and other clinical information collected during labor and delivery"""

    maternal_lab_del = models.OneToOneField(MaternalLabourDel)

    has_cd4 = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy did the mother have at least one CD4 count performed (outside the study)? ",
        help_text="( if 'YES' continue. Otherwise go to question 6 )",
    )

    cd4_date = models.DateField(
        verbose_name="Date of most recent CD4 test? ",
        help_text="",
        blank=True,
        null=True
    )

    cd4_result = models.CharField(
        max_length=35,
        verbose_name="Result of most recent CD4 test",
        blank=True,
        null=True
    )

    has_vl = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy did the mother have a viral load perfomed (outside the study)? ",
        help_text="(if 'YES' continue. Otherwise go to question 9)",
    )

    vl_date = models.DateField(
        verbose_name="If yes, Date of most recent VL test? ",
        help_text="",
        blank=True,
        null=True
    )

    vl_result = models.CharField(
        max_length=35,
        verbose_name="Result of most recent VL test",
        blank=True,
        null=True
    )

    took_suppliments = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother take any of the following during this pregnancy?(in 10)   ",
        help_text="( if 'YES' continue. Otherwise go to question 11 )",
    )

    suppliment = models.ManyToManyField(
        verbose_name="Select all that apply ",
        help_text="",
    )

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information ",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Labour & Delivery: ClinHist"


class MaternalLabDelDx(BaseUuidModel):

    """ Diagnosis during pregnancy collected during labor and delivery. """

    has_preg_dx = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy, did the mother have any of the following? ",
        help_text="If yes, Select all that apply in the table, only report grade 3 or 4 diagnoses",
    )

    has_who_dx = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="During this pregnancy, did the mother have any new diagnoses "
        "listed in the WHO Adult/Adolescent HIV clinical staging document which "
        "is/are NOT reported below in Question 5 ",
        help_text="If yes, answer 4, otherwise go to Question 5",
    )

    wcs_dx_adult = models.ManyToManyField(
        verbose_name="List any new WHO Stage III/IV diagnoses that are not reported in Question 3 below:  ",
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Labour & Delivery: Preg Dx"


class MaternalLabDelDxT (BaseUuidModel):

    """ Diagnosis during pregnancy collected during labor and delivery (transactions). """

    lab_del_dx = models.CharField(
        max_length=175,
        verbose_name="Diagnosis",
        help_text="",
    )

    lab_del_dx_specify = models.CharField(
        max_length=50,
        verbose_name="Diagnosis specification",
        help_text="",
        blank=True,
        null=True,
    )

    grade = models.IntegerField(
        verbose_name="Grade",
    )

    hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Hospitalized",
        help_text="",
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Labour & Delivery: Preg DxT"
