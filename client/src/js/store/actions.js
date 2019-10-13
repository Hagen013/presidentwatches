import api from '@/api'


export default {
    addToCart(context, payload) {
        let data = JSON.stringify(payload);
        api.post('/cart/items/', data).then(
            response => {
                context.commit('updateCart', response.data);
                try { rrApi.addToBasket(payload.pk) } catch(e) {};
                let key = parseInt(payload.pk);
                let item  = response.data.items[key];
                dataLayer.push({
                    "event": "AddToCart",
                    "ecommerce": {
                        "add": {
                            "products": [
                                {
                                    "id": String(item.pk),
                                    "name": item.model,
                                    "price": item.price,
                                    "brand": item.brand,
                                    "category": "Наручные часы",
                                    "quantity": 1
                                }
                            ]
                        }
                    }
                })
            },
            response => {

            }
        )
    },
    transferFavorites2Cart(context, payload) {
        api.get('/cart/fav2cart/')
            .then(response => {
                context.commit('updateCart', response.data);
                let items = response.data.items;
                let products = [];
                for (let key in items) {
                    let item = items[key];
                    products.push({
                        "id": String(item.pk),
                        "name": item.model,
                        "price": item.price,
                        "brand": item.brand,
                        "category": "Наручные часы",
                        "quantity": item.quantity
                    })
                }
                dataLayer.push({
                    "event": "AddToCart",
                    "ecommerce": {
                        "add": {
                            "products": products
                        }
                    }
                })
            })
            .catch(error => {
            })
    },
    removeFromCart(context, payload) {
        api.delete(`/cart/items/${payload.pk}/`)
            .then(response => {
                context.commit('updateCart', response.data.cart);
                let item = response.data.deleted;
                products = [{
                    "id": String(item.pk),
                    "name": item.model,
                    "price": item.price,
                    "brand": item.brand,
                    "category": "Наручные часы",
                    "quantity": item.quantity
                },];
                dataLayer.push({
                    "event": "RemoveFromCart",
                    "ecommerce": {
                        "remove": {
                            "products": products
                        }
                    }
                })
            })
            .catch(error => {
            })
    },
    updateQuantity(context, payload) {
        api.put(`/cart/items/${payload.pk}/quantity/${payload.quantity}/`)
            .then(response => {
                context.commit('updateCart', response.data.cart);
                let item = response.data.changed;
                let products = [{
                    "id": String(item.pk),
                    "name": item.model,
                    "price": item.price,
                    "brand": item.brand,
                    "category": "Наручные часы",
                    "quantity": 1
                },];
                if (payload.quantity > response.data.quantity) {
                    dataLayer.push({
                        "event": "AddToCart",
                        "ecommerce": {
                            "add": {
                                "products": products
                            }
                        }
                    })
                } else {
                    dataLayer.push({
                        "event": "RemoveFromCart",
                        "ecommerce": {
                            "remove": {
                                "products": products
                            }
                        }
                    })                    
                }
            })
            .catch(error => {
            })
    },
    clearCart(context, payload) {
        api.delete('/cart/')
            .then(response => {
                context.commit('updateCart', response.data.cart);
                let items = response.data.deleted;
                let products = [];
                for (let key in items) {
                    let item = items[key];
                    products.push({
                        "id": String(item.pk),
                        "name": item.model,
                        "price": item.price,
                        "brand": item.brand,
                        "category": "Наручные часы",
                        "quantity": item.quantity
                    })
                }
                dataLayer.push({
                    "event": "RemoveFromCart",
                    "ecommerce": {
                        "remove": {
                            "products": products
                        }
                    }
                })
            })
            .catch(error => {
            })
    },
};
