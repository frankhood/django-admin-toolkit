from unittest.mock import patch

import freezegun
from django.apps import apps
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from tests.example import models
from tests.example.admin import ExampleModelForBaseAdminMixinAdmin, ExampleFkModelForBaseAdminMixinAdmin, \
    ExampleModelForAfterSaveAdminMixinAdmin
from tests.example.factories import (
    ExampleModelForBaseAdminMixinFactory,
    ExampleM2MModelForBaseAdminMixinFactory,
    ExampleFkModelForBaseAdminMixinFactory, ExampleGenericRelationModelForBaseAdminMixinFactory
)


class MockRequest:
    pass


class BaseAdminMixinUnitTest(TestCase):

    def setUp(self) -> None:
        self.site = AdminSite()

    def test__display_image(self):
        example = ExampleModelForBaseAdminMixinFactory(test_image="tests/test_images/test_image.png")
        admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
        self.assertEqual(
            admin._display_image(example.test_image),
            """<a href='/tests/media/tests/test_images/test_image.png' target='_blank'><img src='/tests/media/tests/test_images/test_image.png' width='80' heigth='80' /></a>"""
        )

    def test__display_datetime(self):
        with freezegun.freeze_time("2020-12-12 00:00:00"):
            example = ExampleModelForBaseAdminMixinFactory(test_datetime=timezone.now())
            admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
            self.assertEqual(admin._display_datetime(example.test_datetime), "12/12/2020 midnight")

    def test__display_date(self):
        with freezegun.freeze_time("2020-12-12 00:00:00"):
            example = ExampleModelForBaseAdminMixinFactory(test_datetime=timezone.now())
            admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
            self.assertEqual(admin._display_date(example.test_datetime), "12/12/2020")

    def test__display_time(self):
        with freezegun.freeze_time("2020-12-12 00:00:00"):
            example = ExampleModelForBaseAdminMixinFactory(test_datetime=timezone.now())
            admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
            self.assertEqual(admin._display_time(example.test_datetime), "00:00")

    def test__display_boolean(self):
        with self.subTest("test_boolean True"):
            example = ExampleModelForBaseAdminMixinFactory(test_boolean=True)
            admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
            self.assertEqual(admin._display_boolean(example.test_boolean), "yes")
        with self.subTest("test_boolean False"):
            example = ExampleModelForBaseAdminMixinFactory(test_boolean=False)
            admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
            self.assertEqual(admin._display_boolean(example.test_boolean), "no")
        with self.subTest("test_boolean None"):
            example = ExampleModelForBaseAdminMixinFactory(test_boolean=None)
            admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
            self.assertEqual(admin._display_boolean(example.test_boolean), "maybe")

    def test__display_fk_object(self):
        example = ExampleModelForBaseAdminMixinFactory()
        admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
        self.assertEqual(
            admin._display_fk_object(example.test_fk),
            """<a href="/admin/example/examplefkmodelforbaseadminmixin/1/change/" target="_blank">1</a>"""
        )

    def test__display_m2m_objects(self):
        m2m_object_1 = ExampleM2MModelForBaseAdminMixinFactory()
        m2m_object_2 = ExampleM2MModelForBaseAdminMixinFactory()
        m2m_object_3 = ExampleM2MModelForBaseAdminMixinFactory()
        example = ExampleModelForBaseAdminMixinFactory(test_m2m=[m2m_object_1, m2m_object_2, m2m_object_3])
        example.save()
        admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
        self.assertEqual(
            admin._display_m2m_objects(example, "test_m2m"),
            """<a href="/admin/example/examplem2mmodelforbaseadminmixin/?example_for_base_admin_mixins=1" target="_blank">Display 3 elements</a>"""
        )

    def test__display_related_objects(self):
        with self.subTest("M2M"):
            m2m_object_1 = ExampleM2MModelForBaseAdminMixinFactory()
            m2m_object_2 = ExampleM2MModelForBaseAdminMixinFactory()
            m2m_object_3 = ExampleM2MModelForBaseAdminMixinFactory()
            example = ExampleModelForBaseAdminMixinFactory(test_m2m=[m2m_object_1, m2m_object_2, m2m_object_3])
            admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
            self.assertEqual(
                admin._display_related_objects(example, "test_m2m"),
                """<a href="/admin/example/examplemodelforbaseadminmixin/?ExampleModelForBaseAdminMixin=1" target="_blank">Display 3 elements</a>"""
            )
        with self.subTest("FK"):
            example = ExampleFkModelForBaseAdminMixinFactory()
            ExampleModelForBaseAdminMixinFactory(test_fk=example)
            admin = ExampleFkModelForBaseAdminMixinAdmin(models.ExampleFkModelForBaseAdminMixin, self.site)
            self.assertEqual(
                admin._display_related_objects(example, "example_for_base_admin_mixins"),
                """<a href="/admin/example/examplemodelforbaseadminmixin/?test_fk=2" target="_blank">Display 1 elements</a>"""
            )

    def test__display_generic_related_objects(self):
        example_model = ExampleModelForBaseAdminMixinFactory()
        example_model_content_type = ContentType.objects.get(app_label="example", model="examplemodelforbaseadminmixin")
        ExampleGenericRelationModelForBaseAdminMixinFactory(content_type=example_model_content_type, object_id=example_model.id)
        admin = ExampleModelForBaseAdminMixinAdmin(models.ExampleModelForBaseAdminMixin, self.site)
        self.assertEqual(
            admin._display_generic_related_objects(example_model, "example_generic_relation_model_for_base_admin_mixin", "Example Generic Relation Model For Base Admin Mixins"),
            """<a href="/admin/example/examplegenericrelationmodelforbaseadminmixin/?content_type=9&object_id=1" target="_blank">Display 1 Example Generic Relation Model For Base Admin Mixins</a>"""
        )


class AfterSaveAdminMixinUnitTest(TestCase):

    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()

    def test_after_save(self):
        ...

    def test_log_addition(self):
        with patch.object(ExampleModelForAfterSaveAdminMixinAdmin, "log_addition") as log_addition_mock_method:
            with patch.object(ExampleModelForAfterSaveAdminMixinAdmin, "after_save") as after_save_mock_method:
                admin = ExampleModelForAfterSaveAdminMixinAdmin(models.ExampleModelForAfterSaveAdminMixin, self.site)
                url = reverse_lazy("admin:example_examplemodelforaftersaveadminmixin_add")
                User = apps.get_model(settings.AUTH_USER_MODEL)
                user = User.objects.create(is_superuser=True, is_staff=True)
                self.client.force_login(user)
                response = self.client.post(url, {"test_text": "Test Text"})
                self.assertEqual(response.status_code, 201)
                print("RESPONSE => ", response.__dict__)
                log_addition_mock_method.assert_called_once()
                after_save_mock_method.assert_called_once()

    def test_log_change(self):
        ...
