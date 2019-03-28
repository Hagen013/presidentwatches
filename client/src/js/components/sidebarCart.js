import Component from '../lib/component.js';
import store from '../store/index.js';

export default class sidebarCart extends Component {

    constructor() {
        super({
            store,
            element: document.getElementById('sidebar-cart-items')
        });
    }

    render() {
        console.log('rendering')
        let self = this;
        console.log(store.state.cart.data.items)
        let items = [];
        for (let key in store.state.cart.data.items) {
            items.push(store.state.cart.data.items[key]);
        }
        console.log(items);

        self.element.innerHTML = `
        ${items.map(item => {
            return `
            <li class='card-mini sidebar-card'>
                <div class="card-mini__img-wrap">
                    <img class='card-mini__img' src='${item['image']}'>
                </div>
            </li>
            `
        }).join('')}`;
    }
};
