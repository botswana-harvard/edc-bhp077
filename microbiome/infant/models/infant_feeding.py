from django.db import models
from django.core.urlresolvers import reverse

from edc_base.model.fields.custom_fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNSURE_NA

from ..choices import COWS_MILK, REASON_RCV_FORMULA, TIMES_BREASTFED, WATER_USED


class InfantFeeding(models.Model):

    """Infant Feeding """

    last_att_sche_visit = models.DateField(
        verbose_name="When was the last attended scheduled visit where an infant feeding form was completed? ",
        help_text="",
        blank=True,
        null=True,
    )

    other_feeding = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed, "
                     "has the participant received any formula milk or other foods or liquids other than breastmilk? ",
        help_text=("If Formula Feeding or received any other foods or liquids answer YES. "
                     "If Breast Feeding answer is NO, then go to Q22"),
    )

    formula_intro_occur = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name="Did the introduction of formula or other foods or liquids to the participant occur before the "
                     "last attended scheduled visit where an infant feeding form was completed?",
        help_text="If this is the randomization visit you must enter NO, because no infant could take any formula ,"
                  "foods or liquids before birth",
        default='N/A',
    )

    formula_date = models.DateField(
        verbose_name="Date participant first received formula milk (or other foods or liquids)since last attended "
                     "scheduled visit where an infant feeding form was completed",
        help_text="Only put a date here if this is the first time you are reporting introduction of formula,food or "
                  "other liquids, if you are not certain if a date has been previously reported come out of this form "
                  "and press the audit trail at the end of the feeding form and then press search next to the subject "
                  "identifier.For all visits after september 06 2011 infant feeding form data will be displayed.",
        blank=True,
        null=True,
    )

    reason_rcv_formula = models.CharField(
        verbose_name="Which of the following is the most significant reason why the participant received formula milk "
                     "(if the baby had breastfed) or other foods or liquids (if the baby has been breastfed or formula"
                     " fed) since the last attended scheduled visit where an infant feeding form was completed? ",
        max_length=25,
        help_text="If baby breastfed give reason why they received formula or other food/liquids, if the baby was "
                  "formula feeding give reason for receiving other foods/liquids",
        choices=REASON_RCV_FORMULA,
        default='N/A',
    )

    reason_rcv_fm_other = models.TextField(
        max_length=250,
        verbose_name="If 'other' specify",
        blank=True,
        null=True,
    )

    water_used = models.CharField(
        max_length=50,
        verbose_name="What water do you usually use to prepare the participant's milk?",
        choices=WATER_USED,
        help_text="",
        default='N/A',
    )

    water_used_other = OtherCharField(
        max_length=35,
        verbose_name="If 'other', specify",
        blank=True,
        null=True,
    )

    formula = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Formula?",
        help_text="If formula feeding since last visit answer YES",
        default='N/A',
    )

    water = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed did "
                     "the participant take Water?",
        help_text="Not as part of formula milk",
        default='N/A',
    )

    juice = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Juice?",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer N/A ",
        default='N/A',
    )

    cow_milk = models.CharField(
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Cow's milk?",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer N/A ",
        default='N/A',
    )

    cow_milk_yes = models.CharField(
        verbose_name="If 'Yes', was cow's milk...",
        max_length=25,
        choices=COWS_MILK,
        help_text="",
        default='N/A',
    )

    other_milk = models.CharField(
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was "
                     "completed did the participant take Other animal milk?",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer N/A ",
        default='N/A',
    )

    other_milk_animal = OtherCharField(
        max_length=35,
        verbose_name="If 'Yes' specify which animal:",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer N/A ",
        blank=True,
        null=True,
    )

    milk_boiled = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Was milk boiled?",
        help_text="",
        default='N/A',
    )

    fruits_veg = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Fruits/vegetables",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this "
                  "question, you may not answer N/A ",
        default='N/A',
    )

    cereal_porridge = models.CharField(
        max_length=12,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Cereal/porridge?",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer N/A ",
        default='N/A',
    )

    solid_liquid = models.CharField(
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was "
                     "completed did the participant take Other solids and liquids",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer N/A ",
        default='N/A',
    )

    rehydration_salts = models.CharField(
        max_length=3,
        choices=YES_NO_UNSURE_NA,
        verbose_name="Since the last attended scheduled visit where an infant feeding form was completed "
                     "did the participant take Oral rehydaration salts",
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT SURE to this question, "
                  "you may not answer N/A ",
        default='N/A',
    )

    ever_breastfeed = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Since the last attended scheduled visit,did the infant ever breastfeed",
        help_text="",
    )

    complete_weaning = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name="If 'NO', did complete weaning from breast milk take place before the last "
                     "attended scheduled visit?",
        help_text="If formula fed from birth,answer as N/A. If YES, go to question 26. Otherwise continue.",
        default='N/A',
    )

    weaned_completely = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name="Is the participant currently completely weaned from breast milk (at least 72 hours "
                     "without breastfeeding,no intention to re-start)?",
        help_text="If formula fed from birth ,answer as N/A and go to question 26, otherwise continue",
        default='N/A',
    )

    most_recent_bm = models.DateField(
        verbose_name="Date of most recent breastfeeding ",
        help_text="",
        blank=True,
        null=True,
    )

    times_breastfed = models.CharField(
        max_length=50,
        verbose_name="Between the last attended scheduled visit where an infant feeding form was completed and date "
                     "of most recent breastfeeding,how often did the participant receive breast milk for feeding?",
        choices=TIMES_BREASTFED,
        help_text="",
        default='N/A',
    )

    comments = models.TextField(
        max_length=200,
        verbose_name="List any comments about participant's feeding that are not answered above",
        blank=True,
        null=True,
    )

    def __st__(self):
        return "%s" % (self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantfeeding_change', args=(self.id,))

    class Meta:
        app_label = "microbiome"
        verbose_name = "Infant Feeding"
