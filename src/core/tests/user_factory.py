import factory
from factory.django import DjangoModelFactory
from authentication.models import User


class UserFactory(DjangoModelFactory):
    email = factory.LazyAttribute(lambda a: f"{a.first_name}_{a.last_name}@example.com".lower())
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User
