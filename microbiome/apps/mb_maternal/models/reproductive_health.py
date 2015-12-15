from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO_DWTA

from ..maternal_choices import YES_NO_DNT_DWTA, NEXT_CHILD_PLAN
from .maternal_consent import MaternalConsent
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from bhp077.apps.microbiome_list.models import Contraceptives


class ReproductiveHealth(MaternalScheduledVisitModel):

    """ A model completed by the user on the mother's sexual reproductive health. """

    CONSENT_MODEL = MaternalConsent

    more_children = models.CharField(
        verbose_name='Do you desire more children?',
        max_length=25,
        choices=YES_NO_DNT_DWTA,
        help_text='')

    next_child = models.CharField(
        verbose_name='When would you like to have your next child?',
        max_length=35,
        choices=NEXT_CHILD_PLAN,
        blank=True,
        null=True,
        help_text='')

    contraceptive_measure = models.CharField(
        verbose_name='Have you discussed a contraceptive measure with a health care provider?',
        max_length=35,
        choices=YES_NO_DWTA,
        help_text='')

    uses_contraceptive = models.CharField(
        verbose_name='Are you currently using a contraceptive method?',
        max_length=35,
        choices=YES_NO_DWTA,
        help_text='')

    contraceptives = models.ManyToManyField(
        Contraceptives,
        verbose_name='Please share with us your current contraceptive methods',
        help_text='')

    contraceptives_other = OtherCharField(
        max_length=35,
        verbose_name="If Other enter text description of other contraceptive method being used",
        blank=True,
        null=True)

    srh_referral = models.CharField(
        verbose_name='Would you like to be referred to the Sexual Reproductive Health Clinic?',
        max_length=25,
        choices=YES_NO_DWTA,
        help_text='')

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Reproductive Health'
        verbose_name_plural = 'Reproductive Health'
