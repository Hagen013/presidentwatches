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
    setActiveFacetes(state, payload) {
        for (let i=0; i<payload.length; i++) {
            let item = payload[i];
            if (state.facetes.active[item.key] !== undefined) {
                state.facetes.active[item.key].push(item.id);
            } else {
                state.facetes.active[item.key] = [item.id,]
            }

        }
    },
    setBaseFacetes(state, payload) {
        for (let i=0; i<payload.length; i++) {
            let item = payload[i];
            if (state.facetes.base[item.key] !== undefined) {
                state.facetes.base[item.key].push(item.id);
            } else {
                state.facetes.base[item.key] = [item.id,]
            }
        }
    },

    addActiveOption(state, payload) {
        let key = payload['key'];
        let value = payload['value'];

        if (state.facetes.active[key] === undefined) {
            state.facetes.active[key] = [value]
        } else {
            let index = state.facetes.active[key].indexOf(value);
            if (index === -1) {
                state.facetes.active[key].push(value);
            }
        }

        if (state.facetes.removedBase[key] !== undefined) {
            let index = state.facetes.removedBase[key].indexOf(value);
            if (index !== -1) {
                state.facetes.removedBase[key].splice(index, 1);
                if (state.facetes.removedBase[key].length === 0) {
                    delete state.facetes.removedBase[key];
                }
            }
        } else if (state.facetes.removed[key] !== undefined) {
            let index = state.facetes.removed[key].indexOf(value);
            if (index !== -1) {
                state.facetes.removed[key].splice(index, 1);
            }
            if (state.facetes.removed[key].length === 0) {
                delete state.facetes.removed[key];
            }
        }
    },
    removeActiveOption(state, payload) {
        let key = payload['key'];
        let value = payload['value'];

        let activeBaseEqual = false;

        if (state.facetes.active[key] !== undefined) {
            let index = state.facetes.active[key].indexOf(value);
            if (index !== -1) {
                state.facetes.active[key].splice(index, 1);
                if (state.facetes.base[key] !== undefined) {
                    activeBaseEqual = true;
                    for (let i=0; i<state.facetes.active[key].length; i++) {
                        let value = state.facetes.active[key][i];
                        let index = state.facetes.base[key].indexOf(value);
                        if (index === -1) {
                            activeBaseEqual = false;
                            break
                        }
                    }
                }
                if ( (state.facetes.active[key].length === 0) || activeBaseEqual ) {
                    delete state.facetes.active[key];
                    state.facetes.removed[key] = [];
                }
            }
        }

        if (state.facetes.base[key] !== undefined) {
            let index = state.facetes.base[key].indexOf(value);
            if (index !== -1) {
                if (state.facetes.removedBase[key] !== undefined) {
                    let removedIndex = state.facetes.removedBase[key].indexOf(value);
                    if (removedIndex !== -1) {
                        state.facetes.removedBase[key].push(value);
                    }
                } else {
                    state.facetes.removedBase[key] = [value]
                }
            }
        }
        console.log(state.facetes.active)
    },
};
