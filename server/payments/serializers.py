from .models import Payment

from rest_framework import serializers


class CreatePaymentSerializer():
    pass


class PaymentSeializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'id',
            'user',
            'order',
            'y_id',
            'uuid',
            'status',
            'paid',
            'amount',
            'amount_paid',
            'confirmation_url',
            'created_at',
            'description',
            'metadata',
            'refundable'
        )