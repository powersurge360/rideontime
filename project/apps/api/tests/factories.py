import factory
from multigtfs.models import Feed

from ..models import StopProxy

class FeedFactory(factory.DjangoModelFactory):
    class Meta:
        model = Feed


class StopProxyFactory(factory.DjangoModelFactory):
    class Meta:
        model = StopProxy

    feed = factory.SubFactory(FeedFactory)
