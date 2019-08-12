import Vue from 'vue'

import Vuex from 'vuex'
import VueRouter from 'vue-router'
import store from '@/profile/store/index.js'

import VueInputMask from './utils/inputmask.js'

Vue.use(VueInputMask);
Vue.use(VueRouter);
Vue.use(Vuex);

import app from './app.vue'


var profile = new Vue({
    name: 'profile',
    el: '#profile',
    store,
    components: {
        'app': app,
    },
    data: {
    },
    methods: {
    }
});
