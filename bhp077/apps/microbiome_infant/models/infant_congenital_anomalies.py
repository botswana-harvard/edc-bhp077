from django.db import models

from edc.base.model.fields import OtherCharField
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.choices import CONFIRMED_SUSPECTED

from bhp077.apps.microbiome.choices import (
    CNS_ABNORMALITIES, FACIAL_DEFECT, CLEFT_DISORDER, MOUTH_UP_GASTROINT_DISORDER,
    CARDIOVASCULAR_DISORDER, RESPIRATORY_DEFECT, LOWER_GASTROINTESTINAL_ABNORMALITY,
    FEM_GENITAL_ANOMALY, MALE_GENITAL_ANOMALY, RENAL_ANOMALY, MUSCULOSKELETAL_ABNORMALITY,
    SKIN_ABNORMALITY, TRISOME_CHROSOMESOME_ABNORMALITY, OTHER_DEFECT)

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantCongenitalAnomalies(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's congenital anomalies. """

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies"


class BaseCnsItem(BaseUuidModel):
    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    objects = models.Manager()

    history = AuditTrail()

    def get_visit(self):
        return self.congenital_anomalies.get_visit()

    def get_report_datetime(self):
        return self.congenital_anomalies.get_report_datetime()

    def get_subject_identifier(self):
        return self.congenital_anomalies.get_subject_identifier()

    def __unicode__(self):
        return unicode(self.get_visit())

    class Meta:
        abstract = True


class InfantCnsAbnormalityItems(BaseCnsItem):

    cns_abnormality = models.CharField(
        max_length=250,
        choices=CNS_ABNORMALITIES,
        verbose_name="Central nervous system abnormality",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    cns_abnormality_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Cns"


class InfantFacialDefectItems(BaseCnsItem):

    facial_defect = models.CharField(
        max_length=250,
        choices=FACIAL_DEFECT,
        verbose_name="Facial defects",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    facial_defects_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Facial"


class InfantCleftDisorderItems(BaseCnsItem):

    cleft_disorder = models.CharField(
        max_length=250,
        choices=CLEFT_DISORDER,
        verbose_name="Cleft disorders",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    cleft_disorders_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Cleft"


class InfantMouthUpGastrointestinalItems(BaseCnsItem):

    mouth_up_gastrointest = models.CharField(
        max_length=250,
        choices=MOUTH_UP_GASTROINT_DISORDER,
        verbose_name="Mouth and upper gastrointestinal disorders",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    mouth_up_gastrointest_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:MouthUpp"


class InfantCardiovascularDisorderItems(BaseCnsItem):

    cardiovascular_disorder = models.CharField(
        max_length=250,
        choices=CARDIOVASCULAR_DISORDER,
        verbose_name="Cardiovascular disorders",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    cardiovascular_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Cardio"


class InfantRespiratoryDefectItems(BaseCnsItem):

    respiratory_defect = models.CharField(
        max_length=250,
        choices=RESPIRATORY_DEFECT,
        verbose_name="Respiratory defects",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    respiratory_defects_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Respitarory"


class InfantLowerGastrointestinalItems(BaseCnsItem):

    lower_gastrointestinal = models.CharField(
        max_length=250,
        choices=LOWER_GASTROINTESTINAL_ABNORMALITY,
        verbose_name="Lower gastrointestinal abnormalities",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    lower_gastrointestinal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:LowerGast"


class InfantFemaleGenitalAnomalyItems(BaseCnsItem):

    female_genital_anomal = models.CharField(
        max_length=250,
        choices=FEM_GENITAL_ANOMALY,
        verbose_name="Female genital anomaly",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    female_genital_anomal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:FemaleGen"


class InfantMaleGenitalAnomalyItems(BaseCnsItem):

    male_genital_anomal = models.CharField(
        max_length=250,
        choices=MALE_GENITAL_ANOMALY,
        verbose_name="Male genital anomaly",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    male_genital_anomal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:MaleGen"


class InfantRenalAnomalyItems(BaseCnsItem):

    renal_amomalies = models.CharField(
        max_length=250,
        choices=RENAL_ANOMALY,
        verbose_name="Renal anomalies",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    renal_amomalies_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Renal"


class InfantMusculoskeletalAbnormalItems(BaseCnsItem):

    musculo_skeletal = models.CharField(
        max_length=250,
        choices=MUSCULOSKELETAL_ABNORMALITY,
        verbose_name="Musculo-skeletal abnomalities",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    musculo_skeletal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Musculosk"


class InfantSkinAbnormalItems(BaseCnsItem):

    skin_abnormality = models.CharField(
        max_length=250,
        choices=SKIN_ABNORMALITY,
        verbose_name="Skin abnormalities",
        help_text="Excludes cafe au lait spots, Mongolian spots, port wine stains, "
        "nevus, hemangloma <4 cm in diameter. If hemangloma is >4 cm, specify",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    skin_abnormality_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Skin"


class InfantTrisomiesChromosomeItems(BaseCnsItem):

    triso_chromo_abnormal = models.CharField(
        max_length=250,
        choices=TRISOME_CHROSOMESOME_ABNORMALITY,
        verbose_name="Trisomies / chromosomes abnormalities",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    triso_chromo_abnormal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Trisomes"


class InfantOtherAbnormalityItems(BaseCnsItem):

    other_abnormalities = models.CharField(
        max_length=250,
        choices=OTHER_DEFECT,
        verbose_name="Other",
        blank=True,
        null=True,
    )

    abnormality_status = models.CharField(
        max_length=35,
        choices=CONFIRMED_SUSPECTED,
        verbose_name="Abnormality status",
        blank=True,
        null=True,
    )

    other_abnormalities_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Congenital Anomalies:Other"
