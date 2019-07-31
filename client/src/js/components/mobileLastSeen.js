import Component from '@/lib/component.js';
import store from '@/store/index.js';


export default class mobileLastSeen extends Component {

    constructor() {
        super({
            store,
            element: document.getElementById('last-seen-mobile')
        });
    }

    initialize() {
        console.log('init')
        this.bindMethods();
    }

    addItem(target) {
        let pk = target.getAttribute('data-pk');
        store.dispatch('addToCart', {pk: pk})
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
