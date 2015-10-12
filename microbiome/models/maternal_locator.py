from django.db import models

from edc_base.encrypted_fields import EncryptedCharField
from edc_constants.choices import YES_NO
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators import CellNumber, TelephoneNumber
from edc_base.model.fields import OtherCharField
from edc.subject.locator.models import BaseLocator

from .maternal_visit import MaternalVisit


class MaternalLocator(BaseLocator, BaseUuidModel):

    maternal_visit = models.ForeignKey(MaternalVisit)

    care_clinic = OtherCharField(
        max_length=35,
        verbose_name="Health clinic where your infant will receive their routine care ",
        help_text="", )

    has_caretaker_alt = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Has the participant identified someone who will be "
        "responsible for the care of the baby in case of her death, to whom the "
        "study team could share information about her baby's health?",
        help_text="", )

    caretaker_name = EncryptedCharField(
        max_length=35,
        verbose_name="Full Name of the responsible person",
        help_text="include firstname and surname",
        blank=True,
        null=True, )

    caretaker_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[CellNumber, ],
        help_text="",
        blank=True,
        null=True, )

    caretaker_tel = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone number",
        validators=[TelephoneNumber, ],
        help_text="",
        blank=True,
        null=True, )

    class Meta:
        app_label = 'microbiome'
        verbose_name = 'Maternal Locator'
        verbose_name_plural = 'Maternal Locator'
