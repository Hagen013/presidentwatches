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
            params[key] = store.state.facetes.active[key].join(',')
        }
        api.get(`/search/facetes/`, {params: params})
            .then(response => {
                self.handleSuccessfulCountsResponse(response);
            })
            .catch(error => {
            })
    }

    handleSuccessfulCountsResponse(response) {
        let mapping = {};
        let buckets = response.data.aggregations.facet.buckets;
        let values = $(this.element).find('.filter-value');
        console.log(values.length);

        for (let i=0; i<buckets.length; i++) {
            mapping[buckets[i]['key']] = buckets[i]['doc_count'];
        }
        for (let c=0; c<values.length; c++) {
            let id = Number(values[c].getAttribute('data-id'));
            let count = mapping[id];
            let countEl = values[c].querySelector('.filter-count');

            count = count == undefined ? 0 : count;
            $(countEl).text(count);
        }
        let sortedValues = $(values).sort(function(a, b) {
            let aVal = Number($(a).find('.filter-count').text());
            let bVal = Number($(b).find('.filter-count').text());
            return bVal - aVal
        })

        for (let i=0; i<sortedValues.length; i++) {
            let t = $(sortedValues[i].querySelector('.filter-count')).text();
        }
        $(this.element).find('ul').html(sortedValues);
    }

    handleClick() {

    }

    render() {
    }
};
