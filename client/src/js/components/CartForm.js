import store from '@/store/'


export default class CartForm {

    constructor() {
        this.$element = $('#cart-form');
        let self = this;
        store.events.subscribe('stateChange', () => self.recalculate());
    }

    _render() {

    }

    recalculate() {
        let total = 0;
        total += store.state.cart.data['total_price'];
        $('#cart-items-total').html(total);
        $('#cart-total').html(total);
    }

}