import uuid

from django.contrib import admin

from django_admin_toolkit.admin_mixins import AfterSaveMixinAdmin
from tests.example.models import AfterSaveExample


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
