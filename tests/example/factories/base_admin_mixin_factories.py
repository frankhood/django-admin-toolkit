import factory

from tests.example.models import BaseExampleModel, BaseExampleM2MModel, \
    BaseExampleFkModel, BaseExampleGenericRelationModel


class BaseExampleFkModelFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = BaseExampleFkModel


class BaseExampleM2MModelFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = BaseExampleM2MModel


class BaseExampleGenericRelationModelFactory(factory.django.DjangoModelFactory):
    test_text = factory.Faker("word")

    class Meta:
        model = BaseExampleGenericRelationModel


class BaseExampleModelFactory(factory.django.DjangoModelFactory):
    test_boolean = factory.Faker("pybool")
    test_datetime = factory.Faker("date_time")
    test_fk = factory.SubFactory(BaseExampleFkModelFactory)

    class Meta:
        model = BaseExampleModel

    @factory.post_generation
    def test_m2m(self, create, m2m_entries, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if m2m_entries:
            for _m2m_entry in m2m_entries:
                self.test_m2m.add(_m2m_entry)