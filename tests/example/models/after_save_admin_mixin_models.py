from django.db import models

from tests.example import managers as app_managers
from tests.example import querysets as app_queryset


class AfterSaveExampleModel(models.Model):
    objects = app_managers.AfterSaveExampleModelManager.from_queryset(
        app_queryset.AfterSaveExampleModelQuerySet
    )()

    test_text = models.TextField("Test text")

    class Meta:
        verbose_name = "After save example model"
        verbose_name_plural = "After save example models"

    def __str__(self):
        return str(self.id)