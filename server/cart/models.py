from django.db import models
from django.cotrib.postgres.fields import JSONField


class Order(models.Model):

    class Meta:
        abstract = True

    public_id = models.IntegerField(
    )

    manager_notes = models.TextField(
    )

    client_notes = models.TextField(
    )

    state = models.CharField(
    )

    source = models.CharField(
    )

    user = models.ForeignKey(
    )

    # JSON FIELDS
    cart = JSONField()
    location = JSONField()
    customer = JSONField()
    delivery = JSONField()
    cpa = JSONField()
    store = JSONField()
    tracking = JSONField()
    payment = JSONField()

    CART_JSONSCHEMA = {
    }

    LOCATION_JSONSCHEMA = {
    }

    CUSTOMER_JSONSCHEMA = {
    }

    DELIVERY_JSONSCHEMA = {
    }

    CPA_JSONSCHEMA = {
    }

    STORE_JSONSCHEMA = {
    }

    STATE_ORDERING = {
    }

    state_2_admitad_status_mapping = {
    }

    state_2_admitad_message_mapping = {
    }

    @property
    def cpa_admitad_price(self):
        pass
    
    @property
    def cpa_admitad_status(self):
        pass

    @property
    def cpa_admitad_comment(self):
        pass

    @classmethod
    def _generate_public_id(cls):
        pass

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__original_state = self.state

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        pass

