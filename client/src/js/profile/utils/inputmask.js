import Inputmask from 'inputmask'

var inputmaskPlugin = {
    install: function(Vue, options) {
        Vue.directive('mask', {
            bind: function(el, binding) {
                Inputmask(binding.value).mask(el);
            }
        });
    }
};

export default inputmaskPlugin