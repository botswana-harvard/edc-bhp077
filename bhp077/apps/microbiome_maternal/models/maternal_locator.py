from django.db import models

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.locator.models import BaseLocator
from edc_base.encrypted_fields import EncryptedCharField
from edc_base.model.fields import OtherCharField
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators import CellNumber, TelephoneNumber
from edc_constants.choices import YES_NO

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

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    def get_visit(self):
        return self.maternal_visit

    def get_subject_identifier(self):
        return self.maternal_visit.appointment.registered_subject.subject_identifier

    def __unicode__(self):
        return unicode(self.maternal_visit)

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Locator'
        verbose_name_plural = 'Maternal Locator'
