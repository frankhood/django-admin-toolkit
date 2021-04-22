import uuid

from django.contrib import admin
from django.utils.safestring import mark_safe

from django_admin_utils.admin_mixins import AfterSaveMixinAdmin, BaseAdminMixin
from tests.example.models import AfterSaveExample, BaseAdminExample


@admin.register(AfterSaveExample)
class AfterSaveExampleAdmin(AfterSaveMixinAdmin, admin.ModelAdmin):
    list_display = (
        'title',
        'uuid'
    )
    readonly_fields = (
        'uuid',
    )
    fieldsets = (
        (None, {'fields': (
            ('title', 'uuid'),
        )}),
    )

    def after_save(self, request, object, add, message):
        object.uuid = str(uuid.uuid4())
        object.save()


@admin.register(BaseAdminExample)
class BaseAdminExampleAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'display_datetime',
        'display_date',
        'display_time',
        'display_boolean',
        'display_after_save_fk_example',
        'display_after_save_m2m_example',
    )
    fieldsets = (
        (None, {'fields': (
            ('image',),
            ('datetime', 'date', 'time'),
            ('boolean',),
            ('after_save_fk_example', 'after_save_m2m_example'),
        )}),
    )

    def display_image(self, obj):
        if obj and obj.image:
            return mark_safe(self._display_image(obj.image))
        return ''

    def display_datetime(self, obj):
        if obj and obj.datetime:
            return self._display_datetime(obj.datetime)
        return ''

    def display_date(self, obj):
        if obj and obj.datetime:
            return self._display_date(obj.datetime)
        return ''

    def display_time(self, obj):
        if obj and obj.datetime:
            return self._display_time(obj.datetime)
        return ''

    def display_boolean(self, obj):
        if obj and obj.boolean:
            return self._display_boolean(obj.boolean)
        return ''

    def display_after_save_fk_example(self, obj):
        if obj and obj.after_save_fk_example:
            return mark_safe(self._display_fk_object(obj.after_save_fk_example))
        return ''

    def display_after_save_m2m_example(self, obj):
        if obj and obj.after_save_fk_example:
            return mark_safe(self._display_m2m_objects(obj, 'after_save_m2m_example'))
        return ''
