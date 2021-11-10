from django.db import models

from tests.example.managers import AdminFilterExampleModelManager
from tests.example.querysets import AdminFilterExampleModelQuerySet


TEST_CHOICES = (
    ("test_one", "Test One"),
    ("test_two", "Test Two"),
    ("test_three", "Test Three"),
    ("test_four", "Test Four"),
)


class AdminFilterExampleModel(models.Model):

    objects = AdminFilterExampleModelManager.from_queryset(
        AdminFilterExampleModelQuerySet
    )()

    test_char = models.CharField(
        "Test char", max_length=255, blank=True, default=""
    )
    test_choice = models.CharField(
        "Test choice", choices=TEST_CHOICES, max_length=64, default="", blank=True
    )
    test_fk = models.ForeignKey(
        "self", verbose_name="Test FK", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Admin filter example model"
        verbose_name_plural = "Admin filter example models"

    def __str__(self):
        return self.test_char
