import Vue from 'vue'

import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/ru-RU' // lang i18n
import { directive as onClickOutside } from 'vue-on-click-outside' 


Vue.use(ElementUI, { locale })
Vue.directive('on-click-outside', onClickOutside)
Vue.config.productionTip = false

export {Vue}
