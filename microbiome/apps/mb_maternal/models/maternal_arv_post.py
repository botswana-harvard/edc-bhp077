from django.db import models

from edc.subject.haart.choices import ARV_STATUS_WITH_NEVER
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO

from ..managers import MaternalArvPostModManager
from ..maternal_choices import REASON_FOR_HAART

from .base_haart_modification import BaseHaartModification
from .maternal_consent import MaternalConsent
from .maternal_off_study_mixin import MaternalOffStudyMixin
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from edc_constants.constants import NOT_APPLICABLE


class MaternalArvPost (MaternalScheduledVisitModel):

    """ A model completed by the user on the mother's ARVs administered post-partum. """

    CONSENT_MODEL = MaternalConsent

    on_arv_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=("Was the mother supposed to be on triple ARVs any time since the last"
                      " attended scheduled visit?"),
        help_text="If 'NO' End. Otherwise continue go to section one",)

    on_arv_reason = models.CharField(
        verbose_name="Reason for triple ARVs ",
        max_length=25,
        choices=REASON_FOR_HAART,
        default=NOT_APPLICABLE,
        help_text="",)

    on_arv_reason_other = models.TextField(
        max_length=35,
        verbose_name="if other, specify",
        blank=True,
        null=True,)

    arv_status = models.CharField(
        verbose_name=("What is the status of the participant's antiretroviral"
                      " treatment / prophylaxis at this visit or since the last visit? "),
        max_length=25,
        choices=ARV_STATUS_WITH_NEVER,
        default=NOT_APPLICABLE,)

    history = AuditTrail()

    def visit(self):
        return self.maternal_visit

    def __unicode__(self):
        return unicode(self.maternal_visit)

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal ARV Post"
        verbose_name_plural = "Maternal ARV Post"


class MaternalArvPostMod(MaternalOffStudyMixin, BaseHaartModification):

    """ Maternal ARV modifications post-partum.

    if art_status never, no_mod or N/A then this is not required"""
    CONSENT_MODEL = MaternalConsent

    maternal_arv_post = models.ForeignKey(MaternalArvPost)

    objects = MaternalArvPostModManager()

    history = AuditTrail()

    def get_visit(self):
        return self.maternal_arv_post.maternal_visit

    def __unicode__(self):
        return unicode(self.maternal_arv_post)

    def get_report_datetime(self):
        return self.get_visit().get_report_datetime()

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def natural_key(self):
        return super(MaternalArvPostMod, self).natural_key() + self.maternal_arv_post.natural_key()

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = 'Maternal ARVs Post: Mods'
        verbose_name_plural = 'Maternal ARVs Post: Mods'
        unique_together = ('maternal_arv_post', 'arv_code', 'modification_date')


class MaternalArvPostAdh(MaternalScheduledVisitModel):

    """Maternal ARV adherence post-partum"""
    CONSENT_MODEL = MaternalConsent

    maternal_arv_post = models.OneToOneField(MaternalArvPost)

    missed_doses = models.IntegerField(
        verbose_name=("Since the last attended last scheduled visit, how many doses of"
                      " triple ARVs were missed? "))

    missed_days = models.IntegerField(
        verbose_name=("Since the last attended scheduled visit, how many entire days"
                      " were triple ARVS not taken?"),
        default=0)

    missed_days_discnt = models.IntegerField(
        verbose_name=("If triple ARVs discontinued by health provider, how many days were triple ARVs missed"
                      " prior to discontinuation?"),
        default=0)

    comment = models.TextField(
        max_length=250,
        verbose_name="Comment",
        blank=True,
        null=True)

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.maternal_arv_post)

    def get_report_datetime(self):
        return self.maternal_arv_post.get_report_datetime()

    def get_subject_identifier(self):
        return self.maternal_arv_post.get_subject_identifier()

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal ARVs Post: Adherence"
        verbose_name_plural = "Maternal ARVs Post: Adherence"
