import store from '@/store/index.js'

import removeQueryParameter from './removeQueryParameter.js'
import updateQueryString from './updateQueryString.js'


export default function getRedirectionUrl() {
    let queryString = window.location.search;

    for (let key in store.state.facetes.removed) {
        queryString = removeQueryParameter(queryString, key);
    }

    for (let key in store.state.facetes.active) {

        let values = [];
        if (store.state.facetes.base[key] !== undefined) {
            values = store.state.facetes.active[key].filter(function(value) {
                return store.state.facetes.base[key].indexOf(value) === -1
            })
            values = values.join(',')
        } else {
            values = store.state.facetes.active[key].join(',');
        }

        if (values.length > 0) {
            queryString = updateQueryString(queryString, key, values)
        }
    }

    for (let key in store.state.facetes.removedBase) {
        let values = store.state.facetes.removedBase[key].join(',');
        let queryKey = '-' + key;
        queryString = updateQueryString(queryString, queryKey, values);
    }

    return window.location.pathname + queryString
}
