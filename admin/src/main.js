import {Vue} from '@/vue.js'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets
import 'element-ui/lib/theme-chalk/index.css'
import '@/styles/index.scss' // global css

import App from './App'
import router from './router'
import store from './store'

import './permission' // permission control

import '@/icons' // icon


new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
