import freezegun
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone

from tests.example import factories as app_factories
from tests.example import models
from tests.example.admin import BaseExampleFkModelAdmin, BaseExampleModelAdmin


class MockRequest:
    pass


class BaseAdminMixinUnitTest(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()

    def test__display_image(self):
        example = app_factories.BaseExampleModelFactory(
            test_image="tests/test_images/test_image.png"
        )
        admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
        self.assertEqual(
            admin._display_image(example.test_image),
            """<a href='/tests/media/tests/test_images/test_image.png' target='_blank'><img src='/tests/media/tests/test_images/test_image.png' width='80' heigth='80' /></a>""",
        )

    def test__display_datetime(self):
        with freezegun.freeze_time("2020-12-12 00:00:00"):
            example = app_factories.BaseExampleModelFactory(
                test_datetime=timezone.now()
            )
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(
                admin._display_datetime(example.test_datetime), "12/12/2020 midnight"
            )

    def test__display_date(self):
        with freezegun.freeze_time("2020-12-12 00:00:00"):
            example = app_factories.BaseExampleModelFactory(
                test_datetime=timezone.now()
            )
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(admin._display_date(example.test_datetime), "12/12/2020")

    def test__display_time(self):
        with freezegun.freeze_time("2020-12-12 00:00:00"):
            example = app_factories.BaseExampleModelFactory(
                test_datetime=timezone.now()
            )
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(admin._display_time(example.test_datetime), "00:00")

    def test__display_boolean(self):
        with self.subTest("test_boolean True"):
            example = app_factories.BaseExampleModelFactory(test_boolean=True)
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(admin._display_boolean(example.test_boolean), "yes")
        with self.subTest("test_boolean False"):
            example = app_factories.BaseExampleModelFactory(test_boolean=False)
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(admin._display_boolean(example.test_boolean), "no")
        with self.subTest("test_boolean None"):
            example = app_factories.BaseExampleModelFactory(test_boolean=None)
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(admin._display_boolean(example.test_boolean), "maybe")

    def test__display_fk_object(self):
        example = app_factories.BaseExampleModelFactory()
        admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
        self.assertEqual(
            admin._display_fk_object(example.test_fk),
            f"""<a href="/admin/example/baseexamplefkmodel/1/change/" target="_blank">{example.test_fk.test_text}</a>""",
        )

    def test__display_m2m_objects(self):
        m2m_object_1 = app_factories.BaseExampleM2MModelFactory()
        m2m_object_2 = app_factories.BaseExampleM2MModelFactory()
        m2m_object_3 = app_factories.BaseExampleM2MModelFactory()
        example = app_factories.BaseExampleModelFactory(
            test_m2m=[m2m_object_1, m2m_object_2, m2m_object_3]
        )
        example.save()
        admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
        self.assertEqual(
            admin._display_m2m_objects(example, "test_m2m"),
            """<a href="/admin/example/baseexamplem2mmodel/?example_for_base_admin_mixins__id__exact=1" target="_blank">Display 3 elements</a>""",
        )

    def test__display_related_objects(self):
        with self.subTest("M2M"):
            m2m_object_1 = app_factories.BaseExampleM2MModelFactory()
            m2m_object_2 = app_factories.BaseExampleM2MModelFactory()
            m2m_object_3 = app_factories.BaseExampleM2MModelFactory()
            example = app_factories.BaseExampleModelFactory(
                test_m2m=[m2m_object_1, m2m_object_2, m2m_object_3]
            )
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(
                admin._display_related_objects(example, "test_m2m"),
                """<a href="/admin/example/baseexamplem2mmodel/?example_for_base_admin_mixins__id__exact=1" target="_blank">Display 3 elements</a>""",
            )
        with self.subTest("M2M show_generic_link=False"):
            m2m_object_1 = app_factories.BaseExampleM2MModelFactory()
            example = app_factories.BaseExampleModelFactory(test_m2m=[m2m_object_1])
            admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
            self.assertEqual(
                admin._display_related_objects(
                    example, "test_m2m", show_generic_link=False
                ),
                f"""<a href='/admin/example/baseexamplem2mmodel/{m2m_object_1.id}/change/' target='_blank'>{m2m_object_1.__str__()}</a>""",
            )
        with self.subTest("FK"):
            example = app_factories.BaseExampleFkModelFactory()
            app_factories.BaseExampleModelFactory(test_fk=example)
            admin = BaseExampleFkModelAdmin(models.BaseExampleFkModel, self.site)
            self.assertEqual(
                admin._display_related_objects(
                    example, "example_for_base_admin_mixins"
                ),
                """<a href="/admin/example/baseexamplemodel/?test_fk__id__exact=3" target="_blank">Display 1 elements</a>""",
            )

    def test__display_generic_related_objects(self):
        example_model = app_factories.BaseExampleModelFactory()
        example_model_content_type = ContentType.objects.get(
            app_label="example", model="baseexamplemodel"
        )
        app_factories.BaseExampleGenericRelationModelFactory(
            content_type=example_model_content_type, object_id=example_model.id
        )
        admin = BaseExampleModelAdmin(models.BaseExampleModel, self.site)
        self.assertEqual(
            admin._display_generic_related_objects(
                example_model,
                "example_generic_relation_model_for_base_admin_mixin",
                "Example Generic Relation Model For Base Admin Mixins",
            ),
            """<a href="/admin/example/baseexamplegenericrelationmodel/?content_type__id__exact=20&object_id__id__exact=1" target="_blank">Display 1 Example Generic Relation Model For Base Admin Mixins</a>""",
        )
