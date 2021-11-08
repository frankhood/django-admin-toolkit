from django.db import models

from tests.example.managers import ConfigurableWidgetsExampleModelManager, \
    ConfigurableWidgetsExampleFKModelManager, ConfigurableWidgetsExampleM2MModelManager
from tests.example.querysets import ConfigurableWidgetsExampleModelQuerySet, \
    ConfigurableWidgetsExampleFKModelQuerySet, ConfigurableWidgetsExampleM2MModelQuerySet


class ConfigurableWidgetsExampleM2MModel(models.Model):
    objects = ConfigurableWidgetsExampleM2MModelManager.from_queryset(
        ConfigurableWidgetsExampleM2MModelQuerySet
    )()

    test_text = models.CharField("Test Text", max_length=255, default="", blank=True)

    class Meta:
        verbose_name = "Configurable widgets example M2M model"
        verbose_name_plural = "Configurable widgets example M2M models"

    def __str__(self):
        return self.test_text


class ConfigurableWidgetsExampleFKModel(models.Model):
    objects = ConfigurableWidgetsExampleFKModelManager.from_queryset(
        ConfigurableWidgetsExampleFKModelQuerySet
    )()

    test_text = models.CharField("Test Text", max_length=255, default="", blank=True)

    class Meta:
        verbose_name = "Configurable widgets example FK model"
        verbose_name_plural = "Configurable widgets example FK models"

    def __str__(self):
        return self.test_text


class ConfigurableWidgetsExampleModel(models.Model):
    objects = ConfigurableWidgetsExampleModelManager.from_queryset(
        ConfigurableWidgetsExampleModelQuerySet)()

    test_text = models.CharField("Test Text", max_length=500, default="", blank=True)
    test_fk = models.ForeignKey(
        ConfigurableWidgetsExampleFKModel,
        verbose_name="Test FK",
        on_delete=models.SET_NULL,
        null=True
    )
    test_m2m = models.ManyToManyField(
        ConfigurableWidgetsExampleM2MModel,
        verbose_name="Test M2M"
    )

    class Meta:
        verbose_name = "Configurable widgets example model"
        verbose_name_plural = "Configurable widgets example models"
