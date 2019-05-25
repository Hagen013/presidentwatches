from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from shop.models import ProductPage


class LastSeenController():

    LIMIT = 6
    SESSION_ID = 'last_seen'

    def __init__(self, request):
        self.session = request.session
        data = self.session.get(self.SESSION_ID)
        if not data:
            now = datetime.now().isoformat()
            data = {
                'items': [],
            }
            self.session[self.SESSION_ID] = data

        self.data = data

    
    def push(self, instance):

        offer_identifier = instance.id
        now = datetime.now().isoformat()
        identifier_mapping = set(map(lambda x: x['pk'], self.data['items']))

        if offer_identifier not in identifier_mapping:
            item = {
                'pk': instance.id,
                'model': instance.model,
                'price': instance.price,
                'old_price': instance.old_price,
                'total_price': instance.price,
                'image': instance.thumbnail.url,
                'slug': instance.slug,
                'url': instance.absolute_url,
                'added_at': now,
                'brand': instance.brand,
                'series': instance.series
            }
            self.data['items'].insert(0, item)
            self.data['items'] = self.data['items'][:self.LIMIT]

            self.session[self.SESSION_ID] = self.data
