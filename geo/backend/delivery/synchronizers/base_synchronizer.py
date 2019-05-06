from ..models import Delivery


class BaseSynchronizer(object):
    """
    Абстрактный класс-синхронизатор синхронизирует службы доставки.

    """
    delivery_type = None
    queryset = None

    def sync(self):
        """
        Ядро синхронизации

        Использует в себе методы:
        * get_data()
        * get_deleted_rows()
        * get_existing_rows()
        * get_new_rows()
        * sync_item()
        """
        data = self.get_data()

        # Удалить все удалённые
        self.queryset.filter(
            delivery_code__in=self.get_deleted_rows(data.keys())
        ).delete()

        # Изменить существующие
        for dp in self.queryset.filter(
            delivery_code__in=self.get_existing_rows(data.keys())
        ):
            self.sync_item(dp, data[dp.delivery_code])
            dp.save()

        # Создать новые
        for new_dp_code in self.get_new_rows(data.keys()):
            new_dp = Delivery(delivery_code=new_dp_code,
                              delivery_type=self.delivery_type
                              )
            self.sync_item(new_dp, data[new_dp_code])
            new_dp.save()

    def get_data(self):
        """
        Необходимо переопределить в дочерних классах
        Метод должен возвращать данные в формате словаря
        Ключ которого соответствует delivery_code в базе,
        а значение является данными, из которых будет
        извлечено значение соответствующим методом в sync_item(),
        например get_kladr()
        """
        pass

    def _get_db_code_set(self):
        """
        DRY for get_<new/existing/deleted>_rows()
        """
        return set(
            (
                x['delivery_code'] for x in self.queryset.filter(
                    delivery_type=self.delivery_type
                ).values('delivery_code')
            )
        )

    def get_new_rows(self, new_delivery_codes):
        """
        Возвращает список новых delivery_code
        Возможно необходимо переопределить в дочерних
        классах
        """
        return list(set(new_delivery_codes) - self._get_db_code_set())

    def get_existing_rows(self, new_delivery_codes):
        """
        Возвращает список существующих delivery_code
        Возможно необходимо переопределить в дочерних
        классах
        """
        return list(set(new_delivery_codes) & self._get_db_code_set())

    def get_deleted_rows(self, new_delivery_codes):
        """
        Возвращает список удалённых delivery_code
        Возможно необходимо переопределить в дочерних
        классах
        """
        return list(self._get_db_code_set() - set(new_delivery_codes))

    def sync_item(self, dp, item_data):
        """
        Метод синхронизирует экземпляр модели и значение словаря
        """
        dp.kladr = self.get_kladr(item_data)
        dp.latitude = self.get_latitude(item_data)
        dp.longitude = self.get_longitude(item_data)
        dp.city = self.get_city(item_data)
        dp.address = self.get_address(item_data)
        dp.opening_hours = self.get_opening_hours(item_data)
        dp.description = self.get_description(item_data)
        dp.delivery_price = self.get_delivery_price(item_data)
        dp.delivery_time = self.get_delivery_time(item_data)

    # Методы получения данных для экземпляра маодели
    # использующиеся в sync_item()
    @classmethod
    def get_kladr(cls, item_data):
        return item_data['kladr']

    @classmethod
    def get_latitude(cls, item_data):
        return item_data['latitude']

    @classmethod
    def get_longitude(cls, item_data):
        return item_data['longitude']

    @classmethod
    def get_city(cls, item_data):
        return item_data['city']

    @classmethod
    def get_address(cls, item_data):
        return item_data['address']

    @classmethod
    def get_opening_hours(cls, item_data):
        return item_data['opening_hours']

    @classmethod
    def get_description(cls, item_data):
        return item_data['description']

    @classmethod
    def get_delivery_price(cls, item_data):
        return item_data['delivery_price']

    @classmethod
    def get_delivery_time(cls, item_data):
        return item_data['delivery_time']
