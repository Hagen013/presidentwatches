from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer
from core.serializers import DynamicFieldsModelSerializer
from .models import UserSubscribe, UserMarketingGroup

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


class UserSubscribeSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = UserSubscribe
        fields = (
            'email',
        )


class UserMarketingGroupSerializer(ModelSerializer):
    
    class Meta:
        model = UserMarketingGroup
        fields = (
            'id',
            'name',
            'sales',
            'automatically_increase',
            'ranking',
            'userscore_threshold'
        )