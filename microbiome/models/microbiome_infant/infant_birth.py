from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators.date import date_not_future
from edc_constants.choices import GENDER_UNDETERMINED

from microbiome.models.microbiome_maternal import MaternalLabourDel


class InfantBirth(BaseUuidModel):

    maternal_lab_del = models.ForeignKey(
        MaternalLabourDel,
        verbose_name="Mother's delivery record"
    )

    first_name = models.CharField(
        max_length=25,
        verbose_name="Infant's first name",
        help_text="If infant name is unknown or not yet determined, "
                  "use Baby + birth order + mother's last name, e.g. 'Baby1Malane'"
    )

    initials = models.CharField(
        max_length=2,
    )

    birth_order = models.IntegerField(
        verbose_name='Birth Order',
        help_text="For example, 1, 2, 3, .... Is also implied by infant identifier suffix.",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(4), ],
    )

    dob = models.DateField(
        verbose_name='Date of Birth',
        help_text="Must match labour and delivery report.",
        validators=[date_not_future, ],
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_UNDETERMINED,
    )

    class Meta:
        app_label = "microbiome"
        table_name = "micro_infantbirth"
        verbose_name = "Infant Birth Record"
