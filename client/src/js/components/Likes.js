import store from '@/store';


export default class Likes {

    constructor() {
        this._bindMethods();
    }

    _bindMethods() {
        let self = this;

        $('.like').click(function() {
            let pk = this.getAttribute('data-id');
            $(this).addClass('like_active');
            self.addToFavorites({pk: pk});
        })
    }

    addToFavorites(payload) {
        store.dispatch('addToFavorites', payload);
    }

}