from django.contrib.auth import get_user_model

from core.serializers import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'phone_number',
            'birth_date',
            'sex'
        )
        read_only_fields = (
            'id',
            'email',
            'phone'
        )




class UserPrivateSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = (

        )