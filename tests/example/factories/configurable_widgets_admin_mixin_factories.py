import factory.django

from tests.example.models import ConfigurableWidgetsExampleModel, \
    ConfigurableWidgetsExampleM2MModel, ConfigurableWidgetsExampleFKModel


class ConfigurableWidgetsExampleM2MModelFactory(factory.django.DjangoModelFactory):

    test_text = factory.Faker("word")

    class Meta:
        model = ConfigurableWidgetsExampleM2MModel


class ConfigurableWidgetsExampleFKModelFACTORY(factory.django.DjangoModelFactory):

    test_text = factory.Faker("word")

    class Meta:
        model = ConfigurableWidgetsExampleFKModel


class ConfigurableWidgetsExampleModelFactory(factory.django.DjangoModelFactory):

    test_text = factory.Faker("word")
    test_fk = factory.SubFactory(ConfigurableWidgetsExampleFKModelFACTORY)

    class Meta:
        model = ConfigurableWidgetsExampleModel

    @factory.post_generation
    def test_m2m(self, create, m2m_entries, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if m2m_entries:
            for _m2m_entry in m2m_entries:
                self.test_m2m.add(_m2m_entry)