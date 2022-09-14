# -*- coding: utf-8 -*-

import logging
from typing import Dict, List, Optional

from django.contrib import admin
from django.contrib.admin.sites import site
from django.template.defaultfilters import yesno
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils.timezone import get_current_timezone, localtime
from django.utils.translation import gettext_lazy as _

from .widgets import VerboseForeignKeyRawIdWidget, VerboseManyToManyRawIdWidget

logger = logging.getLogger("django-admin-toolkit")


class AfterSaveAdminMixin(admin.ModelAdmin):
    def log_addition(self, request, object, message):
        log = super().log_addition(request, object, message)
        self.after_save(request, object, add=True, message=message)
        return log

    def log_change(self, request, object, message):
        log = super().log_change(request, object, message)
        self.after_save(request, object, add=False, message=message)
        return log

    def after_save(self, request, object, add, message):
        """Allow you to manage the operations to be performed after saving an object and all its inlines."""
        pass


class AllReadonlyAdminMixin(object):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return [x.name for x in self.model._meta.fields] + list(readonly_fields)
        return [] + list(readonly_fields)

    def has_add_permission(self, request, obj=None):
        return False


class AllReadonlyAdminInlineMixin(object):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        result = list(
            set(
                [field.name for field in self.opts.local_fields]
                + [field.name for field in self.opts.local_many_to_many]
            )
        )
        if "id" in result:
            result.remove("id")
        return result + list(readonly_fields) or []

    def has_add_permission(self, request, obj=None):
        return False


class DetailInInlineAdminMixin(object):
    class Media:
        """DetailInInlineAdminMixin Media."""

        css = {
            "all": ("css/admin_buttons.css",),
        }

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        return ["display_inline_obj"] + list(fields)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        return ["display_inline_obj"] + list(readonly_fields)

    @admin.display(description=_("Link"))
    def display_inline_obj(self, obj):
        if obj and obj.id:
            return mark_safe(
                '<a href="{0}" target="_blank" class="admin-button admin-button-success">{1}</a>'.format(
                    obj.admin_change_url, _("Detail")
                )
            )
        return "---"


class EmptyValueAdminMixin(object):
    empty_values: Dict = {}

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if hasattr(self, "empty_values") and db_field.name in self.empty_values.keys():
            kwargs["empty_label"] = self.empty_values[db_field.name]
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ExtraButtonAdminMixin(object):
    # extra_button dict:
    # * label
    # * url
    # * class
    extra_button: Optional[List] = None

    change_list_template = "admin/change_list_with_extrabuttons.html"

    def get_extra_button(self, request):
        return self.extra_button

    def changelist_view(self, request, extra_context=None):
        extra_button = self.get_extra_button(request)
        if extra_button:
            extra_context = extra_context or {}
            extra_context["extra_buttons"] = extra_button
        return super().changelist_view(request, extra_context)


class FloatingAdminMixin(object):
    """Inherit from this class to collapse filters in ChangeListView."""

    filter_image = "img/fh_filter.png"
    change_list_template = "admin/change_list_floating_filter.html"

    class Media:
        """FloatingAdminMixin Media."""

        js = (
            "js/jquery.tabSlideOut.v1.3.js",
            "js/admin_floating.js",
        )
        css = {
            "all": ("css/admin_floating.css",),
        }

    def get_filter_image(self):
        return self.filter_image

    def changelist_view(self, request, extra_context=None):
        extra_context = {"filter_image_url": static(self.get_filter_image())}
        return super().changelist_view(request, extra_context)


class ImprovedRawIdFieldsAdminMixin(object):  # admin.ModelAdmin
    """
    Insert your admin_mixins.py.

    class YourModelAdmin(ImprovedRawIdFieldsAdminMixin,admin.ModelAdmin):
        ...
        improved_raw_id_fields = ['user','events']
        ...
    """

    improved_raw_id_fields: List = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.improved_raw_id_fields:
            kwargs.pop("request", None)
            type = db_field.remote_field.__class__.__name__
            if type == "ManyToOneRel":
                kwargs["widget"] = VerboseForeignKeyRawIdWidget(
                    db_field.remote_field, site
                )
            elif type == "ManyToManyRel":
                kwargs["widget"] = VerboseManyToManyRawIdWidget(
                    db_field.remote_field, site
                )
            return db_field.formfield(**kwargs)
        return super().formfield_for_dbfield(db_field, **kwargs)


class ConfigurableWidgetsAdminMixin(object):
    """
    Customize quickly default widget/label/help_text.

    or every related admin form configurations
    without doing modifications of the autocreated ModelForm

    You can use it for InlineAdmin, too

    How to use it
    `yourapp/admin_mixins.py`

    from django.contrib import admin
    from fhcore.apps.db.admin.mixins import ConfigurableWidgetsMixinAdmin
    from .models import MyModel

    ...

    @admin.register(MyModel)
    class MyModelAdmin(ConfigurableWidgetsMixinAdmin, admin.ModelAdmin):

    ...

        dbfield_overrides = {
             'content': {'widget': CKEditor()},
             'description': {'widget': redactor.widgets.RedactorEditor()},
             'json_data' : {'widget': prettyjson.PrettyJSONWidget(attrs={'initial': 'parsed'})},
             'image': {'widget': fhcore.apps.db.widgets.easy_thumbnail_image_widget.ConfigurableImageWidget({'width':80,'height':80})},
        }

        fkfield_overrides = {
            'fk_field': {'help_text': _("Modify me!")}
        }

        m2mfield_overrides = {
            'widget':CheckboxSelectMultiple()
        }

    """

    dbfield_overrides: Dict = {}
    fkfield_overrides: Dict = {}
    m2mfield_overrides: Dict = {}

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        if self.dbfield_overrides and db_field.name in self.dbfield_overrides:
            kwargs.update(self.dbfield_overrides[db_field.name])
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if self.fkfield_overrides and db_field.name in self.fkfield_overrides:
            kwargs.update(self.fkfield_overrides[db_field.name])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if self.m2mfield_overrides and db_field.name in self.m2mfield_overrides:
            kwargs.update(self.m2mfield_overrides[db_field.name])
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class BaseAdminMixin(object):
    def _display_image(self, img_field, width=80, height=80, show_link=True):
        html_tag = (
            "<img src='{img_field.url}' width='{width}' heigth='{height}' />".format(
                img_field=img_field, width=width, height=height
            )
        )
        if show_link:
            html_tag = "<a href='{img_field.url}' target='_blank'>{img_tag}</a>".format(
                img_field=img_field, img_tag=html_tag
            )
        return html_tag

    def _display_datetime(self, datetime_field):
        return formats.date_format(
            localtime(datetime_field, get_current_timezone()), "SHORT_DATETIME_FORMAT"
        )

    def _display_date(self, date_field):
        return formats.date_format(date_field, "SHORT_DATE_FORMAT")

    def _display_time(self, time_field):
        return formats.date_format(time_field, "H:i")

    def _display_boolean(self, boolean_field):
        return yesno(boolean_field)

    def _display_fk_object(self, fk_field):
        """
        Use this method in your admin to display your fk object link.

        >> your_models.py

        class Device(..):
            user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="devices")

        >> your_admin.py

        @admin.register(Device, DeviceAdmin):
        class DeviceAdmin(...):

            def display_user(self, obj):
                if obj and obj.user:
                    return mark_safe(self._display_fk_object(obj.user))
                return "-"
            display_user.short_description = _("User")
        """
        return '<a href="{0}" target="_blank">{1}</a>' "".format(
            fk_field.admin_change_url, fk_field
        )

    def _display_m2m_objects(self, obj, m2m_field_name, label="elements"):
        """
        Use this method in your admin to display your m2m objects filtered changelist's link.

        >> your_models.py

        class Device(..):
            users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="devices")

        >> your_admin.py

        @admin.register(Device, DeviceAdmin):
        class DeviceAdmin(...):

            def display_users(self, obj):
                if obj and obj.users.exists():
                    return mark_safe(self._display_m2m_objects(obj, users))
                return "-"
            display_users.short_description = _("Users")
        """
        return self._display_related_objects(obj, m2m_field_name, label)

    def _display_related_objects(
        self, obj, related_field_name, label="elements", show_generic_link=True
    ):
        """
        Use this method in your admin to display your 1..N or N..N objects (from related model) filtered changelist's link.
        set show_generic_link to false to show a list of all related objects links

        Example:

        >> your_models.py

        class Device(..):
            users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="devices")

        >> your_admin.py

        @admin.register(User, UserAdmin):
        class UserAdmin(...):

            def display_devices(self, obj):
                if obj and obj.devices.exists():
                    return mark_safe(self._display_related_objects(obj, devices, "devices"))
                return "-"
            display_devices.short_description = _("Devices")
        """
        related_manager = getattr(obj, related_field_name)
        try:
            # N..N direct and related
            related_name = related_manager.query_field_name
        except AttributeError:
            # 1..N
            related_name = related_manager.field.name
        related_model = related_manager.model
        if show_generic_link:
            url = "{}?{}__id__exact={}".format(
                related_model.admin_changelist_url(), related_name, obj.id
            )
            elements_count = related_manager.count()
            return (
                '<a href="{url}" target="_blank">Display {elements_count} {label}</a>'
                "".format(url=url, elements_count=elements_count, label=label)
            )
        else:
            return "<br>".join(
                f"""<a href='{reverse_lazy(f"admin:{related_obj._meta.app_label}_{related_obj._meta.model_name}_change", kwargs={"object_id": related_obj.id})}' target='_blank'>{related_obj.__str__()}</a>"""
                for related_obj in related_manager.all()
            )

    def _display_generic_related_objects(
        self, obj, related_field_name, label="elements"
    ):
        """
        Use this method in your admin to display your 1..N or N..N objects (from related model) filtered changelist's link.

        Example:

        >> your_models.py

        class Tag(..):
            content_type = models.ForeignKKey(ContentType, blank=True, null=True,
                                     on_delete=models.SET_NULL)
            object_id = models.PositiveIntegerField(blank=True, null=True)
            content_object = GenericForeignKey('content_type', 'object_id')

        ...

        class TaggedItem(..):
            tags = GenericRelation(Tag, related_query_name='tagged_items')

        >> your_admin.py

        @admin.register(TaggedItem, TaggedItemAdmin):
        class TaggedItemAdmin(...):

            def display_tags(self, obj):
                if obj and obj.tags.exists():
                    return mark_safe(self._display_generic_related_objects(obj, tags, "tags"))
                return "-"
            display_tags.short_description = _("Tags")

        """
        # @TODO use .remote_field
        related_manager = getattr(obj, related_field_name)
        related_model = related_manager.model
        url = "{}?{}__id__exact={}&{}__id__exact={}".format(
            related_model.admin_changelist_url(),
            related_manager.content_type_field_name,
            obj.get_ct().id,
            related_manager.object_id_field_name,
            obj.id,
        )
        elements_count = related_manager.count()
        return (
            '<a href="{url}" target="_blank">Display {elements_count} {label}</a>'
            "".format(url=url, elements_count=elements_count, label=label)
        )
