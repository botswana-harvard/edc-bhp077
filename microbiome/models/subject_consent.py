from django.db import models
from django.core.exceptions import ValidationError

from edc_consent.models import BaseConsent

from ..models import MaternalEligibilityPre
from ..choices import YES_NO_UNKNOWN


class SubjectConsent(BaseConsent):

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="")

    maternal_eligibility_pre = models.OneToOneField(
        MaternalEligibilityPre,
    )

    def save(self, *args, **kwargs):
        # TODO: Update registered values that might have changed in consent HERE the save registered_subject.
        if not self.registered_subject:
            self.registered_subject = self.maternal_eligibility_pre.registered_subject
        self.matches_maternal_eligibility_pre(self, self.maternal_eligibility_pre)
        super(SubjectConsent, self).save(*args, **kwargs)

    def matches_maternal_eligibility_pre(self, subject_consent, maternal_eligibility_pre, exception_cls=None):
        """Matches values in this consent against the pre maternal eligibility."""
        registered_subject = subject_consent.registered_subject
        exception_cls = exception_cls or ValidationError
        if False:
            raise exception_cls('Subject consent does not match Maternal Pre Elgibility')
        return True

    class Meta:
        app_label = 'microbiome'
