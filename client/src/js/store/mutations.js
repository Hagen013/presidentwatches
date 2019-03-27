export default {
    addItem(state, payload) {
        state.items.push(payload);
        return state;
    },
    clearItem(state, payload) {
        state.items.splice(payload.index, 1);
        return state;
    },
    updateCart(state, payload) {
        console.log('updating');
        state.cart.data = payload;
        return state
    }
};
