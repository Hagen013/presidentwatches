class Cart():

    CART_SESSION_ID = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_ID)
    
    def add_offer(self):
        pass

    def remove_offer(self):
        pass

    def update_offer(self):
        pass

    def calculate_total_price(self):
        pass

    def calculate_total_quantity(self):
        pass

    def clear(self):
        pass
