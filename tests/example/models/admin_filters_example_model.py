from django.db import models

from tests.example.managers import AdminFilterExampleModelManager
from tests.example.querysets import AdminFilterExampleModelQuerySet


class AdminFilterExampleModel(models.Model):

    objects = AdminFilterExampleModelManager.from_queryset(
        AdminFilterExampleModelQuerySet
    )()

    test_char = models.CharField(
        "Test filter boolean", max_length=255, blank=True, default=""
    )
    test_fk = models.ForeignKey(
        "self", verbose_name="Test FK", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Admin filter example model"
        verbose_name_plural = "Admin filter example models"

    def __str__(self):
        return self.test_char
