import { debounce } from 'debounce'

import api from '@/api/index.js'


export default class SearchBox {

    constructor(element) {
        let self = this;
        this.$element = $(element);
        this.$input = this.$element.children('input');
        this.itemsList = this.$element.children('ul');
        this.$parent = this.$element.parent();
        this.items = [];

        this.$input.on('input', function(e) {
            self.input(this.value);
        });

        this.triggerSearch = debounce(function(target) {
            api.get('/search/', {params: {line: target}} )
                .then(
                    response => {
                        self.items = response.data;
                        self.render();
                    },
                    response => {

                    }
                )
        }, 500);

        this.$input.on('focus', function(e) {
            if (self.items.length > 0) {
                self.$element.addClass('active');
            } else if (self.$input.val().length > 0) {
                self.triggerSearch(self.$input.val());
            }
        })

        $(document).mouseup(function (e) {
            let container = self.$element;
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                self.hide();
            }
        })

        this.$element.find('.icon_search').click(function() {
            self.$element.parent().submit();
        })

    }

    input(target) {
        let self = this;
        self.triggerSearch(target);
    }

    hide() {
        this.$element.removeClass('active');
    }

    render() {
        this.$element.addClass('active');
        let itemsList = `
        ${this.items.map(item => {
            return `
            <li class="search-item">
                <a href="${item._source.absolute_url}">
                    ${item._source.name}
                </a>
            </li>
            `
        }).join('')}`;
        this.itemsList.html(itemsList);
    }

    searchRedirect() {

    }

}