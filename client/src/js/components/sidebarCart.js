import Component from '@/lib/component.js';
import store from '@/store/index.js';
import favoritesStore from '@/store/favorites'
import toggleSidebarTab from '@/utils/toggleSidebarTab'
import api from '@/api/index'
import message from '@/lib/message'
import { debounce } from 'debounce'

export default class sidebarCart extends Component {

    constructor() {
        super({
            store,
            element: document.getElementById('sidebar-cart-items')
        });
    }

    initialize() {

        this.$element = $(this.element);
        this.applyPromocode = debounce(function(value) {
            value = value.toUpperCase();
            if (value.length === 0) {
                $('#sidebar-old-price').removeClass('active');
            }
            api.get('/cart/promocode/', {params: {name: value}}).then(
                response => {
                    store.commit('updateCart', response.data)
                    api.get('/promocodes/search/', {params: {name: value}}).then(
                        res => {
                            $('#sidebar-old-price').addClass('active');
                            $('#sidebar-old-price').find('.price').text(store.state.cart.data.total_sale+store.state.cart.data.total_price)
                            message({
                                type: 'success',
                                title: 'Промокод применен',
                                text: res.data.description + `<p class="bold message-sale">Ваша скидка: <span class="price">${store.state.cart.data.total_sale}</span><p>`,
                                link: '<a class="message-btn message-btn-1" href="/info/promo/">ВСЕ ПРОМОКОДЫ</a>'
                            })
                        },
                        res => {

                        }
                    )
                },
                response => {
                    console.log(response);
                }
            )
        }, 500)
        this.bindMethods();
    }

    removeItem(target) {
        let pk = target.parentNode.getAttribute('data-pk');
        store.dispatch('removeFromCart', {pk: pk});
    }

    decrementItem(target) {
        let model = $(target).parents('.card-mini').attr('data-pk');
        let quantity = Number($(target).siblings('.item-quantity').text());
        quantity -= 1;
        if (quantity <= 0 ) {
            store.dispatch('removeFromCart', {pk: model});
        } else {
            store.dispatch('updateQuantity', {pk: model, quantity: quantity});
        }
    }

    incrementItem(target) {
        let model = $(target).parents('.card-mini').attr('data-pk');
        let quantity = Number($(target).siblings('.item-quantity').text());
        quantity += 1;
        store.dispatch('updateQuantity', {pk: model, quantity: quantity});
    }

    clearCart() {
        store.dispatch('clearCart');
    }

    addToFavorites(payload) {
        favoritesStore.dispatch('addToFavorites', payload);
        toggleSidebarTab('#favorites');
    }

    bindMethods() {
        let self = this;

        this.$element.find('.card-mini__delete').click(function(e) {
            self.removeItem(this);
        })

        this.$element.find('.quantity_decrement').click(function(e) {
             self.decrementItem(this);
        })

        this.$element.find('.quantity_increment').click(function(e) {
            self.incrementItem(this);
        })

        $('#sidebar-cart-clear').click(function(e) {
            self.clearCart();
        })

        $('#sidebar-promocode').on('input', function(e){
            self.applyPromocode(this.value);
        })
    }

    render() {
        let self = this;
        let items = [];
        for (let key in store.state.cart.data.items) {
            items.push(store.state.cart.data.items[key]);
        }
        items = items.sort(function(a,b) {
            let date1 = a.added_at;
            let date2 = b.added_at;
            if (date1 > date2) return 1;
            if (date1 < date2) return -1;
            return 0;
        })
        self.element.innerHTML = `
        ${items.map(item => {
            return `
            <li class='card-mini sidebar-card' data-pk='${item['pk']}'>
                <div class='card-mini__img-wrap'>
                    <a class="link-wrap" href="/watches/${item['slug']}/">
                        <img class='card-mini__img' src='${item['image']}'>
                    </a>
                </div>
                <div class='card-mini__content'>
                    <a class="link-wrap" href="/watches/${item['slug']}/">
                        <div class='card-mini__brand'>
                            ${item['brand']}
                        </div>
                        <div class='card-mini__series'>
                            ${item['series']}
                        </div>
                        <div class='card-mini__model'>
                            ${item['model']}
                        </div>
                    </a>
                    <div class='card-mini__controls row'>
                        <div class='quantity-controls row'>
                            <div class='quantity-btn quantity_decrement cart-item__button'>
                                -
                            </div>
                            <div class='item-quantity'>
                            ${item['quantity']}
                            </div>
                            <div class="quantity-btn quantity_increment cart-item__button">
                                +
                            </div>
                        </div>
                        <div class="card-mini__price text_right">
                            <span class="price">${item['base_price']}</span>
                        </div>
                    </div>
                </div>
                <div class="card-mini__delete">
                    <i class="icon icon_close">
                    </i>
                </div>
                <div class="card-mini__favorite like"
                    data-id="${item['pk']}"
                >
                    <i class="icon icon-like">
                    </i>
                </div>
            </li>
            `
        }).join('')}`;

        $('#sidebar-total-price').text(store.state.cart.data.total_price);
        $('.cart-count').text(store.state.cart.data.total_quantity);
        let favoriteItems = $('#sidebar-favorite-items').find('.sidebar-card');
        let ids = [];
        for (let i=0; i<favoriteItems.length; i++) {
            let dataId = favoriteItems[i].getAttribute('data-pk');
            ids.push(dataId);
        }
        let likes = this.$element.find('.like');
        for (let i=0; i<likes.length; i++) {
            let dataId = likes[i].getAttribute('data-id');
            if (ids.indexOf(dataId) !== -1) {
                $(likes[i]).addClass('like_active');
            }
            $(likes[i]).click(function() {
                if ( !$(this).hasClass('like_active') ) {
                    let pk = this.getAttribute('data-id');
                    $(this).addClass('like_active');
                    self.addToFavorites({pk: pk});
                }
            })
        }
        
        self.bindMethods()
    }
};
