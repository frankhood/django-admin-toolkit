from django.contrib import admin

from admin_toolkit import admin_filters


class SimpleBooleanTestInTestCharFilter(admin_filters.SimpleBooleanListFilter):
    title = "Test word is in Test char?"
    parameter_name = "test_char"

    def get_true_queryset_values(self, queryset):
        return queryset.filter(test_char__icontains="test")

    def get_false_queryset_values(self, queryset):
        return queryset.exclude(test_char__icontains="test")
