from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from admin_toolkit import admin_mixins
from admin_toolkit.admin_filters import RelatedSelectFilter, SelectFilter
from tests.example import admin_filters as app_admin_filters
from tests.example import models as app_models


@admin.register(app_models.BaseExampleFkModel)
class BaseExampleFkModelAdmin(admin_mixins.BaseAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text",)


@admin.register(app_models.BaseExampleM2MModel)
class BaseExampleM2MModelAdmin(admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text",)


@admin.register(app_models.BaseExampleGenericRelationModel)
class BaseExampleGenericRelationModelAdmin(admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text", "content_type", "object_id")


@admin.register(app_models.BaseExampleModel)
class BaseExampleModelAdmin(admin_mixins.BaseAdminMixin, admin.ModelAdmin):
    list_display = (
        "__str__",
        "display_test_boolean",
        "display_test_datetime",
        "display_test_date",
        "display_test_time",
        "display_test_fk",
        "display_test_image",
        "display_test_m2m",
        "display_generic_relation",
    )
    fields = ("test_boolean", "test_datetime", "test_fk", "test_image", "test_m2m")
    readonly_fields = (
        "display_test_boolean",
        "display_test_datetime",
        "display_test_date",
        "display_test_time",
        "display_test_fk",
        "display_test_image",
        "display_test_m2m",
        "display_generic_relation",
    )

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
            return self._display_m2m_objects(
                obj, m2m_field_name="test_m2m", label="Example M2Ms"
            )
        return ""

    @mark_safe
    def display_generic_relation(self, obj):
        if obj and obj.id:
            return self._display_generic_related_objects(
                obj,
                "example_generic_relation_model_for_base_admin_mixin",
                "Example Generic Relations",
            )
        return ""


@admin.register(app_models.AfterSaveExampleModel)
class AfterSaveExampleModelAdmin(admin_mixins.AfterSaveAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "test_text")
    fields = ("test_text",)


class AllReadonlyExampleModelAdminInline(
    admin_mixins.AllReadonlyAdminInlineMixin, admin.TabularInline
):
    model = app_models.AllReadonlyExampleModel
    fields = ("test_text",)


@admin.register(app_models.AllReadonlyExampleModel)
class AllReadonlyExampleModelAdmin(
    admin_mixins.AllReadonlyAdminMixin, admin.ModelAdmin
):
    list_display = (
        "id",
        "test_text",
    )
    fields = ("test_text",)
    inlines = [AllReadonlyExampleModelAdminInline]


@admin.register(app_models.ConfigurableWidgetsExampleM2MModel)
class ConfigurableWidgetsExampleM2MModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "test_text",
    )
    fields = ("test_text",)


@admin.register(app_models.ConfigurableWidgetsExampleFKModel)
class ConfigurableWidgetsExampleFKModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "test_text",
    )
    fields = ("test_text",)


@admin.register(app_models.ConfigurableWidgetsExampleModel)
class ConfigurableWidgetsExampleModelAdmin(
    admin_mixins.ConfigurableWidgetsAdminMixin, admin.ModelAdmin
):
    list_display = (
        "id",
        "test_text",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("test_text",),
                    (
                        "test_fk",
                        "test_m2m",
                    ),
                )
            },
        ),
    )
    filter_horizontal = ("test_m2m",)
    dbfield_overrides = {
        "test_text": {
            "help_text": "Test Text Example help text",
            "widget": forms.Textarea,
        },
    }
    fkfield_overrides = {
        "test_fk": {
            "help_text": "Test FK Example help text",
            "widget": forms.RadioSelect,
        },
    }
    m2mfield_overrides = {
        "test_m2m": {
            "help_text": "Test M2M Example help text",
            "widget": forms.CheckboxSelectMultiple,
        }
    }


class DetailInInlineExampleModelAdminInline(
    admin_mixins.DetailInInlineAdminMixin, admin.TabularInline
):
    fields = ("test_text",)
    model = app_models.DetailInInlineExampleModel


@admin.register(app_models.DetailInInlineExampleModel)
class DetailInInlineExampleModelAdmin(admin.ModelAdmin):
    list_display = ("id", "test_text")
    fields = ("test_text",)
    inlines = [DetailInInlineExampleModelAdminInline]


@admin.register(app_models.EmptyValueExampleModel)
class EmptyValueExampleModelAdmin(admin_mixins.EmptyValueAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "test_text",
        "test_fk",
    )
    fields = ("test_text", "test_fk")
    empty_values = {"test_fk": _("NO TEST FK")}


@admin.register(app_models.ExtraButtonExampleModel)
class ExtraButtonExampleModelAdmin(
    admin_mixins.ExtraButtonAdminMixin, admin.ModelAdmin
):
    list_display = ("id", "test_text")
    fields = ("test_text",)
    extra_button = [
        {"label": "Example Extra Button", "url": "http://example.com", "class": ""}
    ]


@admin.register(app_models.FloatingExampleModel)
class FloatingExampleModelAdmin(admin_mixins.FloatingAdminMixin, admin.ModelAdmin):
    list_display = ("id", "test_text")
    list_filter = ("test_text",)
    fields = ("test_text",)


@admin.register(app_models.ImprovedRawIdFieldsExampleRelatedModel)
class ImprovedRawIdFieldsExampleRelatedModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "test_name",
    )
    fieldsets = ((None, {"fields": (("test_name",),)}),)


@admin.register(app_models.ImprovedRawIdFieldsExampleModel)
class ImprovedRawIdFieldsExampleModelAdmin(
    admin_mixins.ImprovedRawIdFieldsAdminMixin, admin.ModelAdmin
):
    improved_raw_id_fields = ["test_fk", "test_m2m"]
    list_display = (
        "id",
        "test_name",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("test_name",),
                    ("test_fk", "test_m2m"),
                )
            },
        ),
    )


@admin.register(app_models.AdminFilterM2MExampleModel)
class AdminFilterM2MExampleModelAdmin(admin.ModelAdmin):
    list_display = ("id", "test_char")
    fieldsets = ((None, {"fields": (("test_char",),)}),)


@admin.register(app_models.AdminFilterExampleModel)
class AdminFilterExampleModelAdmin(admin.ModelAdmin):
    list_display = ("id", "test_char", "get_test_choice_display", "test_fk")
    list_filter = (
        app_admin_filters.SimpleBooleanTestInTestCharFilter,
        ("test_choice", SelectFilter),
        ("test_fk", RelatedSelectFilter),
        ("test_fk", app_admin_filters.CustomRelatedSelectFilterForTestFK),
        ("test_m2m", app_admin_filters.CustomRelatedSelectFilterForTestM2M),
    )
    fieldsets = (
        (None, {"fields": (("test_char", "test_choice", "test_fk", "test_m2m"),)}),
    )
