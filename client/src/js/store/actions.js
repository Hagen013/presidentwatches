import api from '@/api'


export default {
    addToCart(context, payload) {
        let url = '/api/v0/cart/items/';
        let data = JSON.stringify(payload);
        return fetch(
            url,
            {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: 'post',
                body: data,
                credentials: 'same-origin'
            }
        )
        .then(res => res.json())
        .then(res => {
            context.commit('updateCart', res)
        })
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
