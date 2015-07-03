from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer

from .models import StopProxy, StopTimeProxyQuerySet


class StopTimeRelatedField(serializers.RelatedField):
    def to_representation(self, stop_times):
        future_stop_times = StopTimeProxyQuerySet.future(stop_times)

        return [
            str(st.arrival_time)
            for st in future_stop_times[:5]
        ]


class StopProxySerializer(GeoModelSerializer):
    stoptime_set = StopTimeRelatedField(read_only=True)

    class Meta:
        model = StopProxy
