# Файл содержит переменные словарей для mapping'a старых атрибутов PresidentWatches в новые

# Поля для записи в колонки
columns = [
    {
        'tag': 'extra_info',
        'title': 'Дополнительная информация',
        'type': 'string'
    },
    {
        'tag': 'guarantee',
        'title': 'Гарантия',
        'type': 'integer',
    },
    {
        'tag': 'model',
        'title': 'Модель',
        'type': 'string'
    },
    {
        'tag': 'certificate',
        'title': 'Сертификат',
        'type': 'file'
    },
    {
        'tag': 'manual',
        'title': 'Руководство',
        'type': 'file'
    },
    {
        'tag': 'height',
        'title': 'Длина',
        'type': 'float',
        'measure': 'мм'
    },
    {
        'tag': 'width',
        'title': 'Ширина',
        'type': 'float',
        'measure': 'мм'
    },
    {
        'tag': 'weight',
        'title': 'Вес',
        'type': 'float',
        'measure': 'гр.'
    },
    {
        'tag': 'precision',
        'title': 'Точность хода',
        'type': 'string'
    },
    {
        'tag': 'package',
        'title': 'Комплектация',
        'type': 'string'
    },
]

# Поля для записи в обычные Attribute
other_fields = [
    {
        'tag': 'alarm_presets',
        'title': 'Будильник (кол-во установок)',
        'type': 'integer'
    },
    {
        'tag': 'mech_desc',
        'title': 'Механизм',
        'type': 'string'
    },
]

# Поля для записи в (Single) Choice Attributes
choice_fields = [
    {
        'tag': 'vendor',
        'title': 'Бренд',
        'type': 'string'
    },
    {
        'tag': 'mech_type',
        'title': 'Тип механизма',
        'choices': [
            'Кварцевые',
            'Механические'
        ]
    },
    {
        'tag': 'illuminated_obj',
        'title': 'Подсветка',
        'choices': [
            'стрелок',
            'дисплея',
            'дисплея, стрелок'
        ]
    },
    {
        'tag': 'display_type',
        'title': 'Способ отображения времени',
        'choices': [
            'Аналоговый (стрелки)',
            'аналоговый + цифровой',
            'цифровой (электронный)',
        ]
    },
    {
        'tag': 'waterproof',
        'title': 'Водонепроницаемые',
        'choices': [
            '30',
            '50',
            '100',
            '200'
        ]
    },
    {
        'tag': 'size',
        'title': 'Размер',
        'choices': [
            'Маленькие',
            'Средние',
            'Большие'
        ]
    },
    {
        'tag': 'date_display',
        'title': 'Отображение даты',
        'choices': [
            'нет',
            'число',
            'число, месяц',
            'число, день недели',
            'число, месяц, день недели',
            'число, месяц, год, день недели'
        ]
    },
]

# Поля для записи в MultiChoice Attributes
multichoice_fields = [
    {
        'tag': 'watch_type',
        'title': 'Тип часов',
        'choices': [
            'Мужские',
            'Женские',
            'Детские',
            'Секундомер'
        ]
    },
    {
        'tag': 'hours',
        'title': 'Формат времени',
        'choices': [
            '12 часов',
            '12/24 часа'
        ]
    },
    {
        'tag': 'second_hand',
        'title': 'Секундная стрелка',
        'choices': [
            'отсутствует',
            'центральная',
            'смещенная',
        ]
    },
    {
        'tag': 'digits',
        'title': 'Цифры',
        'choices': [
            'Арабские',
            'Арабские + римские',
            'Римские',
            'Отсутствуют'
        ]
    },
    {
        'tag': 'energy',
        'title': 'Источник энергии',
        'choices': [
            'Батарейка',
            'Солнечная батарейка',
            'Пружинный механизм',
            'Kinetic',
            'Автоподзавод'
        ]
    },
    {
        'tag': 'color',
        'title': 'Цвет',
        'choices': [
            'камуфляжный (милитари)',
            'белый',
            'черный',
            'желтый (золотой)',
            'зеленый',
            'синий (голубой)',
            'красный (оранжевый)',
            'коричневый',
            'фиолетовый',
            'серебряный (серый, металлик)',
            'бежевый',
            'разноцветный'
        ]
    },
    {
        'tag': 'style',
        'title': 'Стиль',
        'choices': [
            'Классический',
            'Спортивный',
            'Fashion',
            'Карманные',
            'Повседневный',
            'Для занятий спортом',
            'Ретро',
            'Военный'
        ]
    },
    {
        'tag': 'illuminated_type',
        'title': 'Тип подсветки',
        'choices': [
            'Люминесцентная',
            'Электролюминесцентная',
            'Светодиодная',
            'Стрелок'
        ]
    },
    {
        'tag': 'form_factor',
        'title': 'Форма часов',
        'choices': [
            'Квадрат',
            'Круг',
            'Овал',
            'Прямоугольник',
            'Бочкообразная',
            'Ромб',
            'Сердце',
            'Трапеция',
            'Другое'
        ]
    },
    {
        'tag': 'material',
        'title': 'Материал',
        'choices': [
            'Пластик',
            'Керамика',
            'Титан',
            'Нерж. сталь',
            'Латунь',
            'Золото',
            'Серебро',
            'Карбон',
            'Медь',
            'Алюминий',
            'Дерево',
            'Вольфрамовый сплав',
            'Цинково-алюминиевый сплав',
            'Нерж. сталь + стразы',
            'Нерж. сталь + позолота',
            'Нерж. сталь + керамика',
            'Нерж. сталь + пластик',
            'Нерж. сталь + дерево',
            'Нерж. сталь + кожа',
            'Нерж. сталь + силикон',
            'Алюминий + пластик',
            'Титан + пластик',
            'Титан + керамика',
        ]
    },
    {
        'tag': 'bracelet',
        'title': 'Браслет',
        'choices': [
            'Пластик',
            'Керамика',
            'Титан',
            'Нерж. сталь',
            'Каучук',
            'Кожа',
            'Текстиль',
            'Латунь',
            'Другой',
            'Резина',
            'Нейлон',
            'Силикон',
            'Золото',
            'Алюминий',
            'Нерж. сталь + керамика',
            'Нерж. сталь + дерево',
            'Нерж. сталь + позолота',
            'Нерж. сталь + платик',
            'Нерж. сталь + силикон',
            'Нерж. сталь + алюминий',
            'Пластик + карбон',
            'Нерж. сталь + кожа',
            'Текстиль + кожа',
            'Титан + керамика',
        ]
    },
    {
        'tag': 'jewel_inserts_type',
        'title': 'Вставка',
        'choices': [
            'агат',
            'аметист',
            'бирюза',
            'бриллиант',
            'гранат',
            'жемчуг',
            'кристаллы Swarovski',
            'оникс',
            'опал',
            'рубин',
            'сапфир',
            'топаз',
            'фианит',
            'хрусталь',
            'циркон',
        ],
    },
    {
        'tag': 'glass',
        'title': 'Стекло',
        'choices': {
            'Минеральное',
            'Пластиковое',
            'Сапфировое'
        }
    },
    {
        'tag': 'symbolics',
        'title': 'Символика',
        'choices': [
            'нет',
            'герб России',
            'флаг России',
            'герб и флаг России'
        ]
    },
    {
        'tag': 'sport_functions',
        'title': 'Спорт-функции',
        'choices': {
            'Секундомер',
            'Таймер',
            'Шагомер',
            'Глубиномер',
            'Пульсометр',
            'Высотомер (альтиметр)',
            'Барометр',
            'Термометр',
            'Компас'
        }
    },
    {
        'tag': 'additional_functions',
        'title': 'Дополнительные функции',
        'choices': [
            'Калькулятор',
            'Записная книжка',
            'Индикатор запаса хода',
            'Второй часовой пояс',
            'Указатель фаз Луны',
            'Будильник',
            'Встроенная память'
        ]
    }
]

# Булевы поля
boolean = [
    {
        'tag': 'gold_n_black',
        'title': "Gold\'n\'Black"
    },
    {
        'tag': 'skeleton',
        'title': 'skeleton',
    },
    {
        'tag': 'shock_resistant',
        'title': 'Противоударные'
    },
    {
        'tag': 'thin_size',
        'title': 'Тонкие'
    },
    {
        'tag': 'limited_edition',
        'title': 'Limited Edition'
    },
    {
        'tag': 'single_hand',
        'title': 'Однострелочные'
    },
    {
        'tag': 'calendar',
        'title': 'Календарь'
    },
    {
        'tag': 'chronometer',
        'title': 'Хронометр'
    },
    {
        'tag': 'self_winding',
        'title': 'Автоподзавод'
    },
    {
        'tag': 'tachymeter',
        'title': 'Тахиметер'
    },
    {
        'tag': 'bluetooth',
        'title': 'Bluetooth'
    },
    {
        'tag': 'gps',
        'title': 'GPS'
    },
    {
        'tag': 'stop_watch',
        'title': 'Секундомер'
    },
    {
        'tag': 'timer',
        'title': 'Таймер'
    },
    {
        'tag': 'pedometer',
        'title': 'Шагомер'
    },
    {
        'tag': 'depth_finder',
        'title': 'Глубиномер'
    },
    {
        'tag': 'pulsometer',
        'title': 'Пульсометр'
    },
    {
        'tag': 'altimeter',
        'title': 'Высотомер (альтимер)'
    },
    {
        'tag': 'barometer',
        'title': 'Барометр'
    },
    {
        'tag': 'thermometer',
        'title': 'Термометр'
    },
    {
        'tag': 'compass',
        'title': 'Компас'
    },
    {
        'tag': 'calculator',
        'title': 'Калькулятор'
    },
    {
        'tag': 'notebook',
        'title': 'Калькулятор'
    },
    {
        'tag': 'power_reserve',
        'title': 'Индикаторз запаса хода'
    },
    {
        'tag': 'alt_timezone',
        'title': 'Второй часовой пояс'
    },
    {
        'tag': 'moon_phase',
        'title': 'Указатель фаз Луны'
    },
    {
        'tag': 'alarm',
        'title': 'Будильник'
    },
    {
        'tag': 'memory',
        'title': 'Встроенная память'
    },
    {
        'tag': 'led_display',
        'title': 'LED-часы'
    },
    {
        'tag': 'rhinestones',
        'title': 'Стразы'
    },
    {
        'tag': 'reverse_turn',
        'title': 'Обратный ход стрелок'
    },
    {
        'tag': 'jewel_inserts',
        'title': 'Камень-вставка'
    },
    {
        'tag': 'orient_college',
        'title': 'Orient College'
    },
    {
        'tag': 'sssr',
        'title': 'СССР'
    },
    {
        'tag': 'military',
        'title': 'Армейские'
    },
]

# Группы атрибутов
attributes_groups = {
    'Общие характеристики': [
        'watch_type',
        'mech_type',
        'mech_desc',
        'hours',
        'seconds_handle',
        'display_type',
        'digits',
        'energy',
        'color',
        'style',
        'gold_n_black',
        'illuminated',
        'illuminated_obj',
        'illuminated_type',
    ],
    'Конструкция': [
        'skeleton',
        'Противоударные',
        'waterproof',
        'form_factor',
        'material',
        'bracelet',
        'jewel_inserts_type',
        'glass',
        'size',
        'thin_size',
    ],
    'Особенности': [
        'limited_edition',
        'single_hand',
        'precision',
        'date_display',
        'calendar',
        'chronometer',
        'self_winding',
        'chronograph',
        'tachymeter',
        'bluetooth',
        'gps',
        'sport_functions',
        'timer',
        'pedometer',
        'depth_finder',
        'altimeter',
        'barometer',
        'thermometer',
        'compass',
        'additional_functions',
        'calculator',
        'notebook',
        'power_reserve',
        'alt_timezone',
        'moon_phase',
        'alarm_presets',
        'memory',
        'led_display',
        'rhinestones',
        'extra_info',
        'reverse_turn',
        'jewel_inserts',
    ],
    'Неотображаемые характеристики': [
        'orient_college',
        'sssr',
        'military',
        'symbolics'
    ]
}
