from django.db import models 
from django.core.exceptions import ObjectDoesNotExist

from mptt.models import TreeManager


class DisplayableManager(models.Manager):

    def get_queryset(self):
        return super(DisplayableManager, self).get_queryset().\
            filter(is_published=True).\
            order_by('scoring')


class OrderableManager(models.Manager):

    def get_queryset(self):
        return super(OrderableManager, self).get_queryset().order_by('order')


class NodeManager(TreeManager):

    def rebuild(self):
        super(NodeManager, self).rebuild()
        for node in self.get_queryset():
            node.set_depth()
            node.save()
        for node in self.get_queryset():
            node.set_inputs()
        root = self.get_queryset().get(_depth=0)
        for node in self.get_queryset().filter(_depth=1):
            node.add_input(root)
        for node in self.get_queryset():
            if node.has_inputs:
                node.parent = node.inputs.all().order_by('-scoring')[0]
                node.save()
        super(NodeManager, self).rebuild()
        for node in self.get_queryset():
            old_url = node.slug
            new_url = node.get_graph_url()

            stored_node_exists = False
            try:
                stored_node = self.get_queryset().get(slug=new_url)
                stored_node_exists = True
            except ObjectDoesNotExist:
                pass

            if stored_node_exists:
                pass
            else:
                node.slug = new_url
            node.save()

            # Handling old outdated urls
            if old_url != node.slug:
                try:
                    instance = node.outdated_url_class.objects.get(
                        slug=old_url
                    )
                    instance.delete()
                except ObjectDoesNotExist:
                    pass
                instance = node.outdated_url_class(
                    node=node,
                    slug=old_url
                )
                instance.save()
        

    def get_by_product(self, product_instance):
        if product_instance.pk:
            try:
                return self.get(id=self
                                .get_queryset()
                                .values('id')
                                .filter(is_published=True)
                                .filter(attribute_values__in=product_instance
                                        .attribute_values
                                        .filter(attribute__name__in=['Бренд', 'Страна', 'Тип часов', 'Коллекция']))
                                .annotate(len_av=models.Count("id",
                                                              distinct=False)
                                          )
                                .order_by('-len_av', '-scoring')[0]['id'])
            except (IndexError, ObjectDoesNotExist):
                return self.get(slug='')
        else:
            raise DisallowedBeforeCreationException('product_instance must be creatied')

    def get_exact_node(self, values):
        if len(values) == 1:
            values = str(values).replace(",", "")
        elif len(values) == 0:
            return self.get_queryset().filter(level=0).order_by("id")
        query = """
        SELECT "shop_categorypage"."id", "shop_categorypage"."is_published", COUNT("shop_categoryvaluerelation"."value_id") AS "len_av"
        FROM "shop_categorypage"
        INNER JOIN "shop_categoryvaluerelation"
        ON ("shop_categoryvaluerelation"."entity_id"="shop_categorypage"."id")
        INNER JOIN "shop_attributevalue"
        ON ("shop_attributevalue"."id"="shop_categoryvaluerelation"."value_id")
        WHERE "shop_categorypage"."id" NOT IN (
            SELECT "shop_categorypage"."id"
            FROM "shop_categorypage"
            INNER JOIN "shop_categoryvaluerelation"
            ON ("shop_categorypage"."id" = "shop_categoryvaluerelation"."entity_id")
            WHERE "shop_categoryvaluerelation"."value_id" NOT IN {values}
            GROUP BY "shop_categorypage"."id"
        )
        AND "shop_categorypage"."is_published"=TRUE
        GROUP BY "shop_categorypage"."id"
        ORDER BY "len_av" DESC, "shop_categorypage"."scoring" DESC
        """.format(values=values)

        qs = self.raw(query)
        
        return qs


class NodePublicManager(NodeManager, DisplayableManager):

    def rebuild(self):
        raise Exception('Public namagers has no permissio to use rebuild() method')
