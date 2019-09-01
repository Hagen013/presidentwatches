import Cookies from 'js-cookie'

import Inputmask from 'inputmask';

import store from '@/store/'
import locationStore from '@/store/location/index'
import api from '@/api'
import geoApi from '@/api/geo'
import message from '@/lib/message'
import { priceFilter, timeFilter } from '@/utils/filters'


function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

export default class CartForm {

    constructor() {
        this.$element = $('#cart-form');
        let self = this;
        let inputSelector = $('#cart-phone');

        this.locationLoading = false;
        this.coordinatesOutdated = true;
        this.coordinates = [];

        store.events.subscribe('stateChange', () => self.recalculate());
        locationStore.events.subscribe('stateChange', () => self.changeLocation());

        let im = new Inputmask(
            '+7 (999) 999-9999',
             {'placeholder': '+7 (___) ___-____' }
        );
        im.mask(inputSelector);

        this.orderData = {
            customer: {
                email: '',
                phone: '',
                name: '',
                address: ''
            },
            delivery: {
                type: 'not_seslected',
                price: 0,
                pvz_code: null,
                pvz_service: null,
                pvz_address: null
            },
            payment: {
                type: 'not_selected'
            },
            client_notes: '',
            source: 2
        }

        let value = $('input[type=radio][name=delivery]:checked').val();
        let price = parseInt($('#delivery-price-sum').text());

        this.orderData.delivery.price = price;

        if (value !== undefined) {
            this.orderData.delivery.type = value;
        }


        this.deliveryData = {
            points: []
        }

        this.cityName = $('#cart-city').text();
        this.products = PRODUCTS.replace(/&#34;/g, '"');
        this.products = JSON.parse(this.products);
        this.getDeliveryData();
        this._bindMethods();
    }

    _render() {

    }

    _bindMethods() {
        let self = this;

        $('#cart-submit').click(function() {
            self.submit();
        })

        this._bindDeliveryOptionsChange();

        let paymentOptions = $('input[type=radio][name=payment]');

        paymentOptions.on('change', function() {
            switch ($(this).val()) {
                case 'cash':
                    self.orderData.payment.type = 'cash';
                    break
                case 'card_offline':
                    self.orderData.payment.type = 'card_offline';
                    break
                case 'card_online':
                    self.orderData.payment.type = 'card_online'
                    break
            }
        })

        let pickupModal = $('#pickup-modal')

        pickupModal.find('.modal-placeholder').click(function() {
            self.hideModal();
        });

        pickupModal.find('.modal-close').click(function() {
            self.hideModal();
        });

        $('#cart-promocode-submit').click(function() {
            let value = $('#cart-promocode').val().toUpperCase();
            api.get(`/cart/promocode/`, {params: {name: value}}).then(
                response => {
                    store.commit('updateCart', response.data)
                    api.get('/promocodes/search/', {params: {name: value}}).then(
                        res => {
                            $('#sidebar-old-price').addClass('active');
                            message({
                                type: 'success',
                                title: 'Промокод применен',
                                text: res.data.description + `<p class="bold message-sale">Ваша скидка: <span class="price">${store.state.cart.data.total_sale}</span><p>`,
                                link: '<a class="message-btn message-btn-1" href="/info/promo/">ВСЕ ПРОМОКОДЫ</a>'
                            })
                        },
                        res => {

                        }
                    )
                },
                response => {
                    message({
                        'type': 'error',
                        'title': 'Промокод не найден',
                        'text': '',
                        'link': '<a class="message-btn message-btn-1" href="/info/promo/">ВСЕ ПРОМОКОДЫ</a>'
                    })
                }
            )
        })
    }

    _bindDeliveryOptionsChange() {
        let self = this;
        let deliveryOptions = $('input[type=radio][name=delivery]');

        deliveryOptions.on('change', function() {
            switch ($(this).val()) {
                case 'curier':
                    self.setDeliveryTypeCurier();
                    break
                case 'delivery_point':
                    self.setDeliveryTypeDeliveryPoint();
                    break
                case 'post':
                    self.setDeliveryTypeRupost()
                    break
                case 'pickup':
                    self.setDeliveryTypePickup()
                    break
            }
        })
    }

    ymapsInitialize(self) {
        return function() {
            

            if (self.map !== undefined) {
                self.map.destroy()
            }

            self.map=new ymaps.Map(self.$map.get(0), {
                center: self.coordinates,
                zoom: 11,
                behaviors: ['default', 'scrollZoom'],
                controls: ['zoomControl', 'fullscreenControl', 'searchControl']
            });

            let collection = [];

            for (let i=0; i<self.deliveryData.points.sdek_points.length; i++) {
                let point = self.deliveryData.points.sdek_points[i];
                let marker = new ymaps.Placemark(
                    [point.latitude, point.longitude],
                    {
                        hintContent: point.address,
                        balloonContentHeader: `
                        <h2 class="bold">Пункт выдачи СДЭК</h2><br/>
                        `,
                        balloonContentBody:
                        `
                        <span class="bold">Адрес:</span>${point.address}<br/>
                        <span class="bold">Срок поставки:</span>${timeFilter(point.time_min, point.time_max)}<br/>
                        <span class="bold">Стоимость:</span>${priceFilter(point.price)}<br/><br/>
                        `,
                        balloonContentFooter: `
                        <button 
                            id="js-balloone-btn"
                            data-code="${point.code}"
                            data-type="sdek"
                            data-address="${point.address}"
                            data-price="${point.price}"
                            class="button button_accent"
                            style="padding:0px 20px"
                        >  
                            ВЫБРАТЬ ПУНКТ
                        </button>
                    `,
                    clusterCaption: "СДЕК",
                    },
                    {
                        balloonContentLayout: self.getBalloonContentLayout(),
                        iconColor: "#00a16d",
                        zIndex: 10000
                    }
                )
                collection.push(marker);
            }

            for (let i=0; i<self.deliveryData.points.pick_point_points.length; i++) {
                let point = self.deliveryData.points.pick_point_points[i];
                let marker = new ymaps.Placemark(
                    [point.latitude, point.longitude],
                    {
                        hintContent: point.address,
                        balloonContentHeader: `
                        <h2 class="bold">Пункт выдачи PickPoint</h2><br/>
                        `,
                        balloonContentBody:
                        `
                        <span class="bold">Адрес:</span>${point.address}<br/>
                        <span class="bold">Срок поставки:</span>${timeFilter(point.time_min, point.time_max)}<br/>
                        <span class="bold">Стоимость:</span>${priceFilter(point.price)}<br/><br/>
                        `,
                        balloonContentFooter: `
                        <button 
                            id="js-balloone-btn"
                            data-code="${point.code}"
                            data-type="pickpoint"
                            data-address="${point.address}"
                            data-price="${point.price}"
                            class="button button_accent"
                            style="padding:0px 20px"
                        >  
                            ВЫБРАТЬ ПУНКТ
                        </button>
                    `,
                    clusterCaption: "PickPoint",
                    },
                    {
                        balloonContentLayout: self.getBalloonContentLayout(),
                        iconColor: "#f68e56",
                        zIndex: 10000
                    }
                )
                collection.push(marker);
            }

            let clusterer = new ymaps.Clusterer({
                preset: 'islands#invertedVioletClusterIcons',
                clusterIconLayout: 'default#pieChart',
                clusterBalloonItemContentLayout: self.getBalloonContentLayout(),
                clusterDisableClickZoom: false
            });

            clusterer.add(collection);
            self.map.geoObjects.add(clusterer);


            self.hideLoader();
            self.showModal();
        }
    }

    getBalloonContentLayout() {
        let self = this;
        return ymaps.templateLayoutFactory.createClass(
            '<div style="padding: 4px">' +
            '<p>$[properties.balloonContentHeader]</p>' +
            '<p>$[properties.balloonContentBody]</p>' +
            '<p>$[properties.balloonContentFooter]</p>' +
            '</div>',
            {
              build: function(){
                this.constructor.superclass.build.call(this);
                let btn = document.getElementById(`js-balloone-btn`)
                btn.addEventListener("click", function () {
                    let type = btn.getAttribute('data-type');
                    let code = btn.getAttribute('data-code');
                    let address = btn.getAttribute('data-address');
                    let price = parseInt(btn.getAttribute('data-price'));
                    let payload = {
                        type: type,
                        code: code,
                        address: address,
                        price: price
                    }
                    self.setDeliveryPoint(payload);
                    self.map.balloon.close();
                    self.map.container.exitFullscreen();
                    self.hideModal();
                });
              }
            });
    }

    setDeliveryPoint(payload) {
        let type = {'sdek': 'СДЭК', 'pickpoint': 'ПикПоинт'}[payload.type];
        let address = `Пункт ${type}, ${payload.address}`;

        this.orderData.delivery.pvz_code = payload.code;
        this.orderData.delivery.pvz_service = payload.type;
        this.orderData.delivery.pvz_address = payload.address;
        this.orderData.delivery.type = 'pvz';
        this.orderData.delivery.price = payload.price;
        this.deliveryData.delivery_point.price = payload.price;

        $('#delivery-price-sum').text(
            payload.price
        )

        $('#delivery-point-address').text(
            address
        )
        this.recalculate();
    }

    setDeliveryTypeCurier() {

        this.orderData.delivery.pvz_code = null;
        this.orderData.delivery.pvz_service = null;
        this.orderData.delivery.pvz_address = null;
        this.orderData.delivery.type = 'curier';
        this.orderData.delivery.price = this.deliveryData.curier.price;
        this.orderData.client_notes = $('#client-notes').val();

        $('#delivery-price-sum').text(
            this.deliveryData.curier.price
        )
        $('.delivery-options-outlet').html(
            `
            <div class="field cart-field">
                <div class="field-title">
                    Адрес
                </div>
                <div class="field-input-box">
                    <input class="input" id="cart-address">
                </div>
            </div>
            <div class="field cart-field">
                <div class="field-title">
                    Пожелания
                </div>
                <div class="field-input-box">
                    <input class="input" value="${this.orderData.client_notes}" id="client-notes">
                </div>
            </div>
            `
        )
        this.recalculate();
    }

    setDeliveryTypePickup() {

        this.orderData.delivery.pvz_code = null;
        this.orderData.delivery.pvz_service = null;
        this.orderData.delivery.pvz_address = null;
        this.orderData.delivery.type = 'pickup';
        this.orderData.delivery.price = 0;
        this.orderData.client_notes = $('#client-notes').val()

        $('#delivery-price-sum').text(
            0
        )
        $('.delivery-options-outlet').html(
            `
            <div class="field cart-field">
                <div class="field-title">
                    Адрес магазина
                </div>
                <div class="field cart-field">
                    <div class="cart-address-placeholder disabled">
                    Торговый центр "РоллХолл" Холодильный переулок, 3, Ряд 4, Бутик 79-80 
                    </div>
                </div>
            </div>
            <div class="field cart-field">
                <div class="field-title">
                    Пожелания
                </div>
                <div class="field-input-box">
                    <input class="input" value="${this.orderData.client_notes}" id="client-notes">
                </div>
            </div>
            `
        )
        this.recalculate()
    }

    setDeliveryTypeRupost() {

        this.orderData.delivery.pvz_code = null;
        this.orderData.delivery.pvz_service = null;
        this.orderData.delivery.pvz_address = null;
        this.orderData.delivery.type = 'rupost';
        this.orderData.delivery.price = this.deliveryData.postal_service.price;
        this.orderData.client_notes = $('#client-notes').val()

        $('#delivery-price-sum').text(
            this.deliveryData.postal_service.price
        )
        $('.delivery-options-outlet').html(
            `
            <div class="field cart-field">
                <div class="field-title">
                    Адрес
                </div>
                <div class="field-input-box">
                    <input class="input" id="cart-address">
                </div>
            </div>
            <div class="field cart-field">
                <div class="field-title">
                    Пожелания
                </div>
                <div class="field-input-box">
                    <input class="input" value="${this.orderData.client_notes}" id="client-notes">
                </div>
            </div>
            `
        )
        this.recalculate();
    }

    setDeliveryTypeDeliveryPoint() {
        let self = this;
        let cityName = $('#cart-city').text();
        this.$map = $('#ymaps-map');

        this.orderData.delivery.pvz_code = '';
        this.orderData.delivery.pvz_service = '';
        this.orderData.delivery.pvz_address = '';
        this.orderData.delivery.type = 'pvz';
        this.orderData.client_notes = $('#client-notes').val()

        self.showLoader();
        $.getScript('https://api-maps.yandex.ru/2.1/?lang=ru-RU', function() {
            if ( (self.coordinatesOutdated) || (self.coordinates.length == 0) ) {
                self.getCoordinates().then(() => {
                    ymaps.ready(self.ymapsInitialize(self));
                })
            } else {
                ymaps.ready(self.ymapsInitialize(self));
            }
        });

        $('#delivery-price-sum').text(
            0
        )

        $('.delivery-options-outlet').html(
            `
            <div class="field cart-field">
                <div class="field-title">
                    Адрес пункта выдачи
                </div>
                <div class="field-input-box">
                    <div class="cart-address-placeholder" id="delivery-point-address">
                    Выбрать пункт выдачи
                    </div>
                </div>
            </div>
            <div class="field cart-field">
                <div class="field-title">
                    Пожелания
                </div>
                <div class="field-input-box">
                    <input class="input" value="${this.orderData.client_notes}" id="client-notes">
                </div>
            </div>
            `
        )

        $('#delivery-point-address').click(function(){
            self.showModal();
        })
        this.recalculate()
    }

    getDeliveryData() {
        let self = this;
        let kladr = Cookies.get('city_code');
        let products = this.products;

        if (store.state.cart.total_price !== undefined) {
            products = [];
            for (let key in store.state.cart.items) {
                let item = store.state.cart.items[key];
                products.push({
                    price: item.price,
                    purchase_price: item.price,
                    vendor: item.brand,
                    product_type: 'CUBE'
                })
            }
        }

        let data =  {
            'kladr': kladr,
            'products': this.products
        }

        geoApi.post('/api/delivery/meny_products/', data).then(
            response => {
                self.handleSuccessfulGeoResponse(response);
            },
            response => {
                self.hanldeFailedGeoResponse(response);
            }
        )

    }

    handleSuccessfulGeoResponse(response) {
        this.deliveryData = response.data;
        if (this.locationLoading) {
            this.hideLoader();
            this.updateDeliveryOptions();
        }
        this.locationLoading = false;
    }

    hanldeFailedGeoResponse(response) {
        if (this.locationLoading) {
            this.hideLoader();
        }
        this.locationLoading = false;
    }

    showModal() {
        $('#pickup-modal').css('display', 'block');
    }

    hideModal() {
        $('#pickup-modal').css('display', 'none');
    }

    showLoader() {
        $('#loader-modal').css('display', 'block');
    }

    hideLoader() {
        $('#loader-modal').css('display', 'none');
    }

    validateOrder() {

        let self = this;
        let phoneIsValid = false;

        // Проверка телефона
        let phoneValue = $('#cart-phone').val().replace(/\(|\)|\-|\_/g, '').replace(/\s/g, '');
        if ( phoneValue.length === 12 ) {
            phoneIsValid = true;
            self.removePhoneError();
            self.orderData.customer.phone = phoneValue;
        } else {
            self.highlightPhoneError();
        }

        // Проверка E-mail
        let emailValue = $('#cart-email').val();
        if (validateEmail(emailValue)) {
            this.orderData.customer.email = emailValue;
            (window["rrApiOnReady"] = window["rrApiOnReady"] || []).push(function() { rrApi.setEmail(emailValue);});
            this.removeEmailError();
        } else {
            this.highlightEmailError();
        }

        // Сохранение имени
        let name = $('#cart-name').val();
        let address = $('#cart-address').val();
        let notes = $('#client-notes').val();

        if (address == undefined) {
            address = '';
        }

        this.orderData.customer.name = name;
        this.orderData.customer.address = address;
        this.orderData.client_notes = notes;

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

        let admitadCookie = Cookies.get('tagtag_aid');
        if ( admitadCookie !== undefined ) {
            this.orderData['cpa'] = {'networks': ['admitad']};
        }

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

    }

    recalculate() {
        let total = 0;

        let map = {
            'pvz': 'delivery_point',
            'curier': 'curier',
            'rupost': 'postal_service'
        }
        
        let deliveryType = this.orderData.delivery.type;
        let deliveryPrice = 0;

        if ( (deliveryType !== 'not_selected') && (deliveryType !== 'pickup') ) {
            deliveryType = map[deliveryType];
            deliveryPrice = this.deliveryData[deliveryType]['price'];
        }
        $('#delivery-price-sum').text(deliveryPrice);

        let productsPrice = 0;

        if (store.state.cart.data !== undefined) {
            productsPrice = store.state.cart.data['total_price'];
        } else {
            productsPrice = parseInt($('#cart-items-total').text());
        }

        total += productsPrice;
        total += deliveryPrice;
        total = Math.floor(total);
        $('#cart-items-total').text(productsPrice);
        $('#cart-total').text(total);
    }

    changeLocation() {
        this.cityName = locationStore.state.location.city_name;
        $('#cart-city').text(this.cityName);
        this.locationLoading = true;
        this.showLoader();
        this.getDeliveryData();
        this.coordinatesOutdated = true;
        this.recalculate()
    }

    getCoordinates() {
        let kladr = Cookies.get('city_code');
        return new Promise((resolve, reject) => {
            geoApi.get('/api/geo_ip/coordinates/', {params: {kladr_code: kladr}}).then(
                response => {
                    this.coordinates = [
                        response.data.latitude,
                        response.data.longitude
                    ];
                    resolve();
                },
                response => {
                    reject();
                }
            )
        })
    }

    updateDeliveryOptions() {
        let self = this;
        let deliveryOptions = $('.cart-delivery-options');
        let deliveryOptionsTemplate = '';

        if (this.cityName === 'Москва') {
            deliveryOptionsTemplate = `
            <li class="radio-group-container">
                <input type="radio"
                    id="radio-1" 
                    name="delivery" 
                    value="curier"
                    checked
                />
                <label for="radio-1" class="flex-column">
                    <div class="rarefied">
                        КУРЬЕРОМ
                    </div>
                    <div class="grey">
                        ${timeFilter(self.deliveryData['curier']['time_min'], self.deliveryData['curier']['time_max'])}
                    </div>
                </label>
            </li>
            <li class="radio-group-container">
                <input type="radio"
                    id="radio-2" 
                    name="delivery" 
                    value="delivery_point"/>
                <label for="radio-2" class="flex-column">
                    <div class="rarefied">
                        ИЗ ПУНКТА ВЫДАЧИ
                    </div>
                    <div class="grey">
                        ${timeFilter(self.deliveryData['delivery_point']['time_min'], self.deliveryData['delivery_point']['time_max'])}
                    </div>
                </label>
            </li>
            <li class="radio-group-container">
                <input type="radio"
                    id="radio-3" 
                    name="delivery" 
                    value="pickup"/>
                <label for="radio-3" class="flex-column">
                    <div class="rarefied">
                        САМОВЫВОЗ
                    </div>
                    <div class="grey">
                    завтра/послезавтра
                    </div>
                </label>
            </li>
            `
        } else {

            let curierIsAvailable = false;
            let deliverPointIsAvailable = false;

            // Проверка на доступность курьерской службы
            if (this.deliveryData['curier'] !== null) {
                this.orderData.delivery.type = 'curier';
                curierIsAvailable = true;
                deliveryOptionsTemplate += `
                <li class="radio-group-container">
                    <input type="radio"
                        id="radio-1" 
                        name="delivery" 
                        value="curier"
                        checked
                    />
                    <label for="radio-1" class="flex-column">
                        <div class="rarefied">
                            КУРЬЕРОМ
                        </div>
                        <div class="grey">
                            ${timeFilter(self.deliveryData['curier']['time_min'], self.deliveryData['curier']['time_max'])}
                        </div>
                    </label>
                </li>
                `
            } else {
                deliveryOptionsTemplate += `
                <li class="radio-group-container">
                    <input type="radio"
                        id="radio-1" 
                        name="delivery" 
                        value="curier"
                        disabled
                    />
                    <label for="radio-1" class="flex-column">
                        <div class="rarefied">
                            КУРЬЕРОМ
                        </div>
                        <div class="red">
                            недоступно
                        </div>
                    </label>
                </li>
                `
            }

            // Проверка на доступность точек доставки
            if (this.deliveryData['delivery_point'] !== null) {
                deliverPointIsAvailable = true;
                deliveryOptionsTemplate += `
                <li class="radio-group-container">
                    <input type="radio"
                        id="radio-2" 
                        name="delivery" 
                        value="delivery_point"
                    />
                    <label for="radio-2" class="flex-column">
                        <div class="rarefied">
                            ИЗ ПУНКТА ВЫДАЧИ
                        </div>
                        <div class="grey">
                            ${timeFilter(self.deliveryData['delivery_point']['time_min'], self.deliveryData['delivery_point']['time_max'])}
                        </div>
                    </label>
                </li>
                `
            } else {
                deliveryOptionsTemplate += `
                <li class="radio-group-container">
                    <input type="radio"
                        id="radio-2" 
                        name="delivery" 
                        value="delivery_point"
                        disabled
                    />
                    <label for="radio-2" class="flex-column">
                        <div class="rarefied">
                            ИЗ ПУНКТА ВЫДАЧИ
                        </div>
                        <div class="red">
                            недоступно
                        </div>
                    </label>
                </li>
                `
            }

            if (!curierIsAvailable) {
                this.orderData.delivery.type = 'rupost';
                deliveryOptionsTemplate += `
                <li class="radio-group-container">
                    <input type="radio"
                        id="radio-3" 
                        name="delivery" 
                        value="post"
                        checked
                    />
                    <label for="radio-3" class="flex-column">
                        <div class="rarefied">
                            ПОЧТОЙ
                        </div>
                        <div class="grey">
                            от 5 до 7 дней
                        </div>
                    </label>
                </li>
                `
            } else {
                deliveryOptionsTemplate += `
                <li class="radio-group-container">
                    <input type="radio"
                        id="radio-3" 
                        name="delivery" 
                        value="post"
                    />
                    <label for="radio-3" class="flex-column">
                        <div class="rarefied">
                            ПОЧТОЙ
                        </div>
                        <div class="grey">
                            от 5 до 7 дней
                        </div>
                    </label>
                </li>
                `
            }

        }

        $('.delivery-options-outlet').html(
            `
            <div class="delivery-options-outlet">
                <div class="field cart-field">
                    <div class="field-title">
                        Адрес
                    </div>
                    <div class="field-input-box">
                        <input class="input" id="cart-address">
                    </div>
                </div>
                <div class="field cart-field">
                    <div class="field-title">
                        Пожелания
                    </div>
                    <div class="field-input-box">
                        <input class="input" id="client-notes">
                    </div>
                </div>
            </div>
            `
        )

        deliveryOptions.html(deliveryOptionsTemplate);

        this._bindDeliveryOptionsChange()
        this.recalculate();
    }

}