import factory
from django.apps import apps

from tests.example.models import ExampleModelForBaseAdminMixin, ExampleM2MModelForBaseAdminMixin, \
    ExampleFkModelForBaseAdminMixin, ExampleGenericRelationModelForBaseAdminMixin


class ExampleFkModelForBaseAdminMixinFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = ExampleFkModelForBaseAdminMixin


class ExampleM2MModelForBaseAdminMixinFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = ExampleM2MModelForBaseAdminMixin


class ExampleGenericRelationModelForBaseAdminMixinFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = ExampleGenericRelationModelForBaseAdminMixin


class ExampleModelForBaseAdminMixinFactory(factory.django.DjangoModelFactory):
    test_boolean = factory.Faker("pybool")
    test_datetime = factory.Faker("date_time")
    test_fk = factory.SubFactory(ExampleFkModelForBaseAdminMixinFactory)

    class Meta:
        model = ExampleModelForBaseAdminMixin

    @factory.post_generation
    def test_m2m(self, create, m2m_entries, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if m2m_entries:
            for _m2m_entry in m2m_entries:
                self.test_m2m.add(_m2m_entry)