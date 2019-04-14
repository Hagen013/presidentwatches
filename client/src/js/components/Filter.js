import store from '@/store/index.js';
import api from '@/api/index.js'

import Component from '@/lib/component.js';


export default class filter extends Component {

    constructor(element) {
        super({
            store,
            element: element
        });
    }

    initialize() {
        this.bindMethods();
        this.key = this.element.getAttribute('data-key');
    }

    bindMethods() {
        let self = this;
        let heading = $(this.element).children('.filter-heading');
        $(heading).click(function(e) {
            self.togglePanel();
        })
    }

    togglePanel() {
        let self = this;
        $(this.element).toggleClass('active');
        if ( $(this.element).hasClass('active') ) {
            self.getCounts();
        }
    }

    getCounts() {
        let self = this;
        let params = {key: this.key};
        for (let key in store.state.facetes.active) {
            console.log(key)
            params[key] = store.state.facetes.active[key].join(',')
        }
        console.log('');
        console.log(params);
        console.log('');
        api.get(`/search/facetes/`, {params: params})
            .then(response => {
                self.handleSuccessfulCountsResponse(response);
            })
            .catch(error => {
                console.log(error);
            })
    }

    handleSuccessfulCountsResponse(response) {
        console.log(response);
    }

    render() {
    }
};
