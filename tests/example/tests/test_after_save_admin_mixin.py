from unittest.mock import patch

from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from tests.example import models
from tests.example.admin import AfterSaveExampleModelAdmin
from tests.example.factories import (
    AfterSaveExampleModelFactory
)


class MockRequest:
    pass


class AfterSaveAdminMixinUnitTest(TestCase):

    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()

    def test_after_save_on_logging_actions(self):
        admin = AfterSaveExampleModelAdmin(models.AfterSaveExampleModel, self.site)
        self.request.user = User.objects.create(username='admin', is_superuser=True, is_staff=True)
        obj = AfterSaveExampleModelFactory()
        content_type = get_content_type_for_model(obj)
        tests = (
            (admin.log_addition, ADDITION, {'added': {}}),
            (admin.log_change, CHANGE, {'changed': {'fields': ['test_text']}}),
        )
        for method, flag, message in tests:
            with self.subTest(name=method.__name__):
                with patch.object(AfterSaveExampleModelAdmin, "after_save") as after_save_mock_method:
                    created = method(self.request, obj, message)
                    fetched = LogEntry.objects.filter(action_flag=flag).latest('id')
                    self.assertEqual(created, fetched)
                    self.assertEqual(fetched.action_flag, flag)
                    self.assertEqual(fetched.content_type, content_type)
                    self.assertEqual(fetched.object_id, str(obj.pk))
                    self.assertEqual(fetched.user, self.request.user)
                    self.assertEqual(fetched.change_message, str(message))
                    self.assertEqual(fetched.object_repr, str(obj))
                    after_save_mock_method.assert_called_once()
