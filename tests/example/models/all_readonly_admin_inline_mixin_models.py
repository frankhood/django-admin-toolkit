from django.db import models

from tests.example.managers import AllReadonlyExampleModelManager
from tests.example.querysets import AllReadonlyExampleModelQuerySet


class AllReadonlyExampleModel(models.Model):
    objects = AllReadonlyExampleModelManager.from_queryset(
        AllReadonlyExampleModelQuerySet)()

    test_text = models.TextField("Test Text", blank=True)
    test_fk = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "All readonly example model"
        verbose_name_plural = "All readonly example models"
