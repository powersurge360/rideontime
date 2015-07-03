from datetime import datetime

from django.contrib.gis.db.models.query import GeoQuerySet

from multigtfs.models import Stop, Service, StopTime, Trip, Route
from multigtfs.models.fields.seconds import Seconds


class StopProxyQuerySet(GeoQuerySet):
    def belonging_to_feed(self, feed):
        return self.filter(
            feed=feed
        )

    def active(self):
        '''Grabs all currently active stops.
        '''
        active_services = ServiceProxy.objects.active()

        active_stop_ids = (active_services
                           .prefetch_related('trip__stoptime__stop')
                           .distinct('trip__stoptime__stop__id')
                           .values_list('trip__stoptime__stop__id', flat=True))

        return self.filter(id__in=active_stop_ids)


class ServiceProxyQuerySet(GeoQuerySet):
    def active(self):
        '''Grabs all currently active services, taking into account the day
        of the week and service start/end dates.
        '''

        today = datetime.today()

        active_services = (self.filter(start_date__lte=today)
                               .filter(end_date__gte=today))

        today_num = today.weekday()

        if today_num == 0:
            active_services = active_services.for_day('monday')
        elif today_num == 1:
            active_services = active_services.for_day('tuesday')
        elif today_num == 2:
            active_services = active_services.for_day('wednesday')
        elif today_num == 3:
            active_services = active_services.for_day('thursday')
        elif today_num == 4:
            active_services = active_services.for_day('friday')
        elif today_num == 5:
            active_services = active_services.for_day('saturday')
        elif today_num == 6:
            active_services = active_services.for_day('sunday')

        return active_services

    def for_day(self, day):
        '''Grabs all services that are active for a given day of the week'''
        day_kwargs = {}
        day_kwargs[day] = True

        return self.filter(**day_kwargs)


class StopTimeProxyQuerySet(GeoQuerySet):
    def future(self):
        '''Grab all stop times that occur in the future'''
        now = datetime.now()

        midnight = now.replace(hour=0, minute=0, second=0)
        seconds = (now - midnight).seconds

        return (self
                .order_by('arrival_time')
                .filter(arrival_time__gte=Seconds(seconds)))


class StopProxy(Stop):
    class Meta:
        proxy = True

    objects = StopProxyQuerySet.as_manager()


class ServiceProxy(Service):
    class Meta:
        proxy = True

    objects = ServiceProxyQuerySet.as_manager()


class StopTimeProxy(StopTime):
    class Meta:
        proxy = True

    objects = StopTimeProxyQuerySet.as_manager()


class TripProxy(Trip):
    class Meta:
        proxy = True


class RouteProxy(Route):
    class Meta:
        proxy = True
