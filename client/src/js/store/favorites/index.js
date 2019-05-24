import actions from './actions.js';
import mutations from './mutations.js';
import state from './state.js';
import Store from '../store.js';

let store = new Store({
    actions,
    mutations,
    state
});

export default store
