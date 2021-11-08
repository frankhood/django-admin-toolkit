import factory

from tests.example.models import AfterSaveExampleModel


class AfterSaveExampleModelFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = AfterSaveExampleModel
