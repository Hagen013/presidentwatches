import Component from '@/lib/component.js'
import store from '@/store/index.js'
import favoritesStore from '@/store/favorites'
import toggleSidebarTab from '@/utils/toggleSidebarTab'

export default class sidebarCart extends Component {

    constructor() {
        super({
            store,
            element: document.getElementById('cart-list')
        });
    }

    initialize() {
        this.$element = $(this.element);
        this._bindMethods();
    }

    _bindMethods() {
        let self = this;

        this.$element.find('.cart-item__delete').click(function(e) {
            self.removeItem(this);
        })

        this.$element.find('.quantity_decrement').click(function(e) {
            self.decrementItem(this);
        })

        this.$element.find('.quantity_increment').click(function(e) {
            self.incrementItem(this);
        })
    }

    removeItem(target) {
        let pk = target.getAttribute('data-pk');
        store.dispatch('removeFromCart', {pk: pk});
    }

    decrementItem(target) {
        let model = $(target).parents('.cart-item').attr('data-pk');
        let quantity = Number($(target).siblings('.item-quantity').text());
        quantity -= 1;
        if (quantity <= 0 ) {
            store.dispatch('removeFromCart', {pk: model});
        } else {
            store.dispatch('updateQuantity', {pk: model, quantity: quantity});
        }
    }

    incrementItem(target) {
        let parent = $(target).parents('.cart-item');
        let pk = parent.attr('data-pk');
        let quantity = Number($(target).siblings('.item-quantity').text());
        quantity += 1;
        store.dispatch('updateQuantity', {pk: pk, quantity: quantity});
    }

    clearCart() {
        store.dispatch('clearCart');
    }

    addToFavorites(payload) {
        favoritesStore.dispatch('addToFavorites', payload);
        toggleSidebarTab('#favorites');
    }

    processPromocode() {

    }

    recalculatePrice() {

    }

    render() {

        let cartIsEmpty = $('.cart-item').length === 0 ? true : false;

        if (store.state.cart.data['total_quantity'] === 0) {
            window.location.reload();
        } else if (cartIsEmpty) {
            window.location.reload();
        } else {
            this.renderItems();
            $('.cart-count').html(store.state.cart.data['total_quantity']);
            $('.cart-total__overall').find('.price').html(store.state.cart.data['total_price']);
            this._bindMethods();
        }

    }

    renderItems() {
        let self = this;
        let items = [];
        for (let key in store.state.cart.data.items) {
            items.push(store.state.cart.data.items[key]);
        }

        self.element.innerHTML = `
        ${items.map(item => {
            return `
            <li class="cart-item" data-pk=${item['pk']} id="cart-item-${item['pk']}">
                <div class="cart-item__img-wrap">
                    <img class="cart-item__img"
                        src="${item['image']}"
                        alt="${item['model']}"
                    >
                </div>
                <div class="cart-item__info">
                    <div class="cart-item__model">
                        ${item['model']}
                    </div>
                    <div class="cart-item__name">
                        <span class="cart-item__brand">
                            ${item['brand']}
                        </span>
                        <span class="cart-item__series">
                            ${item['series']}
                        </span>
                    </div>
                    <div class="cart-item__controls row">
                        <div class="quantity-controls row">
                            <div class="quantity-btn quantity_decrement cart-item__button">
                                -
                            </div>
                            <div class="item-quantity">
                                ${item['quantity']}
                            </div>
                            <div class="quantity-btn quantity_increment cart-item__button">
                                +
                            </div>
                        </div>
                        <div class="cart-item__subtotal">
                            <div class="cart-item__subtotal-quantity grey">
                            </div>
                            <div class="cart-item__subtotal-price bold">
                                <span class="price">
                                    ${item['base_price']}
                                </span>
                            </div>
                            <div class="cart-item-sale">
                            Скидка <span class="price">${item['sale']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="cart-item__favorite">
                        <i class="icon icon_favorite"></i>
                    </div>
                    <div class="cart-item__delete" data-pk=${item['pk']}>
                        <i class="icon icon_close">
                        </i>
                    </div>
                </div>
            </li>
            `
        }).join('')}`;

        // Добавление промежуточных итогов по количеству товаров
        for (let i=0; i<items.length; i++) {
            let item = items[i];
            let selector = `#cart-item-${item['pk']}`;
            let $element = $(selector);
            if (item['quantity'] > 1) {
                let html = `${item['quantity']} шт. × <span class="price price_9">${item['price']}</span>`;
                $element.find('.cart-item__subtotal-quantity').html(html);
            }
            if (item['sale'] > 0) {
                $element.find('.cart-item-sale').addClass('active');
            }
        }

        // Общая скидка
        let totalSale = store.state.cart.data['total_sale'];
        let $totalSaleElement = $('.cart-total-sale');
        if (totalSale > 0) {
            $totalSaleElement.find('.price').text(totalSale);
            $totalSaleElement.addClass('active');
        } else {
            $totalSaleElement.removeClass('active');
        }
    
    }

}