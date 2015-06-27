from django.conf.urls import url

from .views import StopProxyListAPIView

urlpatterns = [
    url(r'^stops/$', StopProxyListAPIView.as_view(), name='stops_list'),
]
