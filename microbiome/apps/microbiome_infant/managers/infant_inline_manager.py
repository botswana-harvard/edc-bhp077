from django.db import models


class InfantInlineModelManager(models.Manager):

    def get_by_natural_key(self, infant_visit):
        return self.get(infant_visit=infant_visit)
