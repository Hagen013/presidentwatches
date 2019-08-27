import Cookies from 'js-cookie'

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

                let admitadCookie = getCookie('tagtag_aid');
                if ( admitadCookie !== undefined ) {
                    data['cpa'] = {'networks': ['admitad']};
                }

                api.post(url, data).then(
                    response => {

                        // RetailRocket
                        let transactionId = response.data.public_id;
                        let data = response.data.cart.items
                        let items = [];
                        for (let key in data) {
                            let item = data[key];

                            items.push({
                                'id': item.pk,
                                'qnt': item.quantity,
                                'price': item.price
                            })
                        }

                        (window["rrApiOnReady"] = window["rrApiOnReady"] || []).push(function() {
                            try { 
                            rrApi.order({
                                transaction: transactionId,
                                items: items
                            });
                            } catch(e) {} 
                        })
                        // RetailRocket end


                        // Admitad
                        let admitadCookie = Cookies.get('tagtag_aid');
                        
                        if (admitadCookie !== undefined) {
                            ADMITAD = window.ADMITAD || {};
                            ADMITAD.Invoice = ADMITAD.Invoice || {};
                            ADMITAD.Invoice.broker = "adm";     // параметр дедупликации (по умолчанию для admitad)
                            ADMITAD.Invoice.category = "1";
                            ADMITAD.Invoice.referencesOrder = ADMITAD.Invoice.referencesOrder || [];
                    
                            let admitadItems = [];
                            for (let key in data) {
                                let item = data[key];
                                admitadItems.push({
                                    Product: {
                                        productID: String(item.pk),
                                        category: '1',
                                        price: item.price,
                                        priceCurrency: 'RUB'
                                    },
                                    orderQuantity: item.quantity,
                                    additionalType: 'sale'
                                })
                            }
                            ADMITAD.Invoice.referencesOrder.push({
                                orderNumber: transactionId,
                                orderedItem: admitadItems
                            });
                            ADMITAD.Tracking.processPositions();
                        }
                        // Admitad End


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
        try { rrApi.addToBasket(`${PRODUCT.pk}`) } catch(e) {}
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