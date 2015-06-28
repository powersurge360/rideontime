from rest_framework.generics import ListAPIView
from rest_framework_gis.filters import DistanceToPointFilter

from .models import StopProxy
from .serializers import StopProxySerializer


class StopProxyListAPIView(ListAPIView):
    '''Retrieves all active stops for today and paginates per 100 entries.

    Accepts the following GET arguments:

    * dist: The distance in meters from a given point
    * point: A given point in long, lat format
    '''
    queryset = StopProxy.objects.active()
    serializer_class = StopProxySerializer
    paginate_by = 100
    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter,)
    distance_filter_convert_meters = True
    bbox_filter_include_overlapping = True
