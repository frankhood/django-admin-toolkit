from django.contrib.admin import AdminSite
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from tests.example.admin import EmptyValueExampleModelAdmin
from tests.example.models import EmptyValueExampleModel


class MockRequest:
    pass


class EmptyValueMixinAdminUnitTest(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()

    def test_formfield_for_foreignkey(self):
        admin = EmptyValueExampleModelAdmin(EmptyValueExampleModel, self.site)
        self.assertEqual(
            admin.formfield_for_foreignkey(EmptyValueExampleModel._meta.get_field("test_fk"), self.request).empty_label,
            _("NO TEST FK")
        )
