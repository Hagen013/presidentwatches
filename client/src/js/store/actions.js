import api from '@/api'


export default {
    addToCart(context, payload) {
        let data = JSON.stringify(payload);
        api.post('/cart/items/', data).then(
            response => {
                context.commit('updateCart', response.data);
                try { rrApi.addToBasket(payload.pk) } catch(e) {}
            },
            response => {

            }
        )
    },
    transferFavorites2Cart(context, payload) {
        api.get('/cart/fav2cart/')
            .then(response => {
                context.commit('updateCart', response.data);
            })
            .catch(error => {
            })
    },
    removeFromCart(context, payload) {
        api.delete(`/cart/items/${payload.pk}/`)
            .then(response => {
                context.commit('updateCart', response.data);
            })
            .catch(error => {
            })
    },
    updateQuantity(context, payload) {
        api.put(`/cart/items/${payload.pk}/quantity/${payload.quantity}/`)
            .then(response => {
                context.commit('updateCart', response.data);
            })
            .catch(error => {
            })
    },
    clearCart(context, payload) {
        api.delete('/cart/')
            .then(response => {
                context.commit('updateCart', response.data);
            })
            .catch(error => {
            })
    },
};
