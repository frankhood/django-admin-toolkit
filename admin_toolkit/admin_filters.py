from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.contrib import admin, messages
from django.contrib.admin import filters
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django-admin-toolkit")


class SimpleBooleanListFilter(admin.SimpleListFilter):
    title = ""  # _('Your Filter Label')
    parameter_name = ""  # 'your_filter_key'
    LOOKUP_CHOICES = (
        ("1", _("Yes")),
        ("0", _("No")),
    )

    def lookups(self, request, model_admin):
        return self.LOOKUP_CHOICES

    def get_allowed_values(self):
        return dict(self.LOOKUP_CHOICES).keys()

    def get_true_queryset_values(self, queryset):
        raise NotImplementedError()

    def get_false_queryset_values(self, queryset):
        raise NotImplementedError()

    def queryset(self, request, queryset):
        _value = self.value()
        if _value in self.get_allowed_values():
            if bool(int(_value)):
                return self.get_true_queryset_values(queryset)
            else:
                return self.get_false_queryset_values(queryset)
        if self.value():
            messages.add_message(
                request,
                messages.WARNING,
                _(
                    "Impossible to filter with the argument '{0}' for the key '{1}'"
                ).format(self.value(), self.title),
            )
        return queryset


class SelectFilter(filters.ChoicesFieldListFilter):
    """
    Replace normal django admin filters with a select for your field with choices
    Use it adding in your admin:
    list_filter= (
        isPublished,
        'field',
        ...
        ('your_choice_field',SelectFilter),#'country
    )
    """

    template = "admin/filter_select.html"


class RelatedSelectFilter(filters.RelatedFieldListFilter):
    """
    Replace normal django admin filters with a select for your fk field
    Use it adding in your admin:
    list_filter= (
        isPublished,
        'field',
        ...
        ('your_fk_field',RelatedSelectFilter),
    )
    """

    template = "admin/filter_select.html"


class CustomRelatedSelectFilter(RelatedSelectFilter):
    """
    Filter Advanced:
    Tnx to `limit_to_currently_related=True` you can see
    in the filters only related models really associated,
    ordered by `get_related_order` method
    tnx to the related manage specified in `get_related_model_field_name`

    Example implementation:

    class EventForEventAttendeeMeetingRelatedSelectFilter(EventRelatedSelectFilter):
        def get_related_model_field_name(self,field):
            return 'eventattendees'

        def get_related_order(self):
            return ['slug']

        def field_choices(self, field, request, model_admin):
            return self.get_related_field_choices(
                field,
                include_blank=False,
                limit_to_currently_related=False
            )

    """

    related_manager = None

    def get_related_order(self):
        return []

    def get_related_model_field_name(self, field):
        return field.related_model._meta.model_name

    def get_related_field_choices(
        self,
        field,
        include_blank=True,
        blank_choice=BLANK_CHOICE_DASH,
        limit_to_currently_related=False,
        **kwargs
    ):
        """
        Returns choices with a default blank choices included, for use as
        SelectField choices for this field.

        Analog of django.db.models.fields.Field.get_choices(), provided
        initially for utilization by RelatedFieldListFilter.
        """
        related_manager = kwargs.pop(
            "related_manager", self.related_manager or "_default_manager"
        )
        related_order = kwargs.pop("related_order", self.get_related_order() or [])

        first_choice = blank_choice if include_blank else []
        queryset = getattr(field.related_model, related_manager).all()
        if limit_to_currently_related:
            queryset = queryset.complex_filter(
                {"%s__isnull" % self.get_related_model_field_name(field): False}
            )
        if related_order:
            queryset = queryset.order_by(*related_order)
        queryset = queryset.distinct()
        lst = [(x._get_pk_val(), smart_str(x)) for x in queryset]
        return first_choice + lst

    def field_choices(self, field, request, model_admin):
        return self.get_related_field_choices(field, include_blank=False)
