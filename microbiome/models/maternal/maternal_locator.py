from django.db import models

from django_crypto_fields import EncryptedCharField
from edc_constants import YES_NO
from edc_base import OtherCharField, BWCellNumber, BWTelephoneNumber
from edc_locator.models import BaseLocator

from .maternal_visit import MaternalVisit


class MaternalLocator(BaseLocator):

    maternal_visit = models.OneToOneField(MaternalVisit)

    care_clinic = OtherCharField(
        max_length=35,
        verbose_name="Health clinic where your infant will receive their routine care ",
        help_text="",
    )

    has_caretaker_alt = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Has the participant identified someone who will be responsible for the care of the baby in case of her death, to whom the study team could share information about her baby's health?",
        help_text="",
    )

    caretaker_name = EncryptedCharField(
        max_length=35,
        verbose_name="Full Name of the responsible person",
        help_text="include firstname and surname",
        blank=True,
        null=True,
    )

    caretaker_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    caretaker_tel = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone number",
        validators=[BWTelephoneNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Maternal Locator'
        app_label = 'microbiome'
