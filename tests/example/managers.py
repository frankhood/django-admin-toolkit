from django.db import models


class ExampleModelForBaseAdminMixinManager(models.Manager):
    ...


class ExampleFkModelForBaseAdminMixinManager(models.Manager):
    ...


class ExampleM2MModelForBaseAdminMixinManager(models.Manager):
    ...


class ExampleGenericRelationModelForBaseAdminMixinManager(models.Manager):
    ...


class ExampleModelForAfterSaveAdminMixinManager(models.Manager):
    ...