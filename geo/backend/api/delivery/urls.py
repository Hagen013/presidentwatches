from django.conf.urls import url, include

from .views import (OneProductDeliveryAPIView,
                    ManyProductsDeliveryAPIView)


delivery_urls = (
    [
        url(r'^one_product/$',
            OneProductDeliveryAPIView.as_view(),
            name='one_product'
            ),
        url(r'^meny_products/$',
            ManyProductsDeliveryAPIView.as_view()
            ),
        # url(r'^(?P<code>(\d{13})|(\d{17})|(\d{19}))/sdek_courier/$',
        #     SdekCourierDeliveryAPIView.as_view()
        #     ),
        # url(r'^(?P<code>(\d{13})|(\d{17})|(\d{19}))/sdek_points/$',
        #     SdekPointsDeliveryAPIView.as_view()
        #    ),
    ],
    'delivery'
)
