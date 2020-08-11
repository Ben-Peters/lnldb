from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory import DjangoModelFactory, Faker, Sequence, SubFactory

from events.models import (Building, CCReport, Event, Event2019, Fund, Location, Category, Organization,
                           EventCCInstance, Service)

__author__ = 'jmerdich'


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)
    username = Sequence(lambda n: 'testuser%d' % n)
    email = Faker('email')
    is_superuser = True
    password = '12345'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        kwargs['password'] = make_password(kwargs['password'])
        return manager.create(*args, **kwargs)


class BuildingFactory(DjangoModelFactory):
    class Meta:
        model = Building


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location
    building = SubFactory(BuildingFactory)


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event
    submitted_ip = '127.0.0.1'
    datetime_setup_complete = timezone.now()
    datetime_start = timezone.now() + timedelta(hours=1)
    datetime_end = timezone.now() + timedelta(hours=3)
    event_name = Faker('company')
    location = SubFactory(LocationFactory)
    submitted_by = SubFactory(UserFactory)


class Event2019Factory(DjangoModelFactory):
    class Meta:
        model = Event2019
    datetime_setup_complete = timezone.now()
    datetime_start = timezone.now() + timedelta(hours=1)
    datetime_end = timezone.now() + timedelta(hours=3)
    event_name = Faker('company')
    location = SubFactory(LocationFactory)
    submitted_by = SubFactory(UserFactory)
    submitted_ip = '127.0.0.1'


class CCInstanceFactory(DjangoModelFactory):
    class Meta:
        model = EventCCInstance

    event = SubFactory(Event2019Factory)
    category = Category.objects.create(name="Event Services")
    service = Service.objects.create(shortname="L1", longname="Lighting", base_cost=100000.00, addtl_cost=1.00,
                                     category=category)
    setup_location = SubFactory(LocationFactory)


class CCReportFactory(DjangoModelFactory):
    class Meta:
        model = CCReport

    event = SubFactory(Event)
    crew_chief = SubFactory(UserFactory)


class OrgFactory(DjangoModelFactory):
    class Meta:
        model = Organization
    user_in_charge = SubFactory(UserFactory)
    name = Faker('company')


class FundFactory(DjangoModelFactory):
    class Meta:
        model = Fund
    organization = Sequence(lambda n: n)
    fund = Sequence(lambda n: n)
    account = Sequence(lambda n: n)
    name = Faker('company')
    notes = Faker('text')
