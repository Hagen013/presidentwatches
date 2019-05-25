import store from '@/store/favorites/index.js';
import toggleSidebarTab from '@/utils/toggleSidearTab'


export default class Likes {

    constructor() {
        this._bindMethods();
    }

    _bindMethods() {
        let self = this;

        $('.like').click(function() {
            let pk = this.getAttribute('data-id');
            if ( !$(this).hasClass('like_active') ) {
                $(this).addClass('like_active');
                self.addToFavorites({pk: pk});
            }
        })
    }

    addToFavorites(payload) {
        store.dispatch('addToFavorites', payload);
        toggleSidebarTab('#favorites');
    }

}