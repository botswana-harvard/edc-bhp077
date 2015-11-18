from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.entry.models import Entry
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO
from edc_constants.constants import YES

from .infant_scheduled_visit_model import InfantScheduledVisitModel
from .infant_birth import InfantBirth


class InfantBirthData(InfantScheduledVisitModel):

    infant_birth = models.OneToOneField(InfantBirth)

    infant_birth_weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="What was the infant's birth weight? ",
        help_text="Measured in Kilograms (kg)")
    infant_length = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        verbose_name="What was the infant's length at birth? ",
        help_text="Measured in centimeters, (cm)")
    head_circumference = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        verbose_name="What was the head circumference in centimeters? ",
        help_text="Measured in centimeters, (cm)")
    apgar_score = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was Apgar Score performed? ",
        help_text="If 'No' go to question 10. Otherwise continue")
    apgar_score_min_1 = models.IntegerField(
        max_length=2,
        verbose_name="At 1 minute: ",
        help_text="-1 if unknown",
        blank=True,
        null=True,
        validators=[MaxValueValidator(10),
                    MinValueValidator(-1)])
    apgar_score_min_5 = models.IntegerField(
        max_length=2,
        verbose_name="At 5 minutes: ",
        help_text="-1 if unknown",
        blank=True,
        null=True,
        validators=[MaxValueValidator(10),
                    MinValueValidator(-1)])
    apgar_score_min_10 = models.IntegerField(
        max_length=2,
        verbose_name="At 10 minutes: ",
        help_text="-1 if unknown",
        blank=True,
        null=True,
        validators=[MaxValueValidator(10),
                    MinValueValidator(-1)])
    congenital_anomalities = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Were any congenital anomalies identified? ",
        help_text="If 'Yes' please complete the Congenital Anomalies Form",)
    other_birth_info = models.TextField(
        max_length=250,
        verbose_name="Other birth information ",
        blank=True,
        null=True)

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.infant_birth)

    def change_meta_status_if_there_are_anomalies_identified(self):
        if self.congenital_anomalities == YES:
            entry = Entry.objects.get(model_name='infantcongenitalanomalies',
                                      visit_definition_id=self.appointment.visit_definition_id)
            scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                appointment=self.appointment,
                entry=entry,
                registered_subject=self.registered_subject)
            if not scheduled_meta_data:
                scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                    appointment=self.appointment,
                    entry=entry,
                    registered_subject=self.registered_subject)
            else:
                scheduled_meta_data = scheduled_meta_data[0]
            scheduled_meta_data.entry_status = 'NEW'
            scheduled_meta_data.save()
            return scheduled_meta_data

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_infantbirthdata_change', args=(self.id,))

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Birth Record: Data"
        verbose_name_plural = "Infant Birth Records: Data"
