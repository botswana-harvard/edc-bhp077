from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc_base.model.fields.custom_fields import OtherCharField
from edc_constants.choices import YES_NO, SEVERITY_LEVEL
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future

from bhp077.apps.microbiome_list.models import AutopsyInfoSource
from bhp077.apps.microbiome.choices import AUTOPSY_SIGNS

from .infant_scheduled_visit_model import InfantScheduledVisitModel

from edc_base.model.models.base_uuid_model import BaseUuidModel


class InfantVerbalAutopsy(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's Verbal Autopsy. """

    report_datetime = models.DateTimeField(
        verbose_name="Today's date",
        null=True,
        blank=False,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ]
    )

    source = models.ManyToManyField(
        AutopsyInfoSource,
        verbose_name='Source of verbal autopsy',
        max_length=50)

    first_sign = models.TextField(
        verbose_name=("Starting with the last illness preceding (participant\'s) death,"
                      " describe the first noticeable sign or symptom of illness, continuing"
                      " until the time of death."),
        max_length=1000)

    prop_cause = models.TextField(
        verbose_name="What do you think probably caused (participant\'s) death?",
        max_length=1000,
        help_text="Note: Please avoid HIV as cause of death")

    sign_symptoms = models.CharField(
        verbose_name=("During the last illness preceding death, did  the participant"
                      " experience ANY of the following signs or symptoms:"),
        max_length=3,
        choices=YES_NO)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.registered_subject.subject_identifier

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.registered_subject.relative_identifier

    def get_registration_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = "microbiome_infant"


class InfantVerbalAutopsyItems(BaseUuidModel):

    verbal_autopsy = models.ForeignKey(InfantVerbalAutopsy)

    sign_symptom = models.CharField(
        max_length=70,
        choices=AUTOPSY_SIGNS,
        verbose_name="Sign or Symptom",
        blank=True,
        null=True,
    )
    onset_date = models.DateField(
        verbose_name="Date of Onset",
        blank=True,
        null=True,
    )
    duration = OtherCharField(
        max_length=25,
        verbose_name="Duration (days/hours)",
        blank=True,
        null=True,
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_LEVEL,
        verbose_name="Severity",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    history = AuditTrail()

    def get_report_datetime(self):
        return self.verbal_autopsy.report_datetime

    def get_consenting_subject_identifier(self):
        """Returns mother's identifier."""
        return self.verbal_autopsy.get_consenting_subject_identifier()

    def get_visit(self):
        return self.verbal_autopsy.infant_visit

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Verbal Autopsy:Item"
