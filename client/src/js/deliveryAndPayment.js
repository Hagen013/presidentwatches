import Cookies from 'js-cookie'

import locationStore from '@/store/location/index'
import api from '@/api'
import geoApi from '@/api/geo'
import { priceFilter, timeFilter } from '@/utils/filters'


$(document).ready(function() {

    class DeliveryController {

        constructor() {
            this._initialize();
        }

        _initialize() {
            this.optionsSelector = document.getElementById('delivery-options');
            this.mapSelector = document.getElementById('delivery-map');
            this.cityName = $('#city-name').text();

            this.getDeliveryData();
            locationStore.events.subscribe('stateChange', () => this.changeLocation());
        }

        getDeliveryData() {

            let self = this;
            let kladr = Cookies.get('city_code');
            let products = [
                {
                    price: 1110,
                    purchase_price: 1110,
                    vendor: 'Casio',
                    product_type: 'CUBE'
                },
            ]

            let data =  {
                'kladr': kladr,
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
            this.renderOptions();
            this.renderMap();
            console.log(this.data)
        }

        hanldeFailedGeoResponse(response) {

        }

        changeLocation() {
            this.getDeliveryData();
            this.cityName = $('#city-name').text();
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

        initializeMap() {
            let self = this;
            $.getScript('https://api-maps.yandex.ru/2.1/?lang=ru-RU', function() {
                self.getCoordinates().then(() => {
                    ymaps.ready(self.ymapsInitialize(self));
                })
            });
        }

        ymapsInitialize(self) {
            return function() {
                console.log('tsooyooyy')

                if (self.map !== undefined) {
                    self.map.destroy()
                }
                self.mapSelector.innerHTML = '';

                self.map=new ymaps.Map(self.mapSelector, {
                    center: self.coordinates,
                    zoom: 11,
                    behaviors: ['default', 'scrollZoom'],
                    controls: ['zoomControl', 'fullscreenControl', 'searchControl']
                });

                let collection = [];

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
                            <span class="bold">Срок поставки:</span>${timeFilter([point.time_min, point.time_max])}<br/>
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
    
                for (let i=0; i<self.data.points.pick_point_points.length; i++) {
                    let point = self.data.points.pick_point_points[i];
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
                            <span class="bold">Срок поставки:</span>${timeFilter([point.time_min, point.time_max])}<br/>
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

            }
        }

        renderOptions() {
            let self = this;
            let html = '';
            
            if (this.data.curier !== null) {
                html += `
            <li class="radio-group-container">
                <input type="radio"
                    id="radio-1" 
                    name="delivery" 
                    value="curier"
                />
                <label for="radio-1" class="flex-column">
                    <div class="rarefied">
                        КУРЬЕРОМ
                    </div>
                    <div class="grey">
                        ${timeFilter(self.data['curier']['time_min'], self.data['curier']['time_max'])}
                    </div>
                </label>
            </li>
                `
            } else {
                html += `
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

            if (this.data.delivery_point !== null) {
                html += `
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
                            ${timeFilter(self.data['delivery_point']['time_min'], self.data['delivery_point']['time_max'])}
                        </div>
                    </label>
                </li>
                `
            } else {
                html += `
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


            if (this.cityName === 'Москва') {
                html += `
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
            // Почта
            html += `
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

            this.optionsSelector.innerHTML = html;

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

        renderMap() {
            this.initializeMap();
        }

    }

    new DeliveryController();

})