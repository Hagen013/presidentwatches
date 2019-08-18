export default {

    // DEVICE
    setResolutionMode(state, payload) {
        state.device.resolutionMode = payload;
    },
    // END DEVICE

    // CART
    addItem(state, payload) {
        state.items.push(payload);
        return state;
    },
    clearItem(state, payload) {
        state.items.splice(payload.index, 1);
        return state;
    },
    updateCart(state, payload) {
        state.cart.data = payload;
        return state
    },
    // END CART

};
