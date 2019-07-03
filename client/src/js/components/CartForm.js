import Inputmask from 'inputmask';

import store from '@/store/'
import api from '@/api'


function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

export default class CartForm {

    constructor() {
        this.$element = $('#cart-form');
        let self = this;
        let inputSelector = $('#cart-phone');

        store.events.subscribe('stateChange', () => self.recalculate());

        let im = new Inputmask(
            '+7 (999) 999-9999',
             {'placeholder': '+7 (___) ___-____' }
        );
        im.mask(inputSelector);

        this.orderData = {
            email: '',
            phone: '',
            name: '',
            location: {

            },
            delivery: '',
            address: '',
            notes: '',
            paymentType: '',
        }

        this._bindMethods();
    }

    _render() {

    }

    _bindMethods() {
        let self = this;

        $('#cart-submit').click(function() {
            self.submit();
        })

    }

    validateOrder() {

        let self = this;
        let phoneIsValid = false;

        // Проверка телефона
        let phoneValue = $('#cart-phone').val().replace(/\(|\)|\-|\_/g, '').replace(/\s/g, '');
        if ( phoneValue.length === 12 ) {
            phoneIsValid = true;
            self.removePhoneError();
            self.orderData.phone = phoneValue;
        } else {
            self.highlightPhoneError();
        }

        // Проверка E-mail
        let emailValue = $('#cart-email').val();
        if (validateEmail(emailValue)) {
            this.orderData.email = emailValue;
            this.removeEmailError();
        } else {
            this.highlightEmailError();
        }

        if ( phoneIsValid === true ) {
            return true
        }
        return false

    }

    highlightPhoneError() {
        $('#cart-phone').addClass('input_error');
        $('#cart-errors').text('Укажите номер телефона, включая код города (10 цифр)');
    }

    removePhoneError() {
        $('#cart-errors').text('');
        $('#cart-phone').removeClass('input_error');
    }

    highlightEmailError() {
        $('#cart-email').addClass('input_error');
    }

    removeEmailError() {
        $('#cart-email').removeClass('input_error');
    }

    submit() {
        let dataIsValid = this.validateOrder();
        if (dataIsValid == true) {
            this.processOrder();
        } else {

        }
    }

    processOrder() {
        let self = this;

        // Проверка E-mail для отправки в RetailRocket
        let email = $('#cart-email').val();
        (window["rrApiOnReady"] = window["rrApiOnReady"] || []).push(function() { rrApi.setEmail(email);});

        api.post('/cart/create-order/', this.orderData).then(
            response => {
                self.handleSuccessfulResponse(response);
            },
            response => {
                self.handleFailedResponse(response);
            }
        )
    }

    handleSuccessfulResponse(response) {
        let data = response.data;
        let url = `/cart/aftercheck/${data.uuid}/`
        window.location.href = url;
    }

    handleFailedResponse(response) {
        console.log("ERROR");
        console.log(response);
    }

    recalculate() {
        let total = 0;
        total += store.state.cart.data['total_price'];
        $('#cart-items-total').html(total);
        $('#cart-total').html(total);
    }

}