import factory.django

from tests.example.models import DetailInInlineExampleModel


class DetailInInlineExampleModelFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = DetailInInlineExampleModel
