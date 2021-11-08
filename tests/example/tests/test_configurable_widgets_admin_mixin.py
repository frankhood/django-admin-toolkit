from django import forms
from django.contrib.admin import AdminSite
from django.test import TestCase

from tests.example.admin import ConfigurableWidgetsExampleModelAdmin
from tests.example.models import ConfigurableWidgetsExampleModel


class MockRequest:
    pass


class ConfigurableWidgetsAdminMixinUnitTest(TestCase):

    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()

    def test_dbfield_overrides(self):
        admin = ConfigurableWidgetsExampleModelAdmin(ConfigurableWidgetsExampleModel, self.site)
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_text'), self.request
            ).help_text,
            "Test Text Example help text"
        )
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_text'), self.request
            ).widget.__class__,
            forms.Textarea
        )
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_fk'), self.request
            ).help_text,
            "Test FK Example help text"
        )
        self.assertNotEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_fk'), self.request
            ).widget.__class__,
            forms.CheckboxInput
        )
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_m2m'), self.request
            ).help_text,
            "Test M2M Example help text"
        )
        self.assertNotEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_m2m'), self.request
            ).widget.__class__,
            forms.CheckboxSelectMultiple
        )

    def test_fkfield_overrides(self):
        admin = ConfigurableWidgetsExampleModelAdmin(ConfigurableWidgetsExampleModel, self.site)
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_text'), self.request
            ).help_text,
            "Test Text Example help text"
        )
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_text'), self.request
            ).widget.__class__,
            forms.Textarea
        )
        self.assertEqual(
            admin.formfield_for_foreignkey(
                ConfigurableWidgetsExampleModel._meta.get_field('test_fk'), self.request
            ).help_text,
            "Test FK Example help text"
        )
        self.assertEqual(
            admin.formfield_for_foreignkey(
                ConfigurableWidgetsExampleModel._meta.get_field('test_fk'), self.request
            ).widget.__class__,
            forms.CheckboxInput
        )
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_m2m'), self.request
            ).help_text,
            "Test M2M Example help text"
        )
        self.assertNotEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_m2m'), self.request
            ).widget.__class__,
            forms.CheckboxSelectMultiple
        )

    def test_m2mfield_overrides(self):
        admin = ConfigurableWidgetsExampleModelAdmin(ConfigurableWidgetsExampleModel, self.site)
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_text'), self.request
            ).help_text,
            "Test Text Example help text"
        )
        self.assertEqual(
            admin.formfield_for_dbfield(
                ConfigurableWidgetsExampleModel._meta.get_field('test_text'), self.request
            ).widget.__class__,
            forms.Textarea
        )
        self.assertEqual(
            admin.formfield_for_foreignkey(
                ConfigurableWidgetsExampleModel._meta.get_field('test_fk'), self.request
            ).help_text,
            "Test FK Example help text"
        )
        self.assertEqual(
            admin.formfield_for_foreignkey(
                ConfigurableWidgetsExampleModel._meta.get_field('test_fk'), self.request
            ).widget.__class__,
            forms.CheckboxInput
        )
        self.assertEqual(
            admin.formfield_for_manytomany(
                ConfigurableWidgetsExampleModel._meta.get_field('test_m2m'), self.request
            ).help_text,
            "Test M2M Example help text"
        )
        self.assertEqual(
            admin.formfield_for_manytomany(
                ConfigurableWidgetsExampleModel._meta.get_field('test_m2m'), self.request
            ).widget.__class__,
            forms.CheckboxSelectMultiple
        )
