from django.contrib import admin
# from .models import SdekCityList, Delivery, PickPointCityList
from .models import DeliveryDelay

# class SdekCitysAdmin(admin.ModelAdmin):
#     search_fields = ('city_name', 'full_name', 'kladr_code__code')
#     search_fields = ('full_name', 'city_name', 'obl_name')
#     fields = (
#         "city_id",
#         "full_name",
#         "city_name",
#         "obl_name",
#         "center",

#     )
#     list_display = (
#         "city_id",
#         "full_name",
#         "city_name",
#         "obl_name",
#         "center",
#         "get_kladr_name",
#         "kladr"
#     )

#     def get_kladr_name(self, obj):
#         if obj.kladr:
#             return obj.kladr.full_name
#         else:
#             return obj.kladr
#     get_kladr_name.admin_order_field = 'Kladr Name'
#     get_kladr_name.short_description = 'Kladr Name'


class PickpointCityCitysAdmin(admin.ModelAdmin):
    pass


# class DeliveryAdmin(admin.ModelAdmin):
#     search_fields = ('city', 'kladr__code', 'delivery_code')
#     fields = (
#         "delivery_code",
#         "delivery_type",
#         "latitude",
#         "longitude",
#         "city",
#         "address",
#         "opening_hours",
#         "description",
#         "delivery_price",
#         "delivery_time",
#     )
#     list_display = (
#         "delivery_code",
#         "kladr",
#         "get_kladr_name",
#         "delivery_type",
#         "latitude",
#         "longitude",
#         "city",
#         "opening_hours",
#         "delivery_price",
#         "delivery_time",
#         "modified_at"
#     )

#     def get_kladr_name(self, obj):
#         if obj.kladr:
#             return obj.kladr.full_name
#         else:
#             return obj.kladr
#     get_kladr_name.admin_order_field = 'author'
#     get_kladr_name.short_description = 'Author Name'


# admin.site.register(Delivery, DeliveryAdmin)
# admin.site.register(SdekCityList, SdekCitysAdmin)
admin.site.register(DeliveryDelay, PickpointCityCitysAdmin)
