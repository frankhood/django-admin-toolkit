from django.db import models

from tests.example import managers as app_managers
from tests.example import querysets as app_querysets


class AdminFilterM2MExampleModel(models.Model):

    objects = app_managers.AdminFilterM2MExampleModelManager.from_queryset(
        app_querysets.AdminFilterM2MExampleModelQuerySet
    )()

    test_char = models.CharField("Test char", max_length=255, blank=True, default="")

    class Meta:
        """AdminFilterM2MExampleModel Meta."""

        verbose_name = "Admin filter m2m example model"
        verbose_name_plural = "Admin filter m2m plural example model"


TEST_CHOICES = (
    ("test_one", "Test One"),
    ("test_two", "Test Two"),
    ("test_three", "Test Three"),
    ("test_four", "Test Four"),
)


class AdminFilterExampleModel(models.Model):

    objects = app_managers.AdminFilterExampleModelManager.from_queryset(
        app_querysets.AdminFilterExampleModelQuerySet
    )()

    test_char = models.CharField("Test char", max_length=255, blank=True, default="")
    test_choice = models.CharField(
        "Test choice", choices=TEST_CHOICES, max_length=64, default="", blank=True
    )
    test_fk = models.ForeignKey(
        "self", verbose_name="Test FK", on_delete=models.SET_NULL, null=True, blank=True
    )
    test_m2m = models.ManyToManyField("example.AdminFilterM2MExampleModel", blank=True)

    class Meta:
        """AdminFilterExampleModel Meta."""

        verbose_name = "Admin filter example model"
        verbose_name_plural = "Admin filter example models"

    def __str__(self):
        return self.test_char
