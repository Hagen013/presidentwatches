export default {
    addItem(context, payload) {
        context.commit('addItem', payload);
    },
    clearItem(context, payload) {
        context.commit('clearItem', payload);
    },
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
            console.log('commiting');
            console.log(res);
            context.commit('updateCart', res)
        })
    }
};
