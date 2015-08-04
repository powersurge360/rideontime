from datetime import datetime, timedelta

from django.test import TestCase

from freezegun import freeze_time

from .factories import (StopProxyFactory, FeedFactory, ServiceProxyFactory,
                        StopTimeProxyFactory, TripProxyFactory)
from ..models import StopProxy, ServiceProxy, StopTimeProxy


class TestStopProxyQuerySet(TestCase):
    def setUp(self):
        # Set up belonging_to_feed tests
        self.feed = FeedFactory()
        self.in_feed_stop = StopProxyFactory.create(
            feed=self.feed,
        )

        self.out_of_feed_stop = StopProxyFactory.create()

        # Set up active tests
        active_service = ServiceProxyFactory(
            start_date=datetime(year=1970, month=1, day=1),
            end_date=datetime(year=1970, month=2, day=1),
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
        )

        inactive_service = ServiceProxyFactory(
            start_date=datetime(year=1971, month=1, day=1),
            end_date=datetime(year=1971, month=2, day=1),
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
        )

        active_trip = TripProxyFactory(
            service=active_service,
        )

        inactive_trip = TripProxyFactory(
            service=inactive_service,
        )

        self.active_stop_time = StopTimeProxyFactory(
            trip=active_trip
        )

        self.inactive_stop_time = StopTimeProxyFactory(
            trip=inactive_trip
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

    @freeze_time('1970-01-20')
    def test_active_includes_active_today(self):
        self.assertEqual(
            StopProxy.objects.active().count(),
            1,
        )

        self.assertEqual(
            StopProxy.objects.active()[0],
            self.active_stop_time.stop,
        )

    @freeze_time('1970-01-20')
    def test_active_excludes_inactive_today(self):
        self.assertEqual(
            StopProxy.objects.active().count(),
            1,
        )

        self.assertNotEqual(
            StopProxy.objects.active()[0],
            self.inactive_stop_time.stop,
        )

    @freeze_time('1970-01-20')
    def test_active_does_one_query(self):
        with self.assertNumQueries(1):
            for item in StopProxy.objects.active():
                pass


class TestServiceProxyQuerySet(TestCase):
    def setUp(self):
        self.good_service = ServiceProxyFactory(
            start_date=datetime(year=1970, month=1, day=1),
            end_date=datetime(year=1970, month=6, day=1),
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
        )

        self.bad_service = ServiceProxyFactory(
            start_date=datetime(year=1971, month=1, day=1),
            end_date=datetime(year=1972, month=1, day=1),
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
        )

    @freeze_time('1970-04-01')
    def test_active_includes_active_today(self):
        self.assertEqual(
            ServiceProxy.objects.active().count(),
            1,
        )

        self.assertEqual(
            ServiceProxy.objects.active()[0],
            self.good_service,
        )

    @freeze_time('1970-04-01')
    def test_active_excludes_active_today(self):
        self.assertEqual(
            ServiceProxy.objects.active().count(),
            1,
        )

        self.assertNotEqual(
            ServiceProxy.objects.active()[0],
            self.bad_service,
        )

    @freeze_time('1970-04-01')
    def test_active_does_one_query(self):
        with self.assertNumQueries(1):
            for item in ServiceProxy.objects.active():
                pass

    def test_active_accounts_for_day(self):
        ServiceProxy.objects.all().delete()

        days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday')

        services = [
            ServiceProxyFactory.create(**{day: True})
            for day in days
        ]

        relevant_date = services[0].start_date

        for i in range(0, 6):
            with freeze_time(relevant_date + timedelta(days=i)):
                self.assertEqual(ServiceProxy.objects.active().count(), 1)

    def test_for_day_grabs_correct_feeds(self):
        ServiceProxy.objects.all().delete()
        days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday')

        services = [
            ServiceProxyFactory.create(**{day: True})
            for day in days
        ]

        self.assertEqual(len(services), 7)

        for day in days:
            self.assertEqual(
                ServiceProxy.objects.for_day(day).count(),
                1,
            )


class TestStopTimeProxyQuerySet(TestCase):
    def setUp(self):
        self.future_stop_times = [
            StopTimeProxyFactory(
                # 1 PM
                arrival_time=46800
            )
            for i in range(10)
        ]

        self.past_stop_times = [
            StopTimeProxyFactory(
                # 1 AM
                arrival_time=3600
            )
            for i in range(10)
        ]

    @freeze_time('12:00pm')
    def test_future_includes_future_stoptimes(self):
        future_stops = StopTimeProxy.objects.future()
        self.assertEqual(
            future_stops.count(),
            10,
        )

        self.assertEqual(
            list(future_stops),
            self.future_stop_times,
        )

    @freeze_time('12:00pm')
    def test_future_excludes_future_stoptimes(self):
        future_stops = StopTimeProxy.objects.future()
        self.assertEqual(
            future_stops.count(),
            10,
        )

        for stop_time in self.past_stop_times:
            self.assertNotIn(stop_time, future_stops)
