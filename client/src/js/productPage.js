import store from './store/index.js';
import SidebarCart from './components/sidebarCart.js'


$(document).ready(function() {

    const sidebarCart = new SidebarCart();

    $('#add-to-cart').click(function() {
        store.dispatch('addToCart', PRODUCT);
    })
})
