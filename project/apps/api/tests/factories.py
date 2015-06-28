from datetime import datetime

from django.contrib.gis.geos import Point

import factory
from multigtfs.models import Feed

from ..models import (StopProxy, StopTimeProxy, TripProxy, ServiceProxy,
                      RouteProxy)


class FeedFactory(factory.DjangoModelFactory):
    class Meta:
        model = Feed


class StopProxyFactory(factory.DjangoModelFactory):
    class Meta:
        model = StopProxy

    feed = factory.SubFactory(FeedFactory)
    point = Point(-182, 50)


class ServiceProxyFactory(factory.DjangoModelFactory):
    class Meta:
        model = ServiceProxy

    feed = factory.SubFactory(FeedFactory)
    service_id = factory.Sequence(lambda n: '{}'.format(n))
    start_date = datetime(year=1970, month=1, day=1)
    end_date = datetime(year=1970, month=6, day=1)
    monday = False
    tuesday = False
    wednesday = False
    thursday = False
    friday = False
    saturday = False
    sunday = False


class RouteProxyFactory(factory.DjangoModelFactory):
    class Meta:
        model = RouteProxy

    rtype = 0
    feed = factory.SubFactory(FeedFactory)


class TripProxyFactory(factory.DjangoModelFactory):
    class Meta:
        model = TripProxy

    service = factory.SubFactory(ServiceProxyFactory)
    route = factory.SubFactory(RouteProxyFactory)


class StopTimeProxyFactory(factory.DjangoModelFactory):
    class Meta:
        model = StopTimeProxy

    trip = factory.SubFactory(TripProxyFactory)
    stop_sequence = factory.Sequence(lambda n: '{}'.format(n))
    stop = factory.SubFactory(StopProxyFactory)
