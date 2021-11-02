from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from tests.example import managers as app_managers
from tests.example import querysets as app_queryset


class ExampleModelForBaseAdminMixin(models.Model):
    objects = app_managers.ExampleModelForBaseAdminMixinManager.from_queryset(app_queryset.ExampleModelForBaseAdminMixinQuerySet)()

    test_boolean = models.BooleanField("Test bool", null=True)
    test_datetime = models.DateTimeField("Test datetime")
    test_fk = models.ForeignKey(
        "example.ExampleFkModelForBaseAdminMixin",
        verbose_name="Test fk",
        on_delete=models.CASCADE,
        related_name="example_for_base_admin_mixins"
    )
    test_image = models.ImageField("Test image", upload_to="example/images/")
    test_m2m = models.ManyToManyField(
        "example.ExampleM2MModelForBaseAdminMixin",
        related_name="example_for_base_admin_mixins",
    )
    example_generic_relation_model_for_base_admin_mixin = GenericRelation(
        "example.ExampleGenericRelationModelForBaseAdminMixin",
        related_query_name='example_model_for_base_admin_mixin'
    )

    def __str__(self):
        return str(self.id)

    @classmethod
    def admin_changelist_url(cls):
        return reverse("admin:example_examplemodelforbaseadminmixin_changelist")

    def get_ct(self):
        return ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.model_name)


class ExampleFkModelForBaseAdminMixin(models.Model):
    objects = app_managers.ExampleFkModelForBaseAdminMixinManager.from_queryset(
        app_queryset.ExampleFkModelForBaseAdminMixinQuerySet
    )()

    test_text = models.TextField("Test text")

    def __str__(self):
        return str(self.id)

    @property
    def admin_change_url(self):
        return reverse("admin:example_examplefkmodelforbaseadminmixin_change", kwargs={"object_id": self.id})


class ExampleM2MModelForBaseAdminMixin(models.Model):
    objects = app_managers.ExampleM2MModelForBaseAdminMixinManager.from_queryset(
        app_queryset.ExampleM2MModelForBaseAdminMixinQuerySet
    )()

    test_text = models.TextField("Test text")

    def __str__(self):
        return str(self.id)

    @classmethod
    def admin_changelist_url(cls):
        return reverse("admin:example_examplem2mmodelforbaseadminmixin_changelist")

    def get_ct(self):
        return ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.model_name)


class ExampleGenericRelationModelForBaseAdminMixin(models.Model):
    objects = app_managers.ExampleGenericRelationModelForBaseAdminMixinManager.from_queryset(
        app_queryset.ExampleGenericRelationModelForBaseAdminMixinQuerySet
    )()

    test_text = models.TextField("Test text")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    test_generic_fk = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.id)

    @classmethod
    def admin_changelist_url(cls):
        return reverse("admin:example_examplegenericrelationmodelforbaseadminmixin_changelist")

    def get_ct(self):
        return ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.model_name)