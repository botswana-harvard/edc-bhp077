from django.db import models

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_base.encrypted_fields import EncryptedCharField
from edc_base.model.fields import OtherCharField
from edc.device.sync.models import BaseSyncUuidModel
from edc_base.model.validators import CellNumber, TelephoneNumber
from edc_constants.choices import YES_NO
from edc_locator.models import LocatorMixin

from .maternal_visit import MaternalVisit
from ..managers import ScheduledModelManager


class MaternalLocator(LocatorMixin, BaseSyncUuidModel):

    """ A model completed by the user to capture locator information and
    the details of the infant caretaker. """

    maternal_visit = models.ForeignKey(MaternalVisit)

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    care_clinic = OtherCharField(
        verbose_name="Health clinic where your infant will receive their routine care ",
        max_length=35,
    )

    has_caretaker = models.CharField(
        verbose_name=(
            "Has the participant identified someone who will be "
            "responsible for the care of the baby in case of her death, to whom the "
            "study team could share information about her baby's health?"),
        max_length=25,
        choices=YES_NO,
        help_text="")

    caretaker_name = EncryptedCharField(
        verbose_name="Full Name of the responsible person",
        max_length=35,
        help_text="include firstname and surname",
        blank=True,
        null=True)

    caretaker_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[CellNumber, ],
        help_text="",
        blank=True,
        null=True)

    caretaker_tel = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone number",
        validators=[TelephoneNumber, ],
        help_text="",
        blank=True,
        null=True)

    objects = ScheduledModelManager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.maternal_visit)

    def natural_key(self):
        return self.maternal_visit.natural_key()

    def get_visit(self):
        return self.maternal_visit

    def get_subject_identifier(self):
        return self.maternal_visit.appointment.registered_subject.subject_identifier

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'Maternal Locator'
        verbose_name_plural = 'Maternal Locator'
