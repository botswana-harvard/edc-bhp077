from django.db import models


class MaternalPostFuDxTManager(models.Manager):

    def get_by_natural_key(self, post_fu_dx, report_datetime, visit_instance, code, subject_identifier_as_pk):
        MaternalPostFuDx = models.get_model('mb_maternal', 'MaternalPostFuDx')
        maternal_post_fu_dx = MaternalPostFuDx.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(post_fu_dx=post_fu_dx, maternal_post_fu_dx=maternal_post_fu_dx)
