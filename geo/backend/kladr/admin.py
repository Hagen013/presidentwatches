from django.contrib import admin
from .models import Kladr


class KladrAdmin(admin.ModelAdmin):
    search_fields = ('code', 'full_name')
    list_display = (
        "code",
        "code_subject",
        "code_region",
        "code_city",
        "code_locality",
        "code_street",
        "code_relevance",
        "name",
        "kladr_type_socr",
        "kladr_type",
        "index",
        "houses_num",
        "status",
    )
    readonly_fields = ("code_subject", "code_region", "code_city",
                       "code_locality", "code_street", "code_relevance",
                       "full_name")

    fields = (
        ('code', 'name', 'kladr_type', ),
        ('full_name',),
        ('index', 'status', ),
        ("code_subject", "code_region", "code_city",
         "code_locality", "code_street", "code_relevance",),
    )

admin.site.register(Kladr, KladrAdmin)
