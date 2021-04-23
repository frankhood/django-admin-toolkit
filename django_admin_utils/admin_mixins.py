import logging

from django.contrib.admin.sites import site
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django_admin_utils.widgets import VerboseForeignKeyRawIdWidget, VerboseManyToManyRawIdWidget

logger = logging.getLogger('django-admin-utils')


class AfterSaveMixinAdmin(object):

    def log_addition(self, request, object, message):
        super().log_addition(request, object, message)
        self.after_save(request, object, add=True, message=message)

    def log_change(self, request, object, message):
        super().log_change(request, object, message)
        self.after_save(request, object, add=False, message=message)

    def after_save(self, request, object, add, message):
        """
        It allows you to manage the operations to be performed
        after saving an object and all its inlines
        """
        pass


class ConfigurableWidgetsMixinAdmin(object):
    """
    Use ConfigurableWidgetsMixinAdmin if you want to customize quickly
    default widget/label/help_text or every related admin form configurations
    without doing modifications of the autocreated ModelForm

    You can use it for InlineAdmin, too

    How to use it
    `yourapp/admin.py`

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
    dbfield_overrides = {}
    fkfield_overrides = {}
    m2mfield_overrides = {}

    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        if (self.dbfield_overrides and
                db_field.name in self.dbfield_overrides):
            kwargs.update(
                self.dbfield_overrides[db_field.name]
            )
        return super().formfield_for_dbfield(
            db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if (self.fkfield_overrides and
                db_field.name in self.fkfield_overrides):
            kwargs.update(
                self.fkfield_overrides[db_field.name]
            )
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if (self.m2mfield_overrides and
                db_field.name in self.m2mfield_overrides):
            kwargs.update(
                self.m2mfield_overrides[db_field.name]
            )
        return super().formfield_for_manytomany(
            db_field, request, **kwargs)


class AllReadonlyAdminMixin(object):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return [x.name for x in self.model._meta.fields] + list(readonly_fields)
        return [] + list(readonly_fields)

    def has_add_permission(self, request):
        return False


class AllReadonlyAdminInlineMixin(object):

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        result = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        if 'id' in result:
            result.remove('id')
        return result + list(readonly_fields) or []

    def has_add_permission(self, request):
        return False


class DetailInInlineAdminMixin(object):
    class Media:
        js = []
        css = {
            'all': ('templates/admin/css/admin_buttons.css',),
        }

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        return ['display_inline_obj'] + list(fields)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        return ['display_inline_obj'] + list(readonly_fields)

    def display_inline_obj(self, obj):
        if obj and obj.id:
            return mark_safe('<a href="{0}" target="_blank" class="admin-button admin-button-success">Dettaglio</a>\
            '.format(obj.admin_change_url, ))
        return '---'
    display_inline_obj.short_description = _("Link")
    display_inline_obj.allow_tags = True


class EmptyValueMixinAdmin(object):
    empty_values = {}

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if hasattr(self,
                   'empty_values') and db_field.name in self.empty_values.keys():
            kwargs['empty_label'] = self.empty_values[db_field.name]
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ExtraButtonAdminMixin(object):
    # extra_button dict:
    # * label
    # * url
    # * class
    extra_button = None

    change_list_template = 'templates/admin/change_list_with_extrabuttons.html'

    def get_extra_button(self, request):
        return self.extra_button

    def changelist_view(self, request, extra_context=None):
        extra_button = self.get_extra_button(request)
        if extra_button:
            extra_context = extra_context or {}
            extra_context['extra_buttons'] = extra_button
        return super().changelist_view(request, extra_context)


class FloatingAdminMixin(object):
    """ Inherit from this class to collapse filters in ChangeListView """

    class Media:
        js = (
            'templates/admin/js/jquery.tabSlideOut.v1.3.js',
            'templates/admin/js/admin_floating.js',
        )
        css = {
            'all': ('templates/admin/css/admin_floating.css',),
        }


class ImproveRawIdFieldsAdminMixin(object):  # admin.ModelAdmin
    """
    in your admin.py insert

    class YourModelAdmin(ImproveRawIdFieldsAdminMixin,admin.ModelAdmin):
        ...
        improved_raw_id_fields = ['user','events']
        ...
    """

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.improved_raw_id_fields:
            kwargs.pop("request", None)
            type = db_field.rel.__class__.__name__
            if type == "ManyToOneRel":
                kwargs['widget'] = VerboseForeignKeyRawIdWidget(db_field.rel, site)
            elif type == "ManyToManyRel":
                kwargs['widget'] = VerboseManyToManyRawIdWidget(db_field.rel, site)
            return db_field.formfield(**kwargs)
        return super().formfield_for_dbfield(db_field, **kwargs)

