from django.db import models


class MaternalPostMedItemsManager(models.Manager):

    def get_by_natural_key(self, medication, date_first_medication,
                           date_stoped, report_datetime, visit_instance,
                           code, subject_identifier_as_pk):
        MaternalPostFuMed = models.get_model('mb_maternal', 'MaternalPostFuMed')
        maternal_post_fu_med = MaternalPostFuMed.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(medication=medication,
                        date_first_medication=date_first_medication,
                        date_stoped=date_stoped,
                        maternal_post_fu_med=maternal_post_fu_med)
