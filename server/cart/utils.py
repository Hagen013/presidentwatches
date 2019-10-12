from .models import Promocode

from .constants import (PICKPOINT_TO_CDEK_STATUS_CODE_MAPPING,
                        RUPOST_TO_CDEK_STATUS_CODE_MAPPING,
                        RUPOST_TEXT_TO_STATUS_MAPPING)

def get_promocode_by_brand(brand):
    return Promocode.objects.filter(brands__in=self.brand).order_by(sale_amount)

def pickpoint_to_cdek_code(code):
    return PICKPOINT_TO_CDEK_STATUS_CODE_MAPPING.get(code, code)

def rupost_to_cdek_code(code):
    cdek_code = RUPOST_TO_CDEK_STATUS_CODE_MAPPING.get(str(code), None)
    if cdek_code is None:
        return code
    return cdek_code

def rupost_msg_to_code(msg):
    return RUPOST_TEXT_TO_STATUS_MAPPING.get(msg, 0)
