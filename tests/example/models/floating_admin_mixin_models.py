from django.db import models

from tests.example.managers import FloatingExampleModelManager
from tests.example.querysets import FloatingExampleModelQuerySet


class FloatingExampleModel(models.Model):

    objects = FloatingExampleModelManager.from_queryset(FloatingExampleModelQuerySet)()
    test_text = models.CharField("Test Text", max_length=255)

    class Meta:
        verbose_name = "Floating example model"
        verbose_name_plural = "Floating example models"
