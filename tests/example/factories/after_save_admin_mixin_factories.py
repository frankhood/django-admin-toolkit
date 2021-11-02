import factory

from tests.example.models import ExampleModelForAfterSaveAdminMixin


class ExampleModelForAfterSaveAdminMixinFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = ExampleModelForAfterSaveAdminMixin
