from rest_framework_gis.serializers import GeoModelSerializer

from .models import StopProxy


class StopProxySerializer(GeoModelSerializer):
    class Meta:
        model = StopProxy
