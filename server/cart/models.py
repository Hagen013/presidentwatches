1import uuid
import datetime
from random import randint

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


def _empty_customer():
    return {
        "name": "",
        "email": "",
        "phone": "",
        "address": ""
    }    


class Order(models.Model):

    class Meta:
        abstract = False

    public_id = models.IntegerField(
        db_index=True
    )

    uuid = models.CharField(
        max_length=128,
        db_index=True
    )

    manager_notes = models.TextField(
        blank=True
    )

    client_notes = models.TextField(
        blank=True
    )

    state = models.CharField(
        blank=True,
        max_length=128
    )

    source = models.CharField(
        blank=True,
        max_length=128
    )

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    # JSON FIELDS
    cart = JSONField()

    location = JSONField(
        blank=True,
        default=dict
    )

    customer = JSONField(
        default=_empty_customer
    )

    delivery = JSONField(
        blank=True,
        default=dict
    )

    cpa = JSONField(
        blank=True,
        default=dict
    )

    store = JSONField(
        blank=True,
        default=dict
    )

    tracking = JSONField(
        blank=True,
        default=dict
    )

    payment = JSONField(
        blank=True,
        default=dict
    )


    CART_JSONSCHEMA = {
    }

    LOCATION_JSONSCHEMA = {
        "type": "objects",
        "properties": {
            "city": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    }
                }
            }
        }
    }

    EMAIL_REGEXP = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    CUSTOMER_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "email": {
                "type": "string",
            }
            "phone": {
                "type": "string"
            },
            "address": {
                "type": "string"
            }
        },
    }

    DELIVERY_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "is_selected": {"type": "boolean"},
            "type": {
                "type": ["string", "null"],
                "pvz_code": {
                    "type": ["string", "null"]
                },
                "pvz_service": {
                    "type": ["string", "null"]
                },
                "price": {
                    "type": ["integer", "null"]
                },
            }
        }
    }

    TRACKING_JSONSCHEMA = {

    }

    CPA_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "networks": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }

    STORE_JSONSCHEMA = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "vendor_code": {"type": "string"},
                "amount": {"type": "integer"},
                "stored": {"type": "boolean"}
            },
            "required": [
                "vendor_code",
                "amount",
                "stored"
            ]
        }
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

    @property
    def rr_email_available(self):
        if self.user is None and len(self.customer['email']) > 0:
            return True
        return False

    @property
    def rr_items(self):

        items = []

        for key in self.cart['items']:
            item = self.cart['items'][key]
            items.append({
                "id": item['pk'],
                "qnt": item['quantity'],
                "price": item['price']
            })

        return items

    @classmethod
    def _generate_public_id(cls):
        date = datetime.datetime.now()
        number = str(randint(1000, 9999))
        year = str(date.year)[2:]
        month = str(date.month)
        day = str(date.day)
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month
        code = "{0}{1}{2}{3}{4}".format(
            year,
            number[:2],
            month,
            day,
            number[2:]
        )
        return int(code)

    @classmethod
    def _generate_uuid(cls):
        return uuid.uuid4().hex

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__original_state = self.state

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

