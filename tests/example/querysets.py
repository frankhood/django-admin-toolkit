from django.db import models


class ExampleModelForBaseAdminMixinQuerySet(models.QuerySet):
    ...


class ExampleFkModelForBaseAdminMixinQuerySet(models.QuerySet):
    ...


class ExampleM2MModelForBaseAdminMixinQuerySet(models.QuerySet):
    ...


class ExampleGenericRelationModelForBaseAdminMixinQuerySet(models.QuerySet):
    ...


class ExampleModelForAfterSaveAdminMixinQuerySet(models.QuerySet):
    ...