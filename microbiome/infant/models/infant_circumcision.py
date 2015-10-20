from django.db import models

from microbiome.choices import CIRCUMCISION

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantCircumcision(InfantScheduledVisitModel):

    circumcised = models.CharField(
        max_length=15,
        verbose_name="In performing your physical exam, you determined this male infant to be:",
        choices=CIRCUMCISION,
        help_text="",
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Male Circumcision"
