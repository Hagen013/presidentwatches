import api from '@/api'

export default {
    addToFavorites(context, payload) {
        api.post('/favorites/', payload)
            .then(response => {
                context.commit('updateFavorites', response.data);
            })
            .catch(error => {
            })
    },
    removeFromFavorites(context, payload) {
        api.delete(`/favorites/items/${payload.pk}`)
            .then(response => {
                context.commit('updateFavorites', response.data);
            })
            .catch(error => {
            })
    },
}