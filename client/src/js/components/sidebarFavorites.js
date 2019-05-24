import Component from '@/lib/component.js';
import store from '@/store/favorites/';
import cartStore from '@/store/index'

export default class sidebarFavorites extends Component {

    constructor() {
        super({
            store,
            element: document.getElementById('sidebar-favorite-items')
        });
    }

    initialize() {
        this._cacheDom();
        this._bindMethods();
    }

    _cacheDom() {
        this.$element = $(this.element);
    }

    _bindMethods() {
        let self = this;

        this.$element.find('.card-mini__delete').click(function() {
            let pk = $(this).parents('.sidebar-card').attr('data-pk');
            self.remove(pk);
        })

        this.$element.find('.card-mini-buy').click(function() {
            let pk = $(this).parents('.sidebar-card').attr('data-pk');
            self.addToCart(pk);
        })
    }

    remove(pk) {
        store.dispatch('removeFromFavorites', {'pk': pk});
    }

    addToCart(pk) {
        cartStore.dispatch('addToCart', {model: pk})
    }

    addAllToCart() {

    }

    render() {
        let self = this;
        let items = [];
        for (let key in store.state.favorites.items) {
            items.push(store.state.favorites.items[key]);
        }

        self.element.innerHTML = `
        ${items.map(item => {
            return `
            <li class='card-mini sidebar-card' data-pk="${item['id']}"
            >
                <div class="card-mini__img-wrap">
                    <a class="link-wrap" href="/watches/${item['slug']}/">
                        <img class="card-mini__img" src="${item['image']}">
                    </a>
                </div>
                <div class="card-mini__content">
                    <a class="link-wrap" href="/watches/${item['slug']}/">
                        <div class="card-mini__brand">
                            ${item['brand']}
                        </div>
                        <div class="card-mini__series">
                            ${item['series']}
                        </div>
                        <div class="card-mini__model">
                            ${item['model']}
                        </div>
                    </a>
                    <div class="card-mini-buy fab fab-mini fab_accent" data-pk="${item['pk']}">
                        <i class="icon icon_cart">
                        </i>
                    </div>
                    <div class="card-mini__price">
                        <span class="price">${item['price']}</span>
                    </div>
                </div>
                <div class="card-mini__delete">
                    <i class="icon icon_close">
                    </i>
                </div>
            </li>
            `
        }).join('')}`;

        this._bindMethods();
    }

}