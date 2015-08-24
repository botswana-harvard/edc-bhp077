from django.db.models.signals import post_save
from django.db import transaction

from django.dispatch import receiver
from ..exceptions import CreateInfantEligibilityError

from ..models import MaternalEligibilityPost, MaternalEligibilityPre, InfantEligibility


@receiver(post_save, weak=False, dispatch_uid='maternal_eligibility_post_save')
def maternal_eligibility_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    """Creates the Infant Eligibility recored to match the number in MaternalEligibilityPost.live_infants.
    Only the foreign key to MaternalEligibilityPost. The user will need to open the form and populate all
    other fields accordingly, before proceeding."""
    if not raw:
        if isinstance(instance, MaternalEligibilityPost):
            num_live_infants = instance.live_infants
            try:
                with transaction.atomic():
                    for index in range(1, num_live_infants):
                        InfantEligibility.objects.create(maternal_enrollment_post=instance)
            except:
                raise CreateInfantEligibilityError(
                    'An ERROR occurred while attempting to create infant eligibility for {}'.format(instance)
                )

@receiver(post_save, weak=False, dispatch_uid='get_create_registered_subject_post_save')
def get_create_registered_subject_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, MaternalEligibilityPre):
            instance.get_create_registered_subject_post_save()
