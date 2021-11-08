from django.db import models


class BaseExampleModelQuerySet(models.QuerySet):
    ...


class BaseExampleFkModelQuerySet(models.QuerySet):
    ...


class BaseExampleM2MModelQuerySet(models.QuerySet):
    ...


class BaseExampleGenericRelationModelQuerySet(models.QuerySet):
    ...


class AfterSaveExampleModelQuerySet(models.QuerySet):
    ...


class AllReadonlyExampleModelQuerySet(models.QuerySet):
    ...


class ConfigurableWidgetsExampleModelQuerySet(models.QuerySet):
    ...


class ConfigurableWidgetsExampleFKModelQuerySet(models.QuerySet):
    ...


class ConfigurableWidgetsExampleM2MModelQuerySet(models.QuerySet):
    ...


class DetailInInlineExampleModelQuerySet(models.QuerySet):
    ...


class EmptyValueExampleModelQuerySet(models.QuerySet):
    ...


class ExtraButtonExampleModelQuerySet(models.QuerySet):
    ...


class FloatingExampleModelQuerySet(models.QuerySet):
    ...


class ImprovedRawIdFieldsExampleModelQuerySet(models.QuerySet):
    ...


class ImprovedRawIdFieldsExampleRelatedModelQuerySet(models.QuerySet):
    ...
