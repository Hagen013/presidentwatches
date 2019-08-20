import Vue from 'vue'

import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n
import { directive as onClickOutsideDirective } from 'vue-on-click-outside' 

Vue.use(ElementUI, { locale })
Vue.directive('on-click-outside', onClickOutsideDirective)
Vue.config.productionTip = false

export {Vue}
