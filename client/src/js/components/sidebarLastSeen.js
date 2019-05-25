import Component from '@/lib/component.js';
import store from '@/store/index.js';
import toggleSidebarTab from '@/utils/toggleSidearTab'


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
        let pk = target.getAttribute('data-pk');
        store.dispatch('addToCart', {pk: pk})
        toggleSidebarTab('#cart');
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
