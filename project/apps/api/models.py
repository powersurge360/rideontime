from django.db import models

from multigtfs.models import Stop


class StopQuerySet(models.QuerySet):
    def belonging_to_feed(self, feed):
        return self.filter(
            feed=feed
        )


class RideOnTimeStop(Stop):
    class Meta:
        proxy = True

    objects = StopQuerySet.as_manager()
