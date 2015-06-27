from rest_framework.generics import ListAPIView
from rest_framework_gis.filters import DistanceToPointFilter

from .models import StopProxy
from .serializers import StopProxySerializer


class StopProxyListAPIView(ListAPIView):
    queryset = StopProxy.objects.active()
    serializer_class = StopProxySerializer
    paginate_by = 100
    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter,)
    distance_filter_convert_meters = True
    bbox_filter_include_overlapping = True
