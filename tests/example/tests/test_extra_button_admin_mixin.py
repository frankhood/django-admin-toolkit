from django.contrib.admin import AdminSite
from django.test import TestCase

from tests.example.admin import ExtraButtonExampleModelAdmin
from tests.example.models import ExtraButtonExampleModel


class MockRequest:
    pass


class ExtraButtonAdminMixinUnitTest(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()

    def test_get_extra_button(self):
        admin = ExtraButtonExampleModelAdmin(ExtraButtonExampleModel, self.site)
        self.assertEqual(
            admin.get_extra_button(self.request),
            [
                {
                    "label": "Example Extra Button",
                    "url": "http://example.com",
                    "class": "",
                }
            ],
        )
