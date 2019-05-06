import ipaddress
from django.conf import settings


from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import GeoIpSerializer
from geo_ip.models import GeoIp


class GeoIpAPIView(APIView):

    def get(self, request):
        client_ip = self.get_client_ip(request)
        client_ip = int(ipaddress.IPv4Address(client_ip))
        try:
            geo_ip = GeoIp.objects.get(ip_left__lte=client_ip,
                                       ip_right__gte=client_ip)
            serializer = GeoIpSerializer(geo_ip)
            return Response(serializer.data)
        except GeoIp.DoesNotExist:
            return Response({'kladr_code': '7700000000000',
                             'kladr_name': 'Москва'})

    def get_client_ip(self, request):
        """
        Предпологается что nginx передаёт в заголовке запись
        uwsgi серверу, тот в свою очередь передаёт её django
        """
        return request.META.get('REMOTE_ADDR')
