from django.db import models

from edc_base.model.model import BaseUuidModel

from .infant_visit import InfantVisit


class InfantCongenitalAnomalies(BaseUuidModel):

    infant_visit = models.OneToOneField(InfantVisit)

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies"


class BaseCnsItem(BaseUuidModel):
    """Adds in method to get mother's subject_identifier for confirming the consent (see bhp_consent)."""

    report_datetime = models.DateTimeField(
        verbose_name="Visit Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
        ],
    )

    class Meta:
        abstract = True


class InfantCnsAbnormalityItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    cns_abnormality = models.CharField(
        max_length=250,
        verbose_name="Central nervous system abnormality",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    cns_abnormality_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "mpepu_infant"
        verbose_name = "Infant Congenital Anomalies:Cns"


class InfantFacialDefectItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    facial_defect = models.CharField(
        max_length=250,
        verbose_name="Facial defects",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    facial_defects_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "mpepu_infant"
        verbose_name = "Infant Congenital Anomalies:Facial"


class InfantCleftDisorderItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    cleft_disorder = models.CharField(
        max_length=250,
        verbose_name="Cleft disorders",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    cleft_disorders_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "mpepu_infant"
        verbose_name = "Infant Congenital Anomalies:Cleft"


class InfantMouthUpGastrointestinalItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    mouth_up_gastrointest = models.CharField(
        max_length=250,
        verbose_name="Mouth and upper gastrointestinal disorders",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    mouth_up_gastrointest_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True)

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:MouthUpp"


class InfantCardiovascularDisorderItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    cardiovascular_disorder = models.CharField(
        max_length=250,
        verbose_name="Cardiovascular disorders",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    cardiovascular_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:Cardio"


class InfantRespiratoryDefectItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    respiratory_defect = models.CharField(
        max_length=250,
        verbose_name="Respiratory defects",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    respiratory_defects_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:Respitarory"


class InfantLowerGastrointestinalItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    lower_gastrointestinal = models.CharField(
        max_length=250,
        verbose_name="Lower gastrointestinal abnormalities",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    lower_gastrointestinal_other = models.CharField(
        max_length=250,
        verbose_name="if other specify",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:LowerGast"


class InfantFemaleGenitalAnomalyItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    female_genital_anomal = models.CharField(
        max_length=250,
        verbose_name="Female genital anomaly",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    female_genital_anomal_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:FemaleGen"


class InfantMaleGenitalAnomalyItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    male_genital_anomal = models.CharField(
        max_length=250,
        verbose_name="Male genital anomaly",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    male_genital_anomal_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:MaleGen"


class InfantRenalAnomalyItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    renal_amomalies = models.CharField(
        max_length=250,
        verbose_name="Renal anomalies",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    renal_amomalies_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:Renal"


class InfantMusculoskeletalAbnormalItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    musculo_skeletal = models.CharField(
        max_length=250,
        verbose_name="Musculo-skeletal abnomalities",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    musculo_skeletal_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:Musculosk"


class InfantSkinAbnormalItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    skin_abnormality = models.CharField(
        max_length=250,
        verbose_name="Skin abnormalities",
        help_text="Excludes cafe au lait spots, Mongolian spots, port wine stains, nevus, hemangloma <4 cm in diameter. If hemangloma is >4 cm, specify",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    skin_abnormality_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:Skin"


class InfantTrisomiesChromosomeItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    triso_chromo_abnormal = models.CharField(
        max_length=250,
        verbose_name="Trisomies / chromosomes abnormalities",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    triso_chromo_abnormal_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:Trisomes"


class InfantOtherAbnormalityItems(BaseCnsItem):

    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    other_abnormalities = models.CharField(
        max_length=250,
        verbose_name="Other",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    other_abnormalities_other = models.CharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Congenital Anomalies:Other"
