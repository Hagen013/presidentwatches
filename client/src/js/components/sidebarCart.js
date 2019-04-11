import Component from '@/lib/component.js';
import store from '@/store/index.js';

export default class sidebarCart extends Component {

    constructor() {
        super({
            store,
            element: document.getElementById('sidebar-cart-items')
        });
    }

    initialize() {
        this.bindMethods();
    }

    removeItem(target) {
        let model = target.parentNode.getAttribute('data-model');
        store.dispatch('removeFromCart', {model: model});
    }

    decrementItem(target) {
        let model = $(target).parents('.card-mini').attr('data-model');
        let quantity = Number($(target).siblings('.item-quantity').text());
        quantity -= 1;
        console.log(quantity)
        if (quantity <= 0 ) {
            store.dispatch('removeFromCart', {model: model});
        } else {
            store.dispatch('updateQuantity', {model: model, quantity: quantity});
        }
    }

    incrementItem(target) {
        let model = $(target).parents('.card-mini').attr('data-model');
        let quantity = Number($(target).siblings('.item-quantity').text());
        quantity += 1;
        store.dispatch('updateQuantity', {model: model, quantity: quantity});
    }

    clearCart() {
        store.dispatch('clearCart');
    }

    bindMethods() {
        let self = this;
        $('.card-mini__delete').click(function(e) {
            self.removeItem(this);
        })
        $('.quantity_decrement').click(function(e) {
            self.decrementItem(this);
        })
        $('.quantity_increment').click(function(e) {
            self.incrementItem(this);
        })
        $('#sidebar-cart-clear').click(function(e) {
            self.clearCart();
        })
    }

    render() {
        let self = this;
        let items = [];
        for (let key in store.state.cart.data.items) {
            items.push(store.state.cart.data.items[key]);
        }

        self.element.innerHTML = `
        ${items.map(item => {
            return `
            <li class='card-mini sidebar-card' data-model='${item['model']}'>
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
                            <span class="price">${item['total_price']}</span>
                        </div>
                    </div>
                </div>
                <div class="card-mini__delete">
                    <i class="icon icon_close">
                    </i>
                </div>
                <div class="card-mini__favorite like">
                    <i class="icon icon-like">
                    </i>
                </div>
            </li>
            `
        }).join('')}`;

        $('#sidebar-total-price').text(store.state.cart.data.total_price);
        $('.cart-count').text(store.state.cart.data.total_quantity);
        self.bindMethods()
    }
};
