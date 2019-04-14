from elasticsearch_dsl import (
    DocType,
    Date,
    Keyword,
    Text,
    Boolean,
    Integer,
    Nested
)

from config.es_client import es_client


class CategoryIndex(DocType):

    class Meta:
        index = 'store'
        doc_type = 'category'
        using = es_client

    id = Integer()
    name = Text()
    absolute_url = Text()
    search_scoring = Integer()


class ProductPageIndex(DocType):

    index = 'store'

    class Meta:
        index = 'store'
        doc_type = 'product'
        using = es_client

    id = Integer()

    brand = Text()
    series = Text()
    model = Text()

    absolute_url = Text()
    _price = Integer()
