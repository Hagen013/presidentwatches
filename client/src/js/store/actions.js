import api from '@/api'
import geoApi from '@/api/geo.js'


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
    removeFromCart(context, payload) {
        api.delete(`/cart/items/${payload.model}/`)
            .then(response => {
                context.commit('updateCart', response.data);
            })
            .catch(error => {
                console.log(error);
            })
    },
    updateQuantity(context, payload) {
        api.put(`/cart/items/${payload.model}/quantity/${payload.quantity}/`)
            .then(response => {
                context.commit('updateCart', response.data);
            })
            .catch(error => {
                console.log(error);
            })
    },
    clearCart(context, payload) {
        api.delete('/cart/')
            .then(response => {
                context.commit('updateCart', response.data);
            })
            .catch(error => {
                console.log(error);
            })
    },
    getLocation(context, payload) {
        geoApi.get('/api/geo_ip/').then(
            response => {
                console.log(response);
            },
            response => {
                console.log(response);
            }
        )
    }
};
