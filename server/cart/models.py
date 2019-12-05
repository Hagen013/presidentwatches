import uuid
import datetime
from random import randint, choice

from jsonschema import validate as jsonschema_validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

from djchoices import DjangoChoices, ChoiceItem

from core.db.mixins import TimeStampedMixin
from core.db.fields import PositiveSmallIntegerRangeField
from core.models import SingletonMixin

from shop.models import Attribute
from shop.models import AttributeValue as Value


User = get_user_model()


def _empty_customer():
    return {
        "name": "",
        "email": "",
        "phone": "",
        "address": ""
    }

def _empty_sale():
    return {
        'promocode': '',
        'amount': 0
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

    _order = models.IntegerField(
        default=10,
        verbose_name='порядок'
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

    sale = JSONField(
        blank=True,
        default=_empty_sale
    )

    total_price = models.PositiveIntegerField(
        default=0
    )

    created_by_staff = models.BooleanField(
        default=False
    )

    CART_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "total_price": {"type": "integer", "minimum": 0},
            "total_sale": {"type": "integer", "minimum": 0},
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
                            "base_price": {"type": "integer", "minimum": 0},
                            "image": {"type": "string"},
                            "added_at": {"type": "string", "format": "date-time"},
                            "brand": {"type": "string"},
                            "series": {"type": "string"},
                            "slug": {"type": "string"},
                            "url": {"type": "string"},
                            "sale": {"type": "integer"},
                            "is_sale": {"type": "boolean"}
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
                },
                "required": ["code", "name"],
                "additionalProperties": False
            }
        },
        "required": ["city",],
        "additionalProperties": False
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
            },
        },
        "required": ["name", "email", "phone", "address"],
        "additionalProperties": False
    }

    DELIVERY_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "pattern": "^(not_selected|curier|pvz|rupost|pickup)$"
            },
            "pvz_code": {
                "type": ["string", "null"]
            },
            "pvz_service": {
                "type": ["string", "null"],
            },
            "pvz_address": {
                "type": ["string", "null"],
            },
            "price": {
                "type": ["integer",],
                "minimum": 0
            },
        },
        "required": [
            "type",
            "pvz_code",
            "pvz_service",
            "pvz_address",
            "price"
        ],
        "additionalProperties": False
    }

    PAYMENT_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "pattern": "^(not_selected|cash|card_offline|card_online)$"
            },
        },
        "required": ["type",],
        "additionalProperties": False
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

    SALE_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "promocode": {
                "type": "string"
            },
            "amount": {
                "type": "integer",
                "minimum": 0
            }
        }
    }

    STATE_ORDERING = {
        '1': 0, # новый
        '2': 1, # недозвон
        '3': 2, # недозвон 2
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

            name = "{brand} {series} {model}".format(
                brand=item['brand'],
                series=item['series'],
                model=item['model']
            )

            items.append({
                "id": item['pk'],
                "qnt": item['quantity'],
                "price": item['price'],
                "brand": item['brand'],
                "model": item['model'],
                "name": name
            })

        return items

    @classmethod
    def _generate_public_id(cls):
        return randint(10000000, 99999999)

    @classmethod
    def _generate_uuid(cls):
        return uuid.uuid4().hex

    def _get_order(self):
        default_order = self._meta.get_field('_order').default
        return self.STATE_ORDERING.get(str(self.state), default_order)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__original_state = self.state

    def clean(self):
        try:
            
            jsonschema_validate(self.cart, self.CART_JSONSCHEMA)
            jsonschema_validate(self.location, self.LOCATION_JSONSCHEMA)
            jsonschema_validate(self.customer, self.CUSTOMER_JSONSCHEMA)
            jsonschema_validate(self.delivery, self.DELIVERY_JSONSCHEMA)
            jsonschema_validate(self.payment, self.PAYMENT_JSONSCHEMA)
            jsonschema_validate(self.sale, self.SALE_JSONSCHEMA)

        except JsonSchemaValidationError as e:
            raise ValidationError(message=e.message)

    def save(self, *args, **kwargs):

        self._order = self._get_order()
        super(Order, self).save(*args, **kwargs)


class User2PromocodeRelation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    promocode = models.ForeignKey(
        'Promocode',
        on_delete=models.CASCADE,
    )

class PromocodeType(DjangoChoices):

    BrandsPromo  = ChoiceItem(1, 'По брендам')
    SeriesPromo  = ChoiceItem(2, 'По коллекциям')
    PrivatePromo = ChoiceItem(3, 'Приватный')
    Custom       = ChoiceItem(4, 'Вручную')
    Gift         = ChoiceItem(5, 'Вам подарок')


class Promocode(TimeStampedMixin):

    MAX_SALE_AMOUNT = 90

    class Meta:
        abstract = False

    name = models.CharField(
        max_length=64,
        unique=True,
        db_index=True
    )

    description = models.CharField(
        max_length=512,
        blank=True
    )

    datatype = models.PositiveSmallIntegerField(
        choices=PromocodeType.choices,
        default=PromocodeType.BrandsPromo
    )

    start_date = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True
    )

    expiration_date = models.DateTimeField(
        blank=True,
        null=True
    )

    is_permament = models.BooleanField(
        default=False
    )

    brands = JSONField(
        default=list
    )

    series = JSONField(
        default=list
    )

    users = models.ManyToManyField(
        User,
        blank=True,
        related_name='promocodes',
        through=User2PromocodeRelation
    )

    has_limited_use = models.BooleanField(
        default=False
    )

    applied = models.BooleanField(
        default=False
    )

    limit = models.PositiveSmallIntegerField(
        default=1
    )

    sale_amount = PositiveSmallIntegerRangeField(
        default=0,
        min_value=0,
        max_value=100
    )

    sales = JSONField(
        default=dict,
        blank=True
    )

    def clean(self, *args, **kwargs):
        
        # Проверка

        # Проверка дат начала и старта:
        if not self.is_permament:
            if self.start_date >= self.expiration_date:
                raise ValidationError('Время старта действия промокода позже времени окончания')

        # Проверка брендов
        if self.datatype == PromocodeType.BrandsPromo:

            if len(self.brands) == 0:
                raise ValidationError('Промокоды по бренду должны содержать как минимум 1 бренд')

            qs = Value.objects.filter(attribute__name='Бренд').values('value_enum')
            possible_brands = {v['value_enum'] for v in qs}
            difference = set(self.brands).difference(possible_brands)
            if len(difference) > 0:
                raise ValidationError('Поле брендов содержит значения, отсутствующие в базе данных')
        

        # Или коллекций
        elif self.datatype == PromocodeType.SeriesPromo:
            if len(self.series) == 0:
                raise ValidationError('Промокоды по коллекции должны содержать как минимум 1 коллекцию')

            qs = Value.objects.filter(attribute__name='Коллекция').values('value_enum')
            possible_series = {v['value_enum'] for v in qs}
            difference = set(self.series).difference(possible_series)
            if len(difference) > 0:
                raise ValidationError('Поле коллекций содержит значения, отсутствующие в базе данных')

        # Или пользователей
        elif self.datatype == PromocodeType.PrivatePromo:
            pass

        # Или всего на свете
        else:
            pass

        super(Promocode, self).clean(*args, **kwargs)

    def apply(self, data, user):
        # Функция преобразования данных корзины
        # в соответствии с условиями промокода

        items = data['items'].copy()
        data['total_sale'] = 0
        data['promocode'] = self.name

        total_overall = 0
        total_sale = 0

        if self.datatype == PromocodeType.Gift:
            brands = set(self.sales.keys())
        else:
            brands = set(self.brands)

        items = data['items'].copy()
        data['total_sale'] = 0
        data['promocode'] = self.name

        for key in list(items.keys()):
            item = items[key]

            if item['is_sale'] == False and item['brand'] in brands:
                    
                total_price = item['price'] * item['quantity']
                if self.datatype == PromocodeType.Gift:
                    sale = int(total_price * self.sales[item['brand']])
                else:
                    sale = int(self.sale_amount*total_price/100)
                total_sale += sale

                item['total_price'] = total_price - sale
                item['sale'] = sale
                total_overall += item['total_price']
                    
            else:
                    
                total_price = item['price'] * item['quantity']
                item['total_price'] = total_price
                item['sale'] = 0
                total_overall += total_price

        data['items'] = items
        data['total_price'] = total_overall
        data['total_sale'] = total_sale
        data['sale_amount'] = self.sale_amount

        return data

        
class GiftSalesTable(SingletonMixin):

    sales = JSONField(
        default=dict,
        blank=True,
    )

    def clean(self):
        for key, value in self.sales.items():
            if type(key) != str or type(value) != float:
                raise ValidationError('Недопустимые значения в поле sales')
        super(GiftSalesTable, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        qs = Promocode.objects.filter(datatype=PromocodeType.Gift)
        qs.update(sales=self.sales)
        super(GiftSalesTable, self).save(*args, **kwargs)
