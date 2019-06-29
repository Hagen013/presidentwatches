import Inputmask from 'inputmask';
import api from '@/api'


export default class FastBuy {

    constructor() {
        this._bindMethods();
    }

    _bindMethods() {
        let self = this;
        let inputSelector = $('#fast-buy-input');
        let im = new Inputmask(
            '+7 (999) 999-9999',
             {'placeholder': '+7 (___) ___-____' }
        );
        im.mask(inputSelector);

        $('#fast-buy').click(function() {
            self.showModal();
        })
        $('#fast-buy-modal').find('.modal-placeholder').click(function() {
            self.hideModal();
        })
        $('#fast-buy-close').click(function() {
            self.hideModal();
        })
        $('.fast-buy-close-btn').click(function() {
            self.hideModal();
        })
        $('#fast-buy-submit').click(function() {
            let value = inputSelector.val().replace(/\(|\)|\-|\_/g, '').replace(/\s/g, '');
            if (value.length == 12) {
                self.hideError();
                let data = {
                    'product': PRODUCT,
                    'phone': value
                }
                let url = `/cart/fast-buy/${PRODUCT.pk}/`;
                api.post(url, data).then(
                    response => {
                        $('.fast-buy-main').html(
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
                        $('#fast-buy-submit').css('display', 'none');
                        $('.fast-buy-close-btn').css('display', 'inline-block');
                        try { rrApi.addToBasket(`${PRODUCT.pk}`) } catch(e) {}
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
        $('#fast-buy-modal').css('display', 'block');
    }

    hideModal() {
        $('#fast-buy-modal').css('display', 'none');
    }

    showError() {
        $('#fast-buy-error').css('display', 'block');
    }

    hideError() {
        $('#fast-buy-error').css('display', 'none');
    }

}