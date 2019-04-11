import Component from '@/lib/component.js';
import store from '@/store/index.js';

export default class sidebarLastSeen extends Component {

    constructor() {
        super({
            store,
            element: document.getElementById('viewed')
        });
    }

    initialize() {
        this.bindMethods();
    }

    addItem(target) {
        let model = target.getAttribute('data-model');
        store.dispatch('addToCart', {model: model})
        $('.sidebar-link').each(function(index) {
            $(this).removeClass('active');
        })
        $(this).addClass('active');
        $('.sidebar-pane').each(function(index) {
            $(this).removeClass('active');
        });
        $('#cart').addClass('active');
        $('#sidebar-cart-link').addClass('active');
    }

    bindMethods() {
        let self = this;
        $(self.element).find('.card-mini-buy').click(function() {
            self.addItem(this);
        })
    }

    render() {
    }
};
