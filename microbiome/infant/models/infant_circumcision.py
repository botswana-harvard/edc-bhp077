from django.db import models

from edc_base.model.models import BaseUuidModel
from ..choices import CIRCUMCISION


class InfantCircumcision(BaseUuidModel):

    circumcised = models.CharField(
        max_length=15,
        verbose_name="In performing your physical exam, you determined this male infant to be:",
        choices=CIRCUMCISION,
        help_text="",
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = "Infant Male Circumcision"
