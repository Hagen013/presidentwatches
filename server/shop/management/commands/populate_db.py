import json

from django.db import transaction, IntegrityError
from django.core.management.base import BaseCommand

from shop.models import ProductPage, Attribute, AttributeValue, AttributeGroup
from shop.constants import (
    columns,
    other_fields,
    choice_fields,
    multichoice_fields,
    boolean,
    attributes_groups
)


def get_group_by_attr_tag(attribute_tag):
    group_name = attribute_2_group_mapping.get(attribute_tag, None)
    if group_name is None:
        return None
    return AttributeGroup.objects.get(name=group_name)


class Command(BaseCommand):
    help = 'Populates database by data from file'

    _lines = []
    _attribute_2_group_mapping = dict()

    def read_file(self, filename):

        products = []
        categories = []

        with open(filename, 'r') as fp:
            for line in fp:
                self.lines.append(line)
        
        for line in lines:
            instance = json.loads(line)
            fields = instance.get('fields', None)
            if fields is not None:
                price = fields.get('price', None)
                if price is not None:
                    products.append(instance)
                else:
                    categories.append(instance)
            else:
                categories.append(instance)

        data = {
            'products': products,
            'categories': categories
        }

        return data


    def get_group_by_attr_tag(self, attribute_tag):
        group_name = attribute_2_group_mapping.get(attribute_tag, None)
        if group_name is None:
            return None
        return AttributeGroup.objects.get(name=group_name)


    def add_choices(self, attribute, choices=None):
        if choices is None:
            msg = "Attribute has no choices: {attribute}".format(
                attribute=attribute
            )
            print(msg)
        else:
            for choice in choices:
                instance = AttributeValue(
                    attribute=attribute,
                    datatype=attribute.datatype,
                    value_enum=choice
                )
                instance.save()


    def populate_attributes(self):
        # Группы атрибутов
        AttributeGroup.objects.all().delete()

        with transaction.atomic():
            for index, group_name in enumerate(attributes_groups):
                instance = AttributeGroup(
                    order=index,
                    name=group_name
                )
                instance.save()

        # Атрибуты и значения
        Attribute.objects.all().delete()
        AttributeValue.objects.all().delete()
        
        # Отображение Атрибут -> Группа Атрибутов
        for key, values in attributes_groups.items():
            for value in values:
                self.attribute_2_group_mapping[value] = key

        for item in choice_fields:
            attribute = Attribute(
                name=item['title'],
                slug=item['tag'],
                datatype=AttributeType.Choice,
                group=get_group_by_attr_tag(item['tag'])
            )
            attribute.full_clean()
            attribute.save()
            choices = item.get('choices', None)
            self.add_choices(attribute=attribute, choices=choices)

        for item in multichoice_fields:
            attribute = Attribute(
                name=item['title'],
                slug=item['tag'],
                datatype=AttributeType.MultiChoice,
                group=get_group_by_attr_tag(item['tag'])
            )
            attribute.full_clean()
            attribute.save()

            choices = item.get('choices', None)
            self.add_choices(attribute=attribute, choices=choices)

        for item in boolean:
            s1 = {v.value_enum for v in Attribute.objects.get(slug='additional_functions').value_set.all()}
            s2 = {v.value_enum for v in Attribute.objects.get(slug='sport_functions').value_set.all()}
            migrated_boolean = s1.union(s2)
            if item['title'] not in migrated_boolean:
                attribute = Attribute(
                    name=item['title'],
                    slug=item['tag'],
                    datatype=AttributeType.Bool
                )
                attribute.full_clean()
                attribute.save()

        for item in other_fields:
            if item['type'] == 'integer':
                attribute = Attribute(
                    name=item['title'],
                    slug=item['tag'],
                    datatype=AttributeType.Integer,
                    group=get_group_by_attr_tag(item['tag'])
                )
                attribute.full_clean()
                attribute.save()
            elif item['type'] == 'string':
                attribute = Attribute(
                    name=item['title'],
                    slug=item['tag'],
                    datatype=AttributeType.Text,
                    group=get_group_by_attr_tag(item['tag'])
                )
                attribute.full_clean()
                attribute.save()

        attribute = Attribute.objects.get(name='Бренд')
        attribute.strict_options = False
        attribute.save()

        other_fields_slugs = {item['tag'] for item in other_fields}
        choice_fields_slugs = {item['tag'] for item in choice_fields}
        multichoice_fields_slugs = {item['tag'] for item in multichoice_fields}
        boolean_fields_slugs = {item['tag'] for item in boolean}

        self.attributes_slugs = other_fields_slugs.union(
            choice_fields_slugs,
            multichoice_fields_slugs,
            boolean_fields_slugs
        )

        # Поля, не участвующие в EAV
        exclude_fields = {
            'old_price',
            'price',
            'available',
            'score',
            'model',
            'new_product',
            'bestseller',
            'yml',
            'yml_sales_notes',
            'manual',
            'video_review',
            'old_id'
        }

        # convolutional boolean attributes
        self.bool_to_multichoice = {}

        s1 = {v.value_enum for v in Attribute.objects.get(slug='sport_functions').value_set.all()}
        s2 = {v.value_enum for v in Attribute.objects.get(slug='additional_functions').value_set.all()}
        s = s1.union(s2)

        for field in boolean:
            title = field['title']
            if title in s1:
                self.bool_to_multichoice[field['tag']] = 'sport_functions'
            elif title in s2:
                self.bool_to_multichoice[field['tag']] = 'additional_functions'


    def populate_products(self, products):
        invalids = []
        models_set = set()
        for row in products:
            fields = row.get('fields')

            _title = row.get('title', '')
            name = row.get('title', '')
            height = fields.get('height', 0)
            width = fields.get('width', 0)
            thickness = fields.get('thickness', 0)
            old_price = fields.get('old_price')
            price = fields.get('price', 0)
            weight = fields.get('weight', 0)
            is_in_store = fields.get('available', False)
            scoring = fields.get('score', 0)
            model = fields.get('model')
            is_new = fields.get('new_product', False)
            is_bestseller = fields.get('bestseller', False)
            yml = fields.get('yml', False)
            slug = row.get('slug')
            is_in_stock = fields.get('in_stock_tulskaya', False)

            _meta_title = row.get('meta_title', None)
            _meta_keywords = row.get('meta_keywords', None)
            _meta_description = row.get('meta_description', None)
            if _meta_title is None:
                _meta_title = ''
            if _meta_keywords is None:
                _meta_keywords = ''
            if _meta_description is None:
                _meta_description = ''
            
            if height is None:
                height = 0
            if width is None:
                width = 0
            if thickness is None:
                thickness = 0
            if weight is None:
                weight = 0
                
            if is_in_stock is None:
                is_in_stock = False

            if price is None:
                price = 0
            else:
                price = round(price)

            if old_price is None:
                old_price = 0
            else:
                old_price = round(old_price)
            
            if model is None or len(model) == 0:
                model = get_model_from_name(name)
                
            data = {
                'name': name,
                '_title': _title,
                'height': height,
                'width': width,
                'thickness': thickness,
                'old_price': old_price,
                '_price': price,
                '_weight': weight,
                'is_in_store': is_in_store,
                'is_in_stock': is_in_stock,
                'scoring': scoring,
                'model': model,
                'is_new': is_new,
                'is_bestseller': is_bestseller,
                'is_yml_offer': yml,
                'slug': slug,
                '_meta_title': _meta_title,
                '_meta_keywords': _meta_keywords,
                '_meta_description': _meta_description
            }
            
            if model not in models_set:
                instance = ProductPage(**data)
                instance.full_clean()
                instance.save()
                models_set.add(model)
            else:
                invalids.append(data)
        return invalids


    def get_product(self, slug):
        try:
            return ProductPage.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None


    def get_attribute(self, key, value):
        """
        Функция находит атрибут по значению key
        или по value, если не найден в первом случае
        """
        data = {
            'attribute': None,
            'value': value
        }
        try:
            attribute = Attribute.objects.get(slug=key)
            data['attribute'] = attribute
            return data
        except ObjectDoesNotExist:
            if key in boolean_2_choice_mapping.keys():
                value_alt = boolean_2_choice_mapping.get(key)
                if value_alt in s1:
                    attribute =  Attribute.objects.get(slug='sport_functions')
                    data['attribute'] = attribute
                    data['value'] = value_alt
                    return data
                elif value_alt in s2:
                    attribute = Attribute.objects.get(slug='additional_functions')
                    data['attribute'] = attribute
                    data['value'] = value_alt
                    return data
                else:
                    return data
            else:
                return data


    def get_value(self, attribute, value):
        """
        Функция находит AttributeValue по значению атрибута
        и value
        """
        value = lost_values_mapping.get(value, value)
        try:
            return AttributeValue.objects.get_or_create(
                attribute=attribute,
                value=value
            )
        except IllegalAssignmentException:
            msg = 'Undocumented option for attribute: {attribute} - {option}'.format(
                attribute=attribute.name,
                option=value
            )
            if value != 'Другой':
                print(msg)
            return None


    def process_attribute_value_pair(self, attribute, value, product):
        value_instance = self.get_value(attribute=attribute, value=value)
        if value_instance is not None:
            product.add_value(value_instance)
        else:
            if value != 'Другой':
                print('Value not found: {key} - {value}'.format(
                    key=key,
                    value=value
                ))


    def bind_values(self, rows):
        for row in rows:
            product = self.get_product(slug=row['slug'])
            if product is not None:
                fields = row['fields']
                filtered_keys = list(filter(lambda x: x in attributes_slugs, fields))
                for key in filtered_keys:
                    value = fields.get(key)
                    if value is not None:
                        data = self.get_attribute(key=key, value=value)
                        attribute = data['attribute']
                        value = data['value']
                        if attribute is not None:
                            
                            if type(value) == list:
                                for subvalue in value:
                                    self.process_attribute_value_pair(
                                        attribute=attribute,
                                        value=subvalue,
                                        product=product
                                    )
                            
                            else:
                                
                                self.process_attribute_value_pair(
                                    attribute=attribute,
                                    value=value,
                                    product=product
                                )
                                
                        else:
                            print('Attribute not found: {key}'.format(
                                key=key
                            ))


    def handle(self, *args, **options):
        data = self.read_file(options['-f'])
        self._products = data['products']
        self._categories = data['categories']
        with transaction.atomic():
            ProductPage.objects.all().delete()
            self.populate_products(products=products)


    def add_agruments(self, parser):
        parser.add_argument(
            '-f',
            'type'=argparse.FileType('r'),
            required=True
        )
 