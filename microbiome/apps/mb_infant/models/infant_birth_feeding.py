from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_visit_tracking.models import CrfInlineModelMixin

from microbiome.apps.mb.choices import FEEDING_CHOICES

from ..choices import INFANT_VACCINATIONS
from ..managers import InfantInlineModelManager

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantBirthFeedVaccine(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's feeding & vaccination/ immunization. """

    feeding_after_delivery = models.CharField(
        max_length=50,
        choices=FEEDING_CHOICES,
        verbose_name="How was the infant being fed immediately after delivery? ",
        help_text=" ...before discharge from maternity")

    comments = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information: ",
        blank=True,
        null=True)

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Birth Feeding & Vaccination"


class InfantVaccines(CrfInlineModelMixin, BaseUuidModel):

    fk_model_attr = 'infant_birth_feed_vaccine'

    infant_birth_feed_vaccine = models.ForeignKey(InfantBirthFeedVaccine)

    vaccination = models.CharField(
        choices=INFANT_VACCINATIONS,
        verbose_name="Since delivery, did the child receive any of the following vaccinations",
        max_length=100,
        null=True,
        blank=True)

    vaccine_date = models.DateField(
        verbose_name='Date Vaccine was given',
        null=True,
        blank=True)

    objects = InfantInlineModelManager()

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant Vaccines"
        verbose_name_plural = "Infant Vaccines"
