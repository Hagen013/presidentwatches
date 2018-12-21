import request from '@/utils/request'

const shop = {
    categories: {
        list(params={}) {
            return request.get('/categories/', {params})
        },
        create() {
            return null
        },
        get(id) {
            return request.get(`/categories/${id}/`);
        },
        update(id) {
            return null
        },
        delete(id) {
            return null
        }
    },
}

export default shop;