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
        state.cart.data = payload;
        return state
    },
    setBaseFacetes(state, payload) {
        for (let i=0; i<payload.length; i++) {
            let item = payload[i];

            if (state.facetes.base[item.key] !== undefined) {
                state.facetes.base[item.key].push(item.id);
            } else {
                state.facetes.base[item.key] = [item.id,]
            }
            if (state.facetes.active[item.key] !== undefined) {
                state.facetes.active[item.key].push(item.id);
            } else {
                state.facetes.active[item.key] = [item.id,]
            }
        }
    }
};
