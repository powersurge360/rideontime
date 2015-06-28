from datetime import datetime

from django.contrib.gis.db.models.query import GeoQuerySet

from multigtfs.models import Stop, Service, StopTime, Trip, Route


class StopProxyQuerySet(GeoQuerySet):
    def belonging_to_feed(self, feed):
        return self.filter(
            feed=feed
        )

    def active(self):
        '''Grabs all currently active stops. Makes a call to
        ServiceProxyQuerySet's active under the hood meaning each use of this
        query will call at least two round trips to the db
        '''
        active_services = ServiceProxy.objects.active()

        active_stop_ids = (active_services
                           .prefetch_related('trip__stoptime__stop')
                           .distinct('trip__stoptime__stop__id')
                           .values('trip__stoptime__stop__id'))

        processed_ids = {
            stop['trip__stoptime__stop__id']
            for stop in active_stop_ids
        }

        return self.filter(id__in=processed_ids)


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
            active_services = active_services.for_day('saturday')

        return active_services

    def for_day(self, day):
        '''Grabs all services that are active for a given day of the week'''
        day_kwargs = {}
        day_kwargs[day] = True

        return self.filter(**day_kwargs)


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


class TripProxy(Trip):
    class Meta:
        proxy = True


class RouteProxy(Route):
    class Meta:
        proxy = True
