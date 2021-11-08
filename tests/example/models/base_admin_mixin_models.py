from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from tests.example import managers as app_managers
from tests.example import querysets as app_queryset


class BaseExampleModel(models.Model):
    objects = app_managers.BaseExampleModelManager.from_queryset(app_queryset.BaseExampleModelQuerySet)()

    test_boolean = models.BooleanField("Test bool", null=True)
    test_datetime = models.DateTimeField("Test datetime")
    test_fk = models.ForeignKey(
        "example.BaseExampleFkModel",
        verbose_name="Test fk",
        on_delete=models.CASCADE,
        related_name="example_for_base_admin_mixins"
    )
    test_image = models.ImageField("Test image", upload_to="example/images/")
    test_m2m = models.ManyToManyField(
        "example.BaseExampleM2MModel",
        related_name="example_for_base_admin_mixins",
    )
    example_generic_relation_model_for_base_admin_mixin = GenericRelation(
        "example.BaseExampleGenericRelationModel",
        related_query_name='example_model_for_base_admin_mixin'
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Base example model"
        verbose_name_plural = "Base example models"

    @classmethod
    def admin_changelist_url(cls):
        return reverse("admin:example_baseexamplemodel_changelist")

    def get_ct(self):
        return ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.model_name)


class BaseExampleFkModel(models.Model):
    objects = app_managers.BaseExampleFkModelManager.from_queryset(
        app_queryset.BaseExampleFkModelQuerySet
    )()

    test_text = models.TextField("Test text")

    class Meta:
        verbose_name = "Base example FK model"
        verbose_name_plural = "Base example FK models"

    def __str__(self):
        return str(self.test_text)

    @property
    def admin_change_url(self):
        return reverse("admin:example_baseexamplefkmodel_change", kwargs={"object_id": self.id})


class BaseExampleM2MModel(models.Model):
    objects = app_managers.BaseExampleM2MModelManager.from_queryset(
        app_queryset.BaseExampleM2MModelQuerySet
    )()

    test_text = models.TextField("Test text")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Base example M2M model"
        verbose_name_plural = "Base example M2M models"

    @classmethod
    def admin_changelist_url(cls):
        return reverse("admin:example_baseexamplem2mmodel_changelist")

    def get_ct(self):
        return ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.model_name)


class BaseExampleGenericRelationModel(models.Model):
    objects = app_managers.BaseExampleGenericRelationModelManager.from_queryset(
        app_queryset.BaseExampleGenericRelationModelQuerySet
    )()

    test_text = models.TextField("Test text")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    test_generic_fk = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Base example generic relation model"
        verbose_name_plural = "Base example generic relation models"

    def __str__(self):
        return str(self.id)

    @classmethod
    def admin_changelist_url(cls):
        return reverse("admin:example_baseexamplegenericrelationmodel_changelist")

    def get_ct(self):
        return ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.model_name)