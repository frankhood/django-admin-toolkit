import factory.django

from tests.example.models import AllReadonlyExampleModel


class AllReadonlyExampleModelFactory(factory.django.DjangoModelFactory):

    test_text = factory.Faker("word")

    class Meta:
        model = AllReadonlyExampleModel
