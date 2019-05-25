import Vue from 'vue'

import navigation from './components/Navigation.vue'
import personalInfo from './components/PersonalInfo.vue'
import orders from './components/Orders.vue'
import promo from './components/Promo.vue'
import subscribes from './components/Subscribes.vue'

var profile = new Vue({
    name: 'profile',
    el: '#profile',
    components: {
        'navigation': navigation,
        'personal-info': personalInfo,
        'orders': orders,
        'promo': promo,
        'subscribes': subscribes
    },
    data: {
        activeOption: 'orders'
    },
    methods: {
        handleOptionChange(option) {
            this.activeOption = option;
        }
    }
});
