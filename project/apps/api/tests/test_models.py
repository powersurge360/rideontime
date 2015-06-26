from django.test import TestCase
from django.contrib.gis.geos import Point

from .factories import RideOnTimeStopFactory, FeedFactory
from ..models import RideOnTimeStop


class TestStopQuerySet(TestCase):
    def setUp(self):
        self.feed = FeedFactory()
        self.in_feed_stop = RideOnTimeStopFactory.create(
            point=Point(-182, 50),
            feed=self.feed,
        )

        self.out_of_feed_stop = RideOnTimeStopFactory.create(
            point=Point(-182, 123)
        )

    def test_belonging_to_feed_includes_only_one(self):
        self.assertEqual(
            RideOnTimeStop.objects.belonging_to_feed(self.feed).count(),
            1,
        )

    def test_belonging_to_feed_include(self):

        self.assertEqual(
            RideOnTimeStop.objects.belonging_to_feed(self.feed)[0],
            self.in_feed_stop,
        )

    def test_belonging_to_feed_exclude(self):
        self.assertNotEqual(
            RideOnTimeStop.objects.belonging_to_feed(self.feed)[0],
            self.out_of_feed_stop,
        )
