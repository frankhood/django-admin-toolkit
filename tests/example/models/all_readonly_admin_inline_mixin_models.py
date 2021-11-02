from django.db import models


class ExampleModelAllReadonlyAdminInlineMixin(models.Model):
    test_text = models.TextField("Test Text", blank=True)

    class Meta:
        verbose_name = "Example"