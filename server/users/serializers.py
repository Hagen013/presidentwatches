from django.contrib.auth import get_user_model

from core.serializers import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'username',
        )