from rest_framework import serializers

from kladr.models import Kladr


class KladrSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kladr
        fields = ('code', 'name', 'kladr_type', 'full_name')


class KladrDetalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kladr
        fields = ('code', 'name', 'kladr_type', 'full_name')

    @classmethod
    def kladr_children(cls, instance):
        children = [{'code': x.code,
                     'name': x.name,
                     'kladr_type': x.kladr_type,
                     'full_name': x.full_name} for x in
                    instance.get_children().filter(code_relevance=0)
                    ]
        if children:
            return children
        else:
            return None

    def to_representation(self, instance):
        ret = super(KladrDetalSerializer, self).to_representation(instance)
        ret['kladr_children'] = self.kladr_children(instance)
        return ret
