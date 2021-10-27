from django.contrib import admin
from django.utils.safestring import mark_safe

from admin_toolkit.admin import BaseAdminMixin, AfterSaveAdminMixin
from tests.example import models


@admin.register(models.ExampleFkModelForBaseAdminMixin)
class ExampleFkModelForBaseAdminMixinAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text",)


@admin.register(models.ExampleM2MModelForBaseAdminMixin)
class ExampleM2MModelForBaseAdminMixinAdmin(admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text",)


@admin.register(models.ExampleGenericRelationModelForBaseAdminMixin)
class ExampleGenericRelationModelForBaseAdminMixinAdmin(admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text",)


@admin.register(models.ExampleModelForBaseAdminMixin)
class ExampleModelForBaseAdminMixinAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = (
        "__str__",
        "display_test_boolean",
        "display_test_datetime",
        "display_test_date",
        "display_test_time",
        "display_test_fk",
        "display_test_image",
        "display_test_m2m",
    )
    fields = ("test_boolean", "test_datetime", "test_fk", "test_image", "test_m2m")

    @mark_safe
    def display_test_boolean(self, obj):
        if obj and obj.test_boolean:
            return self._display_boolean(obj.test_boolean)
        return ""

    @mark_safe
    def display_test_datetime(self, obj):
        if obj and obj.test_datetime:
            return self._display_datetime(obj.test_datetime)
        return ""

    @mark_safe
    def display_test_date(self, obj):
        if obj and obj.test_datetime:
            return self._display_date(obj.test_datetime)
        return ""

    @mark_safe
    def display_test_time(self, obj):
        if obj and obj.test_datetime:
            return self._display_time(obj.test_datetime)
        return ""

    @mark_safe
    def display_test_fk(self, obj):
        if obj and obj.test_fk:
            return self._display_fk_object(obj.test_fk)
        return ""

    @mark_safe
    def display_test_image(self, obj):
        if obj and obj.test_image:
            return self._display_image(obj.test_image)
        return ""

    @mark_safe
    def display_test_m2m(self, obj):
        if obj and obj.test_m2m:
            return self._display_m2m_objects(obj, m2m_field_name="test_m2m")
        return ""


@admin.register(models.ExampleModelForAfterSaveAdminMixin)
class ExampleModelForAfterSaveAdminMixinAdmin(AfterSaveAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text",)
