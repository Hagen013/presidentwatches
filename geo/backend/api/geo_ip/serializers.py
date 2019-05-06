from rest_framework import serializers

from geo_ip.models import GeoIp


class GeoIpSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoIp
        fields = ('kladr_code',
                  'kladr_name',
                  )
