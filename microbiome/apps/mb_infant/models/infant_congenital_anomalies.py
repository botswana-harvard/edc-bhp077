from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.choices import CONFIRMED_SUSPECTED

from microbiome.apps.mb.choices import (
    CNS_ABNORMALITIES, FACIAL_DEFECT, CLEFT_DISORDER, MOUTH_UP_GASTROINT_DISORDER,
    CARDIOVASCULAR_DISORDER, RESPIRATORY_DEFECT, LOWER_GASTROINTESTINAL_ABNORMALITY,
    FEM_GENITAL_ANOMALY, MALE_GENITAL_ANOMALY, RENAL_ANOMALY, MUSCULOSKELETAL_ABNORMALITY,
    SKIN_ABNORMALITY, TRISOME_CHROSOMESOME_ABNORMALITY, OTHER_DEFECT)

from ..managers import InfantInlineModelManager

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantCongenitalAnomalies(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's congenital anomalies. """

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies"


class BaseCnsItem(BaseUuidModel):
    congenital_anomalies = models.ForeignKey(InfantCongenitalAnomalies)

    objects = InfantInlineModelManager()

    history = AuditTrail()

    def natural_key(self):
        return self.get_visit().natural_key()

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


class InfantCns(BaseCnsItem):

    cns = models.CharField(
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

    cns_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Cns"


class InfantFacialDefect(BaseCnsItem):

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

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Facial"


class InfantCleftDisorder(BaseCnsItem):

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

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Cleft"


class InfantMouthUpGi(BaseCnsItem):

    mouth_up_gi = models.CharField(
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

    mouth_up_gi_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:MouthUp"


class InfantCardioDisorder(BaseCnsItem):

    cardio_disorder = models.CharField(
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

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Cardio"


class InfantRespiratoryDefect(BaseCnsItem):

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

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Respiratory"


class InfantLowerGi(BaseCnsItem):

    lower_gi = models.CharField(
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

    lower_gi_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify",
        blank=True,
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Lower GI"


class InfantFemaleGenital(BaseCnsItem):

    female_genital = models.CharField(
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

    female_genital_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Female Gen"


class InfantMaleGenital(BaseCnsItem):

    male_genital = models.CharField(
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

    male_genital_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies:Male Gen"


class InfantRenal(BaseCnsItem):

    renal = models.CharField(
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

    renal_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies: Renal"


class InfantMusculoskeletal(BaseCnsItem):

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

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies: Musculo-sk"


class InfantSkin(BaseCnsItem):

    skin = models.CharField(
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

    skin_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies: Skin"


class InfantTrisomies(BaseCnsItem):

    trisomies = models.CharField(
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

    trisomies_other = OtherCharField(
        max_length=250,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies: Trisomes"


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

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Congenital Anomalies: Other"
