from shop.models import ProductPage as Product


def recalculate_rating():
    for instance in Product.objects.all():
        instance.rating = instance.get_average_rating()
        instance.save()
