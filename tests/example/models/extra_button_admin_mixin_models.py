from django.db import models

from tests.example.managers import ExtraButtonExampleModelManager
from tests.example.querysets import ExtraButtonExampleModelQuerySet


class ExtraButtonExampleModel(models.Model):

    objects = ExtraButtonExampleModelManager.from_queryset(ExtraButtonExampleModelQuerySet)()
    test_text = models.TextField("Test Text", default="", blank=True)

    class Meta:
        verbose_name = "Extra button example model"
        verbose_name_plural = "Extra button example models"
