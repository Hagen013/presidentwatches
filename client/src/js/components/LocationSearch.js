import { debounce } from 'debounce'
import Cookies from 'js-cookie'

import store from '@/store/index'
import geoApi from '@/api/geo'


export default class LocationSearch {
   
    constructor() {

        let self = this;
        this.$buttons = $('.city-choice');
        this.$wrap = $('.location-modal');
        this.$placeholder = this.$wrap.find('.modal-placeholder');
        this.$closeButton = this.$wrap.find('.modal-close');
        this.$input = this.$wrap.find('input')
        this.$searchList = this.$wrap.find('ul.search-list');
        this.items = [];

        this.triggerSearch = debounce(function(target) {
            let url = `/api/kladr/search/${target}`
            geoApi.get(url).then(
                response => {
                    this.items = response.data;
                    self.renderCityList();
                },
                response => {

                }
            )
        }, 500);

        this.$buttons.click(function() {
            self.showModal();
        })
        this.$placeholder.click(function() {
            self.hideModal();
        })
        this.$closeButton.click(function() {
            self.hideModal();
        })
        this.$input.on('input', function(e) {
            if (this.value.length > 0) {
                self.triggerSearch(this.value);
            }
        });
        this.$wrap.find('.location-link').click(function() {
            let code = this.getAttribute('data-code');
            let name = this.innerText;
            let params = {code: code, name: name};
            self.changeLocation(params);
        })
        this.$input.on('focus', function(e) {
            if (self.items.length > 0) {
                self.$wrap.find('.input-box').addClass('active');
            }
        })
        $(document).mouseup(function (e) {
            let container = self.$wrap.find('.input-box');
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                self.$wrap.find('.input-box').removeClass('active');
            }
        })
    }

    showModal() {
        if (this.$modal === undefined) {
            this.$modal = $('#location-modal');
        }
        this.$modal.css('display', 'flex');
    }


    hideModal() {
        if (this.$modal === undefined) {
            this.$modal = $('#location-modal');
        }
        this.$modal.css('display', 'none');
        this.$wrap.find('.input-box').removeClass('active');
    }

    changeLocation(payload) {
        console.log(payload);
        Cookies.set('city_name', payload.name);
        Cookies.set('city_code', payload.code);
        this.hideModal();
        $('.city-name').text(payload.name);
    }
    
    renderCityList() {
        let self = this;
        let html = `
        ${this.items.map(item => {
            return `
            <li class="search-item" data-code="${item.code}" data-name="${item.name}">
                <a>
                    ${item.full_name}
                </a>
            </li>
            `
        }).join('')}`;
        this.$searchList.html(html);
        this.$wrap.find('.input-box').addClass('active');
        this.$searchList.find('.search-item').click(function() {
            let code = this.getAttribute('data-code');
            let name = this.getAttribute('data-name');
            let params = {code: code, name: name};
            self.changeLocation(params);
        })
        if (this.$searchList.innerHeight() > this.$searchList.parent().height()) {
            this.$searchList.css('overlay-y', 'scroll');
        } else {
            this.$searchList.css('overlay-y', 'hidden');
        }

        if (this.$searchList.innerHeight() > 255) {
            this.$searchList.css('overflow-y', 'scroll');
        } else {
            this.$searchList.css('overflow-y', 'hidden');
        }

    }

}
