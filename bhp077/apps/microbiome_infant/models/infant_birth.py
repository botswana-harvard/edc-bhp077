from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.registration.models import RegisteredSubject
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_base.model.validators.date import date_not_future
from edc_consent.models import RequiresConsentMixin
from edc_constants.choices import GENDER_UNDETERMINED

from bhp077.apps.microbiome_maternal.models import MaternalLabourDel
from bhp077.apps.microbiome_infant.models.infant_off_study_mixin import InfantOffStudyMixin


class InfantBirth(InfantOffStudyMixin, BaseUuidModel, BaseAppointmentMixin):

    registered_subject = models.OneToOneField(RegisteredSubject, editable=False, null=True)

    maternal_labour_del = models.ForeignKey(
        MaternalLabourDel,
        verbose_name="Mother's delivery record")

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time infant enrolled",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    first_name = models.CharField(
        max_length=25,
        verbose_name="Infant's first name",
        help_text="If infant name is unknown or not yet determined, "
                  "use Baby + birth order + mother's last name, e.g. 'Baby1Malane'")
    initials = models.CharField(
        max_length=2)

    birth_order = models.IntegerField(
        verbose_name='Birth Order',
        help_text="",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(4), ])

    dob = models.DateField(
        verbose_name='Date of Birth',
        help_text="Must match labour and delivery report.",
        validators=[date_not_future, ])

    gender = models.CharField(
        max_length=10,
        choices=GENDER_UNDETERMINED)

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Birth Record"
        verbose_name_plural = "Infant Birth Record"
