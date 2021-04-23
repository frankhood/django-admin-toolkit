from django.db import models


class AfterSaveExample(models.Model):
    title = models.CharField(
        'Title',
        max_length=64,
    )
    uuid = models.CharField(
        'UUID',
        max_length=64,
        blank=True,
        default=''
    )

    class Meta:
        verbose_name = 'After Save Example'
        verbose_name_plural = 'After Save Examples'
