from django.test import TestCase
from django.contrib.gis.geos import Point

from .factories import StopProxyFactory, FeedFactory
from ..models import StopProxy


class TestStopQuerySet(TestCase):
    def setUp(self):
        self.feed = FeedFactory()
        self.in_feed_stop = StopProxyFactory.create(
            point=Point(-182, 50),
            feed=self.feed,
        )

        self.out_of_feed_stop = StopProxyFactory.create(
            point=Point(-182, 123)
        )

    def test_belonging_to_feed_includes_only_one(self):
        self.assertEqual(
            StopProxy.objects.belonging_to_feed(self.feed).count(),
            1,
        )

    def test_belonging_to_feed_include(self):

        self.assertEqual(
            StopProxy.objects.belonging_to_feed(self.feed)[0],
            self.in_feed_stop,
        )

    def test_belonging_to_feed_exclude(self):
        self.assertNotEqual(
            StopProxy.objects.belonging_to_feed(self.feed)[0],
            self.out_of_feed_stop,
        )

    def test_active(self):
        self.assertEqual(
            StopProxy.objects.active().count(),
            2,
        )
