from django.db import models
from edc_base.model.models import BaseUuidModel
from ..maternal_choices import ARV_DRUG_LIST, ARV_MODIFICATION_REASON, DOSE_STATUS


class BaseHaartModification(BaseUuidModel):
    """
    Base Class for recording HAART medications
    """
    arv_code = models.CharField(
        verbose_name="ARV Code",
        max_length=25,
        choices=ARV_DRUG_LIST)
    dose_status = models.CharField(
        max_length=25,
        choices=DOSE_STATUS,
        verbose_name="Dose Status")
    modification_date = models.DateField(
        verbose_name="Date ARV Modified")
    modification_code = models.CharField(
        max_length=50,
        choices=ARV_MODIFICATION_REASON,
        verbose_name="Reason for Modification")

    def natural_key(self):
        return (self.arv_code, self.modification_date, )

    class Meta:
        abstract = True
