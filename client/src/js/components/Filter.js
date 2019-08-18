import store from '@/store/facetes/index.js'
import api from '@/api/index.js'

import Component from '@/lib/component.js'
import SimpleBar from 'simplebar'

import getRedirectionUrl from '@/utils/getRedirectionUrl'
import fuzzy from 'fuzzysearch'


export default class filter extends Component {

    constructor(element, selectionFunction) {
        super({
            store,
            element: element
        });
        if ( (selectionFunction === null) || (selectionFunction === undefined) ) {
            this.selectionFunction = this.getRedirectionCounts;
        } else {
            this.selectionFunction = selectionFunction;
        }
    }

    initialize() {
        this.bindMethods();
        this.key = this.element.getAttribute('data-key');
        this.$element = $(this.element);
        this.initialized = false;
        this.toggled  = false;

        if (store.state.facetes.active[this.key] !== undefined) {
            let count = this.$element.find('.round-count');
            count.text(store.state.facetes.active[this.key].length)
            count.css('display', 'inline-block');
        }
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
            if (!this.initialized) {
                self.getCounts();
            }
        }
    }

    getCounts() {
        let self = this;
        let params = {key: this.key};
        if (!this.toggled) {
            this.showPlaceholder();
        }
        for (let key in store.state.facetes.active) {
            params[key] = store.state.facetes.active[key].join(',')
        }
        api.get(`/search/facetes/`, {params: params})
            .then(response => {
                self.handleSuccessfulCountsResponse(response);
            })
            .catch(error => {
                console.log(error);
            })
    }

    getRedirectionCounts(element) {
        let self = this;
        let url = `/search/facetes/${this.key}/count/`;
        let params = {};
        for (let key in store.state.facetes.active) {
            params[key] = store.state.facetes.active[key].join(',')
        }
        api.get(url, {params: params})
            .then(response => {
                let count = response.data.hits.total;
                let url = getRedirectionUrl();

                $('.filter-result').remove();
                $('.catalog__filters').prepend(`
                <div class="filter-result">
                    <a href="${url}">
                    Найдено ${count} позиций
                    <div class="bold filter-result__watch">ПОКАЗАТЬ</div>
                    </a>
                </div>
                `)
                let offset = element.offset().top - $('.catalog__filters').offset().top - 8;
                $('.filter-result').css('top', offset);
            })
            .catch(error => {
                console.log(error);
            })
    }

    showPlaceholder() {
        let valuesList = this.element.querySelector('.filter-values-list');
        valuesList.innerHTML = `
        <div class="filter-placeholder">
            <img src="/static/assets/placeholder.svg">
        </div>
        `
    }

    handleSuccessfulCountsResponse(response) {
        let values = response.data.values;
        let counts = response.data.counts;
        let mapping = {};

        for (let i=0; i<counts.length; i++) {
            mapping[counts[i].key] = counts[i].doc_count; 
        }

        for (let z=0; z<values.length; z++) {
            let count = mapping[values[z].id];
            count = count === undefined ? 0 : count
            values[z].count = count;
        }
        this.values = values.sort( (a, b) => {
            return b.count - a.count
        })
        if (!this.toggled) {
            this.render();
        }
    }

    render() {

        let self = this;
        let valuesList = this.element.querySelector('.filter-values-list');
        let isScrollable = this.values.length > 8;
        if ( (this.values[0].value == true) || (this.values[0]).value == false ) {
            for (let i=0; i<this.values.length; i++) {
                this.values[i].value = this.values[i].value === true ? 'Да' : 'Нет';
            }
        }

        valuesList.innerHTML = `${this.values.map(value => {
            return `
            <li class="filter-value" data-id=${value.id}>
                <span class="filter-text">${value.value}</span>
                <span class="filter-count">
                ${value.count}
                </span>
            </li>
            `
        }).join('')}`;
        // Привязка активных значений
        let activeValues = store.state.facetes.active[this.key];
        if (activeValues !== undefined) {
            for (let i=0; i<activeValues.length; i++) {
                let selector = `*[data-id="${activeValues[i]}"]`;
                $(this.element).find(selector).addClass('active');
            }
        }
        $(valuesList).children('.filter-value').click(function() {
            let valueId = Number(this.getAttribute('data-id'));
            let button = $(this);
            button.toggleClass('active');
            if (button.hasClass('active')) {
                store.commit('addActiveOption', {key: self.key, value: valueId});
            } else {
                store.commit('removeActiveOption', {key: self.key, value: valueId});
            }
            self.selectionFunction(button);
        })
        // Если необходим scroll
        if ( (!this.toggled) && (isScrollable) ) {
            this.element.querySelector('.input filter-input')
            let simpa = new SimpleBar(valuesList, { autoHide: false });
            this.$element.find('.filter-input-box').removeClass('hidden');
            $('.filter-input').keyup(function() {
                let search = this.value.toLowerCase();
                let listValues = self.element.getElementsByClassName('filter-value');
                for (let i=0; i<listValues.length; i++) {
                    let value = listValues[i];
                    let target = value.childNodes[1].innerText.toLowerCase();
                    if (fuzzy(search, target)) {
                        $(value).removeClass('hidden');
                    } else {
                        $(value).addClass('hidden');
                    }
                }
            })
        }
        this.toggled = true;
    }
};
