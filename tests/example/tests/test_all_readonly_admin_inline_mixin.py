from django.contrib.admin import AdminSite
from django.test import TestCase

from tests.example.admin import AllReadonlyExampleModelAdmin, \
    AllReadonlyExampleModelAdminInline
from tests.example.factories.all_readonly_admin_mixin_factories import AllReadonlyExampleModelFactory
from tests.example.models import AllReadonlyExampleModel


class MockRequest:
    pass


class AllReadonlyExampleModelUnitTest(TestCase):

    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()

    def test_example_model_all_readonly_admin_inline_mixin_admin(self):
        admin = AllReadonlyExampleModelAdmin(AllReadonlyExampleModel, self.site)
        obj = AllReadonlyExampleModelFactory()
        self.assertEqual(
            sorted(admin.get_readonly_fields(self.request, obj)),
            sorted(["id", "test_text", "test_fk"])
        )
        self.assertFalse(admin.has_add_permission(self.request))

    def test_example_model_all_readonlu_admin_inline_mixin_admin_inline(self):
        admin = AllReadonlyExampleModelAdminInline(AllReadonlyExampleModel, self.site)
        parent_obj = AllReadonlyExampleModelFactory()
        obj = AllReadonlyExampleModelFactory(test_fk=parent_obj)
        self.assertEqual(
            sorted(admin.get_readonly_fields(self.request, obj)),
            sorted(["test_text", "test_fk"])
        )
        self.assertFalse(admin.has_add_permission(self.request))
