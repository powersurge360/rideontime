from django.db import models
from django.contrib.gis.db.models.query import GeoQuerySet

from multigtfs.models import Stop


class StopProxyQuerySet(GeoQuerySet):
    def belonging_to_feed(self, feed):
        return self.filter(
            feed=feed
        )

    def active(self):
        return self.all()


class StopProxy(Stop):
    class Meta:
        proxy = True

    objects = StopProxyQuerySet.as_manager()
