from django.db import models

from tests.example.managers import ImprovedRawIdFieldsExampleModelManager, \
    ImprovedRawIdFieldsExampleRelatedModelManager
from tests.example.querysets import ImprovedRawIdFieldsExampleModelQuerySet, \
    ImprovedRawIdFieldsExampleRelatedModelQuerySet


class ImprovedRawIdFieldsExampleRelatedModel(models.Model):

    objects = ImprovedRawIdFieldsExampleRelatedModelManager.from_queryset(ImprovedRawIdFieldsExampleRelatedModelQuerySet)()

    test_name = models.CharField("Test Name", max_length=255)

    class Meta:
        verbose_name = "Improve raw id fields example related model"
        verbose_name_plural = "Improve raw id fields example related models"

    def __str__(self):
        return self.test_name


class ImprovedRawIdFieldsExampleModel(models.Model):

    test_name = models.CharField("Test Name", max_length=255)
    test_fk = models.ForeignKey(
        ImprovedRawIdFieldsExampleRelatedModel,
        verbose_name="Test FK",
        on_delete=models.SET_NULL, null=True,
        related_name="related_test_fk",
        related_query_name="related_test_fk",
    )
    test_m2m = models.ManyToManyField(
        ImprovedRawIdFieldsExampleRelatedModel,
        verbose_name="Test M2M",
        related_name="related_test_m2m",
        related_query_name="related_test_m2m",
    )

    objects = ImprovedRawIdFieldsExampleModelManager.from_queryset(
        ImprovedRawIdFieldsExampleModelQuerySet)()

    class Meta:
        verbose_name = "Improve raw id fields example model"
        verbose_name_plural = "Improve raw id fields example models"

    def __str__(self):
        return self.test_name