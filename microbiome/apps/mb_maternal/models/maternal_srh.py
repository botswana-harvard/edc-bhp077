from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO_DWTA

from ..maternal_choices import REASON_UNSEEN_AT_CLINIC, REASON_CONTRACEPTIVE_NOT_INITIATED
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from bhp077.apps.microbiome_list.models import Contraceptives
from .maternal_consent import MaternalConsent


class MaternalSrh(MaternalScheduledVisitModel):

    """ A model completed by the user on the mother's use of sexual reproductive health services. """

    CONSENT_MODEL = MaternalConsent

    seen_at_clinic = models.CharField(
        verbose_name=('At the last visit, you had asked to be referred to the Sexual'
                      ' Reproductive Health Clinic.  Have you been seen in that clinic'
                      ' since your last visit with us?'),
        max_length=15,
        choices=YES_NO_DWTA)

    reason_unseen_clinic = models.CharField(
        verbose_name='If no, why not?',
        max_length=45,
        null=True,
        blank=True,
        choices=REASON_UNSEEN_AT_CLINIC)

    reason_unseen_clinic_other = OtherCharField(
        verbose_name='If Other, describe')

    is_contraceptive_initiated = models.CharField(
        verbose_name='If you did attend, did you initiate a contraceptive method?',
        max_length=15,
        choices=YES_NO_DWTA)

    contraceptives = models.ManyToManyField(
        Contraceptives,
        verbose_name='If yes, which method did you select? ',
        help_text='Tell us all that apply')

    reason_not_initiated = models.CharField(
        verbose_name=('If you have not initiated a contraceptive method after attending'
                      ' a SRH clinic, please share with use the reason why you have not'
                      ' initiated a method'),
        max_length=45,
        choices=REASON_CONTRACEPTIVE_NOT_INITIATED,
        blank=True,
        null=True,
        help_text='')

    srh_referral = models.CharField(
        verbose_name='Would you like to be referred to the Sexual Reproductive Health Clinic?',
        max_length=25,
        choices=YES_NO_DWTA,
        help_text='')

    srh_referral_other = OtherCharField(
        verbose_name='If other is selected enter text',
        blank=True,
        null=True,
        help_text='')

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal SRH Services'
        verbose_name_plural = 'Maternal SRH Services'
