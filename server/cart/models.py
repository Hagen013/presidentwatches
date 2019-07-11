import uuid
import datetime
from random import randint

from jsonschema import validate as jsonschema_validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

from djchoices import DjangoChoices, ChoiceItem

from core.db.mixins import TimeStampedMixin


User = get_user_model()


def _empty_customer():
    return {
        "name": "",
        "email": "",
        "phone": "",
        "address": ""
    }


class OrderState(DjangoChoices):

    New         = ChoiceItem(1, 'Новый')
    UnderCall   = ChoiceItem(2, 'Недозвон')
    UnderCall_2 = ChoiceItem(3, 'Недозвон_2')
    Delivery    = ChoiceItem(4, 'Доставка')
    Agreed      = ChoiceItem(5, 'Согласован')
    Fulfilled   = ChoiceItem(6, 'Выполнен')
    Cancelled   = ChoiceItem(7, 'Отменён')
    Cancelled_2 = ChoiceItem(8, 'Отменён: недозвон')
    HandedOver  = ChoiceItem(9, 'Вручен')
    Rejected    = ChoiceItem(10, 'Отказ')


class OrderSource(DjangoChoices):

    Unknown = ChoiceItem(1, 'Неизвестно')
    Cart    = ChoiceItem(2, 'Корзина')
    FastBuy = ChoiceItem(3, 'Быстрая покупка')
    Catalog = ChoiceItem(4, 'Страница категории')


class Order(TimeStampedMixin):

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

    state = models.IntegerField(
        choices=OrderState.choices,
        default=OrderState.New
    )

    source = models.IntegerField(
        choices=OrderSource.choices,
        default=OrderSource.Unknown
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
        "type": "object",
        "properties": {
            "total_price": {"type": "integer", "minimum": 0},
            "items": {
                "type": "object",
                "patternProperties": {
                    "[\d]+$": {
                        "type": "object",
                        "properties": {
                            "pk": {"type": "integer"},
                            "model": {"type": "string"},
                            "price": {"type": "integer", "minimum": 0},
                            "quantity": {"type": "integer", "minimum": 0},
                            "total_price": {"type": "integer", "minimum": 0},
                            "image": {"type": "string"},
                            "added_at": {"type": "string", "format": "date-time"},
                            "brand": {"type": "string"},
                            "series": {"type": "string"},
                            "slug": {"type": "string"},
                            "url": {"type": "string"}
                        },
                        "required": ["model", "price", "quantity", "total_price", "image", "slug"],
                        "additionalProperties": False,
                    },
                }
            }
        }
    }

    LOCATION_JSONSCHEMA = {
        "type": "object",
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
            },
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

    PAYMENT_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "is_selected": {"type": "boolean"},
            "type": {
                "type": "string",
                "pattern": "^(cash|card_on_receipt|card)$"
            }
        }
    }

    TRACKING_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "service": {"type": "string"},
            "change_date": {"type": "string"},
            "dispatch_number": {"type": "string"},
            "state_description": {"type": "string"},
            "service_status_code": {"type": ["string", "null"]},
            "status_code": {"type": ["string", "null"]},
            "sum": {"type": ["integer", "null"]},
            "history": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "change_date": {
                            "type": "string",
                            "format": "date-tme",
                        },
                        "state_description": {"type": "string"},
                        "service_status_code": {"type": "integer"},
                        "city_code": {"type": ["string", "null"]}
                    }
                }
            },
            "reason": {
                "type": ["object", "null"],
                "properties": {
                    "code": {"type": ["string", "null"]}
                }
            },
            "delay_reason": {
                "type": ["object", 'null'],
                "properties": {
                    "code": {"type": ["string", "null"]}
                }
            }
        }
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
        "новый": 0,
        "недозвон": 1,
        "недозвон": 2
    }

    state_2_admitad_status_mapping = {
        "вручен": 1,
        "отменен": 2,
        "отменен: недозвон": 2,
        "недозвон": 2,
        "отказ": 2
    }

    state_2_admitad_message_mapping = {
        "отменён": "Отменен клиентом",
        "отменён: недозвон": "Отменен по причине недозвона",
        "недозвон": "Не удалось дозвониться",
        "отказ": "Отказ при получении"
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
        try:
            
            jsonschema_validate(self.cart, self.CART_JSONSCHEMA)
            print('Cart is valid')

            jsonschema_validate(self.location, self.LOCATION_JSONSCHEMA)
            print('Location is valid')

            jsonschema_validate(self.customer, self.CUSTOMER_JSONSCHEMA)
            print('Customer is valid')

            jsonschema_validate(self.delivery, self.DELIVERY_JSONSCHEMA)
            print('Delivery is valid')

            jsonschema_validate(self.payment, self.PAYMENT_JSONSCHEMA)
            print('Payment is valid')

        except JsonSchemaValidationError as e:
            print("JSJOSJSSOJSOSJSOSJS")
            raise ValidationError(message=e.message)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


