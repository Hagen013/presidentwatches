import Inputmask from 'inputmask';
import api from '@/api'


export default class FastBuy {

    constructor() {
        this._bindMethods();
    }

    _bindMethods() {
        let self = this;
        let inputSelector = $('#call-modal-input');
        let im = new Inputmask(
            '+7 (999) 999-9999',
             {'placeholder': '+7 (___) ___-____' }
        );
        im.mask(inputSelector);

        $('#header-call').click(function() {
            self.showModal();
        })
        $('#call-modal').find('.modal-placeholder').click(function() {
            self.hideModal();
        })
        $('#call-close').click(function() {
            self.hideModal();
        })
        $('.call-close-btn').click(function() {
            self.hideModal();
        })
        $('#call-modal-submit').click(function() {
            let value = inputSelector.val().replace(/\(|\)|\-|\_/g, '').replace(/\s/g, '');
            if (value.length == 12) {
                self.hideError();
                let url = `/cart/call/`;
                let data = {
                    'phone': value,
                    'product': PRODUCT
                };

                api.post(url, data).then(
                    response => {

                        $('#call-main').html(
                            `
                            <div class="fast-buy-placeholder">
                                <p>
                                Заявка на обратный звонок принята.
                                </p>
                                <p>
                                В ближайшее время мы свяжемся с вами.
                                </p>
                            </div>
                            `
                        );
                        $('#call-modal-submit').css('display', 'none');
                        $('#call-close-btn').css('display', 'inline-block');
                    },
                    response => {
    
                    }
                )
            } else {
                self.showError();
            }
        })
    }

    showModal() {
        $('#call-modal').css('display', 'block');
    }

    hideModal() {
        $('#call-modal').css('display', 'none');
    }

    showError() {
        $('#call-modal-error').css('display', 'block');
    }

    hideError() {
        $('#call-modal-error').css('display', 'none');
    }

}