from django.db import models

from tests.example import managers as app_managers
from tests.example import querysets as app_queryset


class ExampleModelForAfterSaveAdminMixin(models.Model):
    objects = app_managers.ExampleModelForAfterSaveAdminMixinManager.from_queryset(
        app_queryset.ExampleModelForAfterSaveAdminMixinQuerySet
    )()

    test_text = models.TextField("Test text")

    def __str__(self):
        return str(self.id)
