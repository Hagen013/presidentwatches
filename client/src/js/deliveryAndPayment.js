import Cookies from 'js-cookie'

import locationStore from '@/store/location/index'
import api from '@/api'
import geoApi from '@/api/geo'
import { priceFilter, timeFilter } from '@/utils/filters'


class DeliveryController {

    constructor() {
        let self = this;
        this.$options = $('input[type=radio][name=delivery]');
        this.$outlet = $('#delivery-outlet');
        this.cityName = $('#city-name').text();
        this.kladr = Cookies.get('city_code');
        this.settings = {
            points: 'all',
            postamats: true,
            tab: 'points'
        }
        this.initialized = false;
        this.getDeliveryData();

        this.$options.on('change', function(){
            switch ($(this).val()) {
                case 'curier':
                    self.setDeliveryModeCurier();
                    break
                case 'points':
                    self.setDeliveryModePoints();
                    break
                case 'rupost':
                    self.setDeliveryModeRupost();
                    break
                case 'pickup':
                    self.setDeliveryModePickup();
                    break
            }
        })

        locationStore.events.subscribe('stateChange', () => this.changeLocation());
    }

    getDeliveryData() {
        let self = this;
        let products = [
            {
                price: 1110,
                purchase_price: 1110,
                vendor: 'Casio',
                product_type: 'CUBE'
            },
        ];
        let data = {
            'kladr': this.kladr,
            'products': products
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
        this.data = response.data;

        switch (this.settings.tab) {
            case 'curier':
                this.setDeliveryModeCurier();
                break
            case 'points':
                this.setDeliveryModePoints();
                break
            case 'rupost':
                this.setDeliveryModeRupost();
                break
        }
        $('#price-curier').html(`
        <span class="price">
            от 0 до ${this.data.curier.price}
        </div>
        `);
        $('#time-curier').html(`
        ${timeFilter(this.data.curier.time_min, this.data.curier.time_max)}
        `)
        $('#price-points').html(`
        <span class="price">
            от ${this.data.delivery_point.price}
        </div>
        `);
        $('#time-points').html(`
        ${timeFilter(this.data.delivery_point.time_min, this.data.delivery_point.time_max)}
        `)
        $('#price-rupost').html(`
        <span class="price">
            от 0 до 450
        </span>
        `)
        $('#time-rupost').html(`
        ${timeFilter(this.data.postal_service.time_min, this.data.postal_service.time_max)}
        `)
    }

    hanldeFailedGeoResponse(response) {

    }

    setDeliveryModeCurier() {
        this.$outlet.html(`
        <div class="delivery-curier">
            <div class="delivery-curier-content info-page-content">
                <div class="info-page-block">
                    <div class="info-page-block-title bold">
                    Бесплатная доставка курьером
                    </div>
                    <p>
                    Мы предоставляем бесплатную доставку курьерской службой для товаров <span class="bold">не входящих</span> в следующий список брендов: Casio, Orient, Q&Q,
                    Michael Kors, DKNY, Fossil, Diesel, Михаил Москвин, Заря, Восток, Level.
                    </p>
                    <p>Для товаров, входящих в указанный выше список брендов, расчётная сумма доставки для города <a class="link link_dotted city-choice cityname">${this.cityName}</a> 
                    составляет <span class="price">${this.data.curier.price}</span>.</p>
                    <p>Расчетное время доставки составляет ${timeFilter(this.data.curier.time_min, this.data.curier.time_max)}. 
                    Точное время доставки можно узнать у одного из наших операторов по телефону.</p>
                    <p>Оплата при получении при доставке курьером возмножна как <span class="bold">наличным</span>, так и 
                    <span class="bold">банковской картой</span></p>
                    <p>При получении до оплаты можно распаковать и проверить часы. Для города заказов по городу Москва возможно заказать несколько часов на выбор.</p>
                </div>
            </div>
        </div>
        `);

        $('.city-choice').click(function() {
            let modal = $('#location-modal');
            modal.css('display', 'flex');
        });
        this.settings.tab = 'curier';
        this.hideLoader();
    }

    setDeliveryModePoints() {
        let self = this;
        let pointsTotalCount = this.data.points.pick_point_points.length + this.data.points.sdek_points.length;
        this.$outlet.html(`
        <div class="delivery-points-title bold">
            Пункты выдачи ${pointsTotalCount}
        </div>
        <div class="delivery-points">
            <div class="delivery-points-controls">
                <div class="map-option active" data-value="sdek">
                СДЭК
                </div>
                <div class="map-option active" data-value="pickpoint">
                PickPoint
                </div>
                <div class="map-option active" data-value="postamats">
                Постаматы PickPoint
                </div>
            </div>
            <div class="delivery-points-map">
                <div class="ymap" id="ymap">
                </div>
            </div>
        </div>
        `);
        this.initMap();

        $('.map-option').click(function() {
            let $this = $(this);
            if ($this.hasClass('active')) {
                let value = $this.attr('data-value')
                self.removeSettingsOption(value);
                $this.removeClass('active');
            } else {
                let value = $this.attr('data-value');
                self.addSettingsOption(value);
                $this.addClass('active');
            }
        });

        this.settings.tab = 'points';
        this.hideLoader();
    }

    setDeliveryModeRupost() {
        this.$outlet.html(`
        <div class="delivery-rupost">
            <div class="delivery-rupost-content info-page-content">
                <div class="info-page-block-title bold">
                Бесплатная доставка почтой
                </div>
                <p>
                Мы предоставляем бесплатную доставку Почтой России для товаров <span class="bold">не входящих</span> в следующий список брендов: Casio, Orient, Q&Q,
                Michael Kors, DKNY, Fossil, Diesel, Михаил Москвин, Заря, Восток, Level.
                </p>
                <p>Для остальных товаров, не включенных в список выше, стоимость доставки для всех регионов России фиксированная и составляет <span class="price">450</span>.
                Расчетное время доставки для города <a class="link link_dotted city-choice cityname">${this.cityName}</a> составляет 
                ${timeFilter(this.data.postal_service.time_min, this.data.postal_service.time_max)}.
                </p>
            </div>
        </div>
        `);

        $('.city-choice').click(function() {
            let modal = $('#location-modal');
            modal.css('display', 'flex');
        });
        this.settings.tab = 'rupost';
        this.hideLoader();
    }

    setDeliveryModePickup() {
        this.$outlet.html(`
        `)
    }

    removeSettingsOption(value) {
        let self = this;
        if (value === 'postamats') {
            self.settings.postamats = false;
        } else {
            switch (self.settings.points) {
                case 'all':
                    if (value === 'sdek') {
                        self.settings.points = 'pickpoint'
                    } else {
                        self.settings.points = 'sdek'
                    }
                    break
                case 'sdek':
                    if (value === 'sdek') {
                        self.settings.points = 'none'
                    } else {

                    }
                    break
                case 'pickpoint':
                    if (value === 'sdek') {

                    } else {
                        self.settings.points = 'none';
                    }
                    break
                case 'none':
                    break
            }
        }
        this.updateMap();
    }

    addSettingsOption(value) {
        let self = this;
        if (value === 'postamats') {
            self.settings.postamats = true;
        } else {
            switch (self.settings.points) {
                case 'all':
                    break
                case 'sdek':
                    if (value == 'pickpoint') {
                        self.settings.points = 'all'
                    }
                    break
                case 'pickpoint':
                    if (value === 'sdek') {
                        self.settings.points = 'all'
                    }
                    break
                case 'none':
                    if (value === 'sdek') {
                        self.settings.points = 'sdek';
                    } else {
                        self.settings.points = 'pickpoint'
                    }
                    break
            }
        }
        this.updateMap();
    }

    renderMap(self) {
        return function() {

            if (self.map !== undefined) {
                self.map.destroy();
            }
            self.mapSelector = document.getElementById('ymap');
            self.map = new ymaps.Map(self.mapSelector, {
                center: self.coordinates,
                zoom: 11,
                behaviors: ['default', 'scrollZoom'],
                controls: ['zoomControl', 'fullscreenControl', 'searchControl']
            });
            
            self.addPoints();
        }
    }

    updateMap() {
        this.map.geoObjects.removeAll();
        this.addPoints();
    }

    addPoints() {
        let self = this;
        let collection = [];

        switch (this.settings.points) {
            case 'all':
                collection = self.addSdekPoints(collection);
                collection = self.addPickpointPoints(collection);
                break
            case 'sdek':
                collection = self.addSdekPoints(collection);
                break
            case 'pickpoint':
                collection = self.addPickpointPoints(collection);
                break
            case 'none':
                break
        }

        let clusterer = new ymaps.Clusterer({
            preset: 'islands#invertedVioletClusterIcons',
            clusterIconLayout: 'default#pieChart',
            clusterBalloonItemContentLayout: self.getBalloonContentLayout(),
            clusterDisableClickZoom: false
        });
        
        clusterer.add(collection);
        self.map.geoObjects.add(clusterer);

    }

    addSdekPoints(collection) {
        let self = this;
        for (let i=0; i<self.data.points.sdek_points.length; i++) {
            let point = self.data.points.sdek_points[i];
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
        return collection
    }


    addPickpointPoints(collection) {
        let self = this;
        let points = self.data.points.pick_point_points;
        if (!this.settings.postamats) {
            points = points.filter((item) => {
                return item.type == 2
            })
        }

        for (let i=0; i<points.length; i++) {
            let point = points[i];
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
                        data-type="sdek"
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
        return collection
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

    initMap() {
        let self = this;
        $.getScript('https://api-maps.yandex.ru/2.1/?lang=ru-RU', function() {
            self.getCoordinates().then(() => {
                ymaps.ready(self.renderMap(self));
            })
        });
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

    changeLocation() {
        this.kladr = Cookies.get('city_code');
        this.cityName = Cookies.get('city_name')
        $('.cityname').text(this.cityName);
        this.showLoader();
        this.getDeliveryData();
    }

    showLoader() {
        $('#delivery-loader').fadeIn(300);
    }

    hideLoader() {
        $('#delivery-loader').fadeOut(300);
    }

}


$(document).ready(function() {

    const controller = new DeliveryController();

})