from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from djchoices import DjangoChoices, ChoiceItem
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from .utils_data import KLADR_TYPE_SOCR_CHOICE

REGION_ADJUST = {
    '77000000000': '50000000000',  # Москва -> Московская область
    '78000000000': '47000000000',  # С-Петербург -> Ленинградская область
    '92000000000': '91000000000',  # Севастополь -> Крым
}

# Кастомные менеджеры для модели кладера
# -----------------------------------------------------------------------------


class KladrActualManager(TreeManager):

    """
    Выдаёт только актуальные объекты
    """

    def get_queryset(self):
        return super(KladrActualManager, self).\
            get_queryset().\
            filter(code_relevance=0)

    def find_object_with_region(self, city, region=None):
        """
        Более устойчивый поиск
        """
        if region:
            # Нормализация региона
            region = region.replace('.', '')
            region = ' '.join((
                r for r in region.split(' ')
                if all(
                    (r not in socr for socr in KLADR_TYPE_SOCR_CHOICE.keys())
                )
            ))

        try:
            # попробовать вернуть объект в лоб
            return Kladr.actual.get(name=city)
        except ObjectDoesNotExist:
            # если его нет, то вернуть регион если он есть,
            # если нет то ничего
            if region:
                return Kladr.actual.get(name=region)
            else:
                return None
        except MultipleObjectsReturned:
            # если объектов много, то попытаться вернуть с совпадением региона
            # если нет или их тоже много то вернуть тот где больше домов
            if region:
                try:
                    return self.actual.\
                        filter(name=city, full_name__icontains=region).\
                        order_by('-houses_num')[0]
                except IndexError:
                    # хз
                    return self.actual.\
                        filter(name=city).\
                        order_by('-houses_num')[0]
            else:
                return self.actual.\
                    filter(name=city).\
                    order_by('-houses_num')[0]


class KladrSubjectManager(KladrActualManager):

    """
    Актуальные субьекты
    """

    def get_queryset(self):
        return super(KladrSubjectManager, self).\
            get_queryset().\
            filter(code_region=0,
                   code_city=0,
                   code_locality=0,
                   code_street=0)


class KladrRegionManager(KladrActualManager):

    """
    Актуальные региона
    """

    def get_queryset(self):
        return super(KladrRegionManager, self).\
            get_queryset().\
            filter(~Q(code_region=0),
                   code_city=0,
                   code_locality=0,
                   code_street=0)


class KladrCityManager(KladrActualManager):

    """
    Актуальные города
    """

    def get_queryset(self):
        return super(KladrCityManager, self).\
            get_queryset().\
            filter(~Q(code_city=0),
                   code_locality=0,
                   code_street=0)


class KladrLocalityManager(KladrActualManager):

    """
    Актуальные населённые пункты/районы
    """

    def get_queryset(self):
        return super(KladrLocalityManager, self).\
            get_queryset().\
            filter(~Q(code_locality=0),
                   code_street=0)


class KladrStreetManager(KladrActualManager):

    """
    Актуальные улицы
    """

    def get_queryset(self):
        return super(KladrStreetManager, self).\
            get_queryset().\
            filter(~Q(code_street=0))


# Модель кладера
# -----------------------------------------------------------------------------

class Kladr(MPTTModel, models.Model):

    """
    Модель КЛАДРа.
    https://www.nalog.ru/rn77/program//5961265/
    Дата обращения (Чт мар 16 12:36:52 MSK 2017)

    Соответствует официальной таблице КЛАДРа.
    Также, добавлен MPTT индекс, для работы с моделью,
    как с иерархической структурой.
    """

    # Кастомные менеджеры
    objects = TreeManager()
    actual = KladrActualManager()
    subjects = KladrSubjectManager()
    regions = KladrRegionManager()
    citys = KladrCityManager()
    localitys = KladrLocalityManager()
    streets = KladrStreetManager()

    # Булевые Свойства
    @property
    def is_subject(self):
        if self.code_subject and not any((self.code_region,
                                          self.code_city,
                                          self.code_locality,
                                          self.code_street)):
            return True
        else:
            return False

    @property
    def is_region(self):
        if self.code_region and not any((self.code_city,
                                         self.code_locality,
                                         self.code_street)):
            return True
        else:
            return False

    @property
    def is_city(self):
        if self.code_city and not any((self.code_locality,
                                       self.code_street)):
            return True
        else:
            return False

    @property
    def is_locality(self):
        if self.code_locality and not self.code_street:
            return True
        else:
            return False

    @property
    def is_street(self):
        if self.code_street:
            return True
        else:
            return False

    # Код Кладера как строка
    code = models.CharField(
        verbose_name='Код КЛАДРа',
        unique=True,
        blank=False,
        db_index=True,
        max_length=17,
        validators=[RegexValidator(
            regex='^(\d{13})|(\d{17})|(\d{19})$',
            message='Kladr Core Error',
            code='nomatch')
        ]
    )
    # Код Субьекта
    code_subject = models.PositiveSmallIntegerField(
        verbose_name="Код Субьекта",
        default=0,
        # editable=False,
    )
    # Код Региона
    code_region = models.PositiveSmallIntegerField(
        verbose_name="Код Региона",
        default=0,
        # editable=False,
    )
    # Код Города
    code_city = models.PositiveSmallIntegerField(
        verbose_name="Код Города",
        default=0,
        # editable=False,
    )
    # Код Района
    code_locality = models.PositiveSmallIntegerField(
        verbose_name="Код Района",
        default=0,
        # editable=False,
    )
    # Код улицы
    code_street = models.PositiveSmallIntegerField(
        verbose_name="Код улицы",
        default=0,
        # editable=False,
    )
    # Код Актуальности
    code_relevance = models.PositiveSmallIntegerField(
        verbose_name="Код Актуальности",
        default=0,
        # editable=False,
    )

    # Коды в виде словаря
    def get_codes(self):
        return {
            'code_subject': self.code_subject,
            'code_region': self.code_region,
            'code_city': self.code_city,
            'code_locality': self.code_locality,
            'code_street': self.code_street,
            'code_relevance': self.code_relevance
        }

    # Родительский Кладр, присваивается методом _find_parent
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='Предок',
        db_index=True
    )

    # Имя кладра
    name = models.CharField(
        verbose_name='Название',
        max_length=1024,
        blank=False,
        db_index=True
    )
    # Полное имя, включая имя предка
    full_name = models.CharField(
        verbose_name='Полное Название',
        max_length=1024 * 6,
        default="",
        db_index=True
    )

    def get_full_name(self):
        return ' » '.join(
            ["{0}, {1}".format(x.name, x.kladr_type)
             for x in reversed(self.get_ancestors(include_self=True))]
        )

    # Сокращение кладра (тип объекта)
    kladr_type_socr = models.CharField(
        verbose_name='Тип объекта(сокращение)',
        max_length=256,
        blank=False,
    )
    # Десериализованное значение kladr_type_socr
    kladr_type = models.CharField(
        verbose_name='Тип объекта(полное имя)',
        max_length=256,
        blank=False,
    )
    # Почтовый индекс
    index = models.PositiveIntegerField(
        verbose_name='Почтовый индекс',
        unique=False,
        default=0,
        blank=True,
    )

    # Количество домов
    houses_num = models.PositiveIntegerField(
        verbose_name='Почтовый индекс',
        default=0,
    )

    # Статус Объекта
    class StatusType(DjangoChoices):
        _0 = ChoiceItem(0, '0 Не центр')
        _1 = ChoiceItem(1, '1 Центр района')
        _2 = ChoiceItem(2, '2 Центр (столица) региона')
        _3 = ChoiceItem(3, '3 Центр района и региона (1+2)')
        _4 = ChoiceItem(4, '4 Центральный район центра региона')

    status = models.PositiveSmallIntegerField(
        verbose_name='Статус объекта',
        default=0,
        blank=True,
        choices=StatusType.choices,
        validators=[StatusType.validator]
    )

    @classmethod
    def _find_parent(cls, codes):
        """
        Метод класса ищет по коду предка, если не находит,
        идё по рекурсии. Принимает в качестве параметра результат
        метода get_codes с обнулённым code_relevance.

        В конечном итоге если не будет субъекта предка,
        будет вызвано исключение
        """
        if codes['code_street']:
            codes['code_street'] = 0
        elif codes['code_locality']:
            codes['code_locality'] = 0
        elif codes['code_city']:
            codes['code_city'] = 0
        elif codes['code_region']:
            codes['code_region'] = 0
        else:
            raise ValueError('Bad Klard Code')

        from django.core.exceptions import ObjectDoesNotExist
        try:
            return Kladr.actual.get(**codes)
        except ObjectDoesNotExist:
            return cls._find_parent(codes)

    def save(self, *args, **kwargs):
        """
        Метод перезаписывает некоторые поля

        ССРРРГГГПППАА - для кладера регион
        ССРРРГГГПППУУУУАА - для кладера улицы
        ССРРРГГГПППУУУУДДДД - для кладера дома
        """
        # self.kladr_type = KLADR_TYPE_SOCR_CHOICE.get(
        #     self.kladr_type_socr,
        #     self.kladr_type_socr
        # )
        # self.full_name = self.get_full_name()

        # if len(self.code) == len("ССРРРГГГПППАА"):
        #     self.code_subject = int(self.code[:2])
        #     self.code_region = int(self.code[2:5])
        #     self.code_city = int(self.code[5:8])
        #     self.code_locality = int(self.code[8:11])
        #     self.code_relevance = int(self.code[11:13])
        # elif len(self.code) == len("ССРРРГГГПППУУУУАА"):
        #     pass
        # elif len(self.code) == len("ССРРРГГГПППУУУУДДДД"):
        #     pass
        # else:
        #     raise ValueError("Kladr code langth must be 13, 17 or 19")

        # if not self.is_subject:
        #     codes = self.get_codes()
        #     codes['code_relevance'] = 0
        #     self.parent = self._find_parent(codes)
        super(Kladr, self).save(*args, **kwargs)

    def __str__(self):
        return(self.code)
