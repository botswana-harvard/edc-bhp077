from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps
try:
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

from edc_base.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc_registration.models import RegisteredSubject

from ..models import SubjectConsent, MaternalEligibilityPre
from ..choices import (BIRTH_TYPE, VAGINAL, NOT_ENROLLED, HIV_INFECTED_COHOT, HIV_UNIFECTED_COHOT, POS, NEG,
                       PENDING_INFANT_RESULT, YES_NO, CHECKLIST_DISEASES, HIVRESULT_CHOICE, HAART_DURING_PREG,
                       YES, PENDING_BIRTH, NOT_APPLICABLE)


class MaternalEligibilityPost (BaseUuidModel):
    """A model completed to evaluate post consent Eligibility. This could be the 1st step of eligibility.
    The last step  will be InfantEligibility fro HIV infected mothers."""

    registered_subject = models.OneToOneField(
        RegisteredSubject,
        null=True,
        blank=True,
        help_text=''
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Date and time of assessing eligibility'
    )

    # TODO: turn this field in to a ManyToMany.
    disease = models.CharField(
        verbose_name="Do you currently have any of the following diseases?",
        max_length=15,
        help_text="If participant has any of the diseases, then not eligible.",
        choices=CHECKLIST_DISEASES
    )

    currently_pregnant = models.CharField(
        verbose_name="Is the participant currently pregnant?",
        max_length=4,
        choices=YES_NO,
        help_text='If yes, then they are provisionally enrolled pending birth.'
    )

#     pregnancy_weeks = models.IntegerField(
#         verbose_name='If pregnant, how many weeks in to the pregnancy?',
#         null=True,
#         blank=True,
#         help_text='Must be at least 36 weeks pregnant.'
#     )

    weeks_of_gestation = models.IntegerField(
        verbose_name="If delivered, how many weeks of gestation was the pregnancy?",
        null=True,
        blank=True,
        help_text="If gestation was 36 weeks or less (baby born pre-term), then not eligible.",
    )

    days_post_natal = models.IntegerField(
        verbose_name="If delivered, how many days postnatal? ",
        null=True,
        blank=True,
        help_text="if >3 days, ineligible",
    )

    type_of_birth = models.CharField(
        verbose_name="If delivered, how was the infant(s) delivered? ",
        null=True,
        blank=True,
        max_length=10,
        choices=BIRTH_TYPE,
        help_text="If cesarean section, then not eligible."
    )

    live_infants = models.IntegerField(
        verbose_name="If delivered, how many live infants did the mother deliver?",
        null=True,
        blank=True,
        help_text="If zero live then not eligible.",
    )

    verbal_hiv_status = models.CharField(
        verbose_name="What is your current HIV status?",
        max_length=30,
        choices=HIVRESULT_CHOICE,
        help_text=''
    )

    evidence_pos_hiv_status = models.CharField(
        verbose_name="(Interviewer) If HIV+, have you seen evidence of the HIV result?",
        max_length=4,
        choices=YES_NO,
        help_text='Evidence of HIV positive status either by showing a positive testing result or '
                  'showing IDCC records that demonstrate that she is taking ARVs.'
    )

    rapid_test_result = models.CharField(
        verbose_name="(Interviewer: Only for those without HIV+ documentation.) What is the rapid test result?",
        max_length=30,
        null=True,
        blank=True,
        choices=HIVRESULT_CHOICE,
        help_text='If mother has no evidence of HIV status or has not tested on or after 32 weeks gestational age, '
                  'she must undergo  rapid testing. If positive, will not have been on treatment sufficiently long '
                  'enough and is not eligible.  If negative, eligible to join the study.'
    )

    rapid_test_result_datetime = models.DateTimeField(
        verbose_name="Rapid test result date and time",
        null=True,
        blank=True,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Leave blank for an HIV +ve mother with evidence of status'
    )

    haart_during_preg = models.CharField(
        verbose_name="Was the mother on HAART during pregnancy",
        max_length=4,
        null=True,
        blank=True,
        choices=YES_NO,
        help_text='For HIV +ve mothers only. Leave blanck for those HIV -ve.'
    )

    haart_start_date = models.DateField(
        verbose_name="Date of HAART first started",
        null=True,
        blank=True,
        help_text="For HIV +ve mothers only. Leave blanck for those HIV -ve.",
    )

    # TODO: change this in to a ManyToMany
    drug_during_preg = models.CharField(
        max_length=50,
        verbose_name="Which drug was the mother taking during pregnancy?",
        choices=HAART_DURING_PREG,
        help_text="choose Not Applicable if its none of the above.",
    )

    enrollment_status = models.CharField(
        verbose_name="Study arm that mother and child(ren) are enrolled in.",
        max_length=10,
        default=NOT_ENROLLED,
        help_text="Automatically calculated by the system"
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.enrollment_status = self.evaluate_enrollment_status
        super(MaternalEligibilityPost, self).save(*args, **kwargs)

    @property
    def evaluate_enrollment_status(self):
        """Evaluates the post enrollment status"""
        if self.disease.lower() != NOT_APPLICABLE.lower():
            return NOT_ENROLLED
        if self.currently_pregnant == YES:
            return PENDING_BIRTH
        else:
            if self.verbal_hiv_status.lower() == 'neg' and self.rapid_test_result.lower() == 'pos':
                return NOT_ENROLLED
            if self.days_post_natal and self.days_post_natal > 3:
                return NOT_ENROLLED
            elif self.weeks_of_gestation and self.weeks_of_gestation <= 36:
                return NOT_ENROLLED
            elif self.type_of_birth and self.type_of_birth != VAGINAL:
                return NOT_ENROLLED
            elif self.live_infants and self.live_infants == 0:
                return NOT_ENROLLED
            elif self.mother_hiv_result == POS:
                # This is an HIV infected mother, need to check Infant eligibility to make sure atleast one
                # infant is HIV -ve.
                if not self.atleast_one_infant_eligible:
                    # This means all infants are HIV infected from test results.
                    return NOT_ENROLLED
            elif self.mother_hiv_result == POS and not self.atleast_one_infant_resulted:
                # None of the infants for an HIV +ve mother have an HIV result available,
                # so we wait for the first result before allocating mother to study arm.
                self.enrollment_status = PENDING_INFANT_RESULT
            # elif self.is_eligible:
                # Mother is HIV -ve or Mother is HIV +ve and one of the infants have a result,
                # so we go ahead allocate to study arm.
            #    self.enrollment_status = self.evaluate_study_arm()
            else:
                return HIV_INFECTED_COHOT

#     @property
#     def evaluate_study_arm(self):
#         if self.mother_hiv_result == POS:
#             return HIV_INFECTED_COHOT
#         elif self.mother_hiv_result == NEG:
#             return HIV_UNIFECTED_COHOT
#         else:
#             raise ValidationError('Unable to determine enrollment cohot for the mother based on maternal screening.')

    @property
    def maternal_screening(self):
        sc = SubjectConsent.objects.get(registered_subject=self.registered_subject)
        screen_identifier = sc.screening_identifier
        return MaternalEligibilityPre.objects.get(screening_identifier=screen_identifier)

    @property
    def mother_hiv_result(self):
        if (self.verbal_hiv_status == POS and (self.evidence_pos_hiv_status or self.rapid_test_result == POS)):
            return POS
        return NEG

    @property
    def atleast_one_infant_eligible(self):
        InfantEligibility = get_model('microbiome', 'InfantEligibility')
        infant_eligibilities = InfantEligibility.objects.filter(maternal_enrollment_post=self)
        for infant in infant_eligibilities:
            if infant.is_eligible:
                # break out returning True for the 1st eligible infant you encounter.
                return True
        # Return false if no eligible infant could be found for this mother
        return False

    @property
    def atleast_one_infant_resulted(self):
        InfantEligibility = get_model('microbiome', 'InfantEligibility')
        infant_eligibilities = InfantEligibility.objects.filter(maternal_enrollment_post=self)
        for infant in infant_eligibilities:
            if infant.is_resulted:
                # break out returning True for the 1st resulted infant you encounter.
                return True
        # Return false if no resulted infant could be found for this mother
        return False

#     def __str__(self):
#         return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Eligibility Post"
        verbose_name_plural = "Maternal Eligibility Post"
