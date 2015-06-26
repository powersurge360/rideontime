import factory
from multigtfs.models import Feed

from ..models import RideOnTimeStop

class FeedFactory(factory.DjangoModelFactory):
    class Meta:
        model = Feed


class RideOnTimeStopFactory(factory.DjangoModelFactory):
    class Meta:
        model = RideOnTimeStop

    feed = factory.SubFactory(FeedFactory)
