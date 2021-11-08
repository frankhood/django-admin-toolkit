from django.db import models

from tests.example.managers import EmptyValueExampleModelManager
from tests.example.querysets import EmptyValueExampleModelQuerySet


class EmptyValueExampleModel(models.Model):

    objects = EmptyValueExampleModelManager.from_queryset(EmptyValueExampleModelQuerySet)()

    test_text = models.TextField("Test Text", default="", blank=True)
    test_fk = models.ForeignKey("self", verbose_name="Test FK", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Empty value example model"
        verbose_name_plural = "Empty value example models"

