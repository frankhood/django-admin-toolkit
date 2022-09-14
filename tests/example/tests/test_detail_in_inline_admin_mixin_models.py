from django.contrib.admin import AdminSite
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from tests.example.admin import DetailInInlineExampleModelAdminInline
from tests.example.factories import DetailInInlineExampleModelFactory
from tests.example.models import DetailInInlineExampleModel


class MockRequest:
    pass


class DetailInInlineAdminMixinUnitTest(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()

    def test_get_fields(self):
        admin = DetailInInlineExampleModelAdminInline(
            DetailInInlineExampleModel, self.site
        )
        self.assertEqual(
            sorted(admin.get_fields(self.request)),
            sorted(("display_inline_obj", "test_text")),
        )

    def test_get_readonly_fields(self):
        admin = DetailInInlineExampleModelAdminInline(
            DetailInInlineExampleModel, self.site
        )
        self.assertEqual(
            sorted(admin.get_readonly_fields(self.request)),
            sorted(("display_inline_obj",)),
        )

    def test_display_inline_obj(self):
        admin = DetailInInlineExampleModelAdminInline(
            DetailInInlineExampleModel, self.site
        )
        obj = DetailInInlineExampleModelFactory()
        self.assertEqual(
            admin.display_inline_obj(obj),
            '<a href="{0}" target="_blank" class="admin-button admin-button-success">{1}</a>'.format(
                obj.admin_change_url, _("Detail")
            ),
        )
