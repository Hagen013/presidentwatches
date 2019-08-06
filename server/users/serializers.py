from django.contrib.auth import get_user_model

from core.serializers import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'phone_number',
            'birth_date',
            'sex'
        )


class UserPrivateSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = (

        )