from django.db import models


class BaseExampleModelManager(models.Manager):
    ...


class BaseExampleFkModelManager(models.Manager):
    ...


class BaseExampleM2MModelManager(models.Manager):
    ...


class BaseExampleGenericRelationModelManager(models.Manager):
    ...


class AfterSaveExampleModelManager(models.Manager):
    ...


class AllReadonlyExampleModelManager(models.Manager):
    ...


class ConfigurableWidgetsExampleModelManager(models.Manager):
    ...


class ConfigurableWidgetsExampleFKModelManager(models.Manager):
    ...


class ConfigurableWidgetsExampleM2MModelManager(models.Manager):
    ...


class DetailInInlineExampleModelManager(models.Manager):
    ...


class EmptyValueExampleModelManager(models.Manager):
    ...


class ExtraButtonExampleModelManager(models.Manager):
    ...


class FloatingExampleModelManager(models.Manager):
    ...


class ImprovedRawIdFieldsExampleModelManager(models.Manager):
    ...


class ImprovedRawIdFieldsExampleRelatedModelManager(models.Manager):
    ...
