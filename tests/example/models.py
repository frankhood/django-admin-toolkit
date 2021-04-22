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

    @property
    def admin_change_url(self):
        from django.urls import reverse
        url_context = {'app_label': self._meta.app_label, 'model_name': self._meta.model_name}
        return reverse('admin:{app_label}_{model_name}_change'.format(**url_context),
                       args=(self.id,))

    @classmethod
    def admin_changelist_url(cls):
        from django.urls import reverse
        url_context = {'app_label': cls._meta.app_label, 'model_name': cls._meta.model_name}
        return reverse('admin:{app_label}_{model_name}_changelist'.format(**url_context))


class BaseAdminExample(models.Model):
    image = models.ImageField(
        'Image',
        blank=True,
        null=True,
        upload_to='images'
    )
    datetime = models.DateTimeField(
        'Datetime',
        blank=True,
        null=True
    )
    date = models.DateField(
        'Date',
        blank=True,
        null=True
    )
    time = models.TimeField(
        'Time',
        blank=True,
        null=True
    )
    boolean = models.BooleanField(
        'Boolean',
        default=False
    )
    after_save_fk_example = models.ForeignKey(
        'example.AfterSaveExample',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    after_save_m2m_example = models.ManyToManyField(
        'example.AfterSaveExample',
        blank=True,
        related_name='base_admin'
    )

    class Meta:
        verbose_name = 'Base Admin Example'
        verbose_name_plural = 'Base Admin Examples'
