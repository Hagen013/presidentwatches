from .cart import Cart
from dateutil.parser import parse

def cart_processor(request):
    cart = Cart(request)
    sale = cart.data.get('total_sale', None)
    if sale is None:
        cart.clear()

    return {
        'cart': cart
    }    