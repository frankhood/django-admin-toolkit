from django.db import models
from django.urls import reverse

from tests.example.managers import DetailInInlineExampleModelManager
from tests.example.querysets import DetailInInlineExampleModelQuerySet


class DetailInInlineExampleModel(models.Model):

    objects = DetailInInlineExampleModelManager.from_queryset(
        DetailInInlineExampleModelQuerySet)()

    test_text = models.TextField("Test Text", blank=True, default="")
    test_fk = models.ForeignKey("self", verbose_name="Text FK", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Detail in inline example model"
        verbose_name_plural = "Detail in inline example models"

    @property
    def admin_change_url(self):
        return reverse("admin:example_detailininlineexamplemodel_change", kwargs={"object_id": self.id})