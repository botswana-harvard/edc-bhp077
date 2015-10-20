from django.db import models
from django.core.urlresolvers import reverse

from edc_constants.choices import YES_NO

from microbiome.choices import REASON_NOT_RECEIVED_VACCINATION, YES_NOT_SCHEDULED_NOT_RECEIVED

from .infant_fu import InfantFu
from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantFuImmunizations(InfantScheduledVisitModel):

    infant_fu = models.OneToOneField(InfantFu)

    vaccines_received = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Since the last attended scheduled visit,did the child recieve any of the following vaccinations",
        help_text="",
    )

    vitamin_a_vaccine = models.CharField(
        max_length=20,
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        verbose_name="Vitamin A vaccination",
        help_text="Given to children between 6 and 59 months at intervals of 6-11 months, 12-17 months, "
        "18-29 months, 24-29 months, 30-35 months, 36-41 months, 42-47 months, 48-53 months, 54-59 months. ",
    )

    reason_not_received_vita_a = models.CharField(
        max_length=50,
        verbose_name="Reason Vitamin A vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        blank=True,
        null=True,
        help_text="Give reason if the answer for previous question is Not Received",
    )

    bcg_vaccine = models.CharField(
        max_length=20,
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        verbose_name="BCG vaccine",
        help_text="Given at birth or within first few days after birth."
    )

    reason_not_received_bcg = models.CharField(
        verbose_name="Reason BCG vaccine not received",
        max_length=50,
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    hepatitis_b_vaccine = models.CharField(
        max_length=20,
        verbose_name="Hepatitis B vaccine",
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        help_text="Should receive at birth, 2 months, 3 months, and 4 months,"
        "but if late, can still receive up to four vaccinations.",
    )

    reason_not_received_hepatitis_b = models.CharField(
        max_length=50,
        verbose_name="Reason Hepatitis B vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    dpt_vaccine = models.CharField(
        max_length=20,
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        verbose_name="Diphtheria, Pertussis and Tetanus",
        help_text="Should receive at 2, 3 and 4 months of life. ",
    )

    reason_not_received_dpt = models.CharField(
        max_length=50,
        verbose_name="Reason Diphtheria, Pertussis and Tetanus vaccines not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    haemophilus_influenza_b_vaccine = models.CharField(
        max_length=20,
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        verbose_name="Haemophilus Influenza B Vaccine",
        help_text="Should receive at 2, 3 and 4 months of life or later.",
    )

    reason_not_received_haemophilus = models.CharField(
        max_length=50,
        verbose_name="Reason Haemophilus Influenza B vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    pneumonia_conjugated_vaccine = models.CharField(
        max_length=20,
        verbose_name="Pneumonia Conjugated Vaccine",
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        help_text="Should receive at 2, 3 and 4 months of life. ",
    )

    reason_not_received_pcv = models.CharField(
        max_length=50,
        verbose_name="Reason Pneumonia Conjugated Vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    polio_vaccine = models.CharField(
        max_length=20,
        verbose_name="Polio vaccine",
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        help_text="Should receive at 2, 3, 4 and 18 months of life.",
    )

    reason_not_received_polio = models.CharField(
        max_length=50,
        verbose_name="Reason Polio vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    rotavirus_vaccine = models.CharField(
        max_length=20,
        verbose_name="Rotavirus vaccine",
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        help_text="Should receive at 2 and 3 months of life.",
    )

    reason_not_received_rotavirus = models.CharField(
        max_length=50,
        verbose_name="Reason Rotavirus vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    measles_vaccine = models.CharField(
        max_length=20,
        verbose_name="Measles vaccine",
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        help_text="Should receive at 9 and 18 months",
    )

    reason_not_received_measles = models.CharField(
        max_length=50,
        verbose_name="Reason Measles vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    pentavalent_vaccine = models.CharField(
        max_length=20,
        verbose_name="Pentavalent vaccine",
        choices=YES_NOT_SCHEDULED_NOT_RECEIVED,
        help_text="Should receive at 2, 3 and 4 months of life.",
    )

    reason_not_received_pentavalent = models.CharField(
        max_length=50,
        verbose_name="Reason Pentavalent vaccine not received",
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    comments = models.TextField(
        max_length=500,
        verbose_name="Comment",
        blank=True,
        null=True,
    )

    def __str__(self):
        return "%s" % (self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantfumed_change', args=(self.id,))

    class Meta:
        app_label = "infant"
        verbose_name = "Infant FollowUp: Medication"
