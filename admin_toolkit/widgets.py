from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.contrib.admin import widgets
from django.urls import reverse

logger = logging.getLogger("django-admin-toolkit")


class VerboseForeignKeyRawIdWidget(widgets.ForeignKeyRawIdWidget):
    def label_and_url_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.model._default_manager.using(self.db).get(**{key: value})
            change_url = reverse(
                "admin:%s_%s_change"
                % (obj._meta.app_label, obj._meta.model_name.lower()),
                kwargs={"object_id": obj.pk},
            )
            return obj.__str__(), change_url
        except (ValueError, self.rel.related_model.DoesNotExist):
            return "???", "admin/"


class VerboseManyToManyRawIdWidget(widgets.ManyToManyRawIdWidget):
    def label_and_url_for_value(self, value):
        changelist_ids = []
        key = self.rel.get_related_field().name
        for v in value:
            try:
                obj = self.rel.model._default_manager.using(self.db).get(**{key: v})
                changelist_ids.append(obj.id)
            except self.rel.model.DoesNotExist:
                pass

        change_url = (
            reverse(
                "admin:%s_%s_changelist"
                % (obj._meta.app_label, obj._meta.model_name.lower()),
            )
            + f"?{key}__in={','.join(str(id) for id in changelist_ids)}"
        )

        return f"{len(changelist_ids)} {obj._meta.verbose_name_plural}", change_url
