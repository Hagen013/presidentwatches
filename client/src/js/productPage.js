import store from '@/store/index.js';
import locationStore from '@/store/location/index.js'
import geoApi from '@/api/geo'
import { priceFilter, timeFilter } from '@/utils/filters.js'

import FastBuy from '@/components/FastBuy.js';

$(document).ready(function() {

    $("[data-fancybox]").fancybox({
        thumbs : {
            autoStart   : true,
            hideOnClose : false,
            transitionEffect: "slide",
        },
    });

    $('#add-to-cart').click(function() {
        store.dispatch('addToCart', PRODUCT);
    })

    locationStore.events.subscribe('stateChange', () => changeLocation());

    $('.thumb').click(function(e) {
        if ( !$(this).hasClass('thumb_active') ) {
            let thumbnails = $('.thumb');
            for (let i=0; i<thumbnails.length; i++) {
                $(thumbnails[i]).removeClass('thumb_active');
            }
            $(this).addClass('thumb_active');

            // Загрузка главного изображения
            let imageSrc = this.getAttribute('data-image');
            let target = this.getAttribute('data-target');
            let image = new Image;
            let imageLink = $(target);
            let images = $('.product-front__img-link');

            for (let i=0; i<images.length; i++) {
                $(images[i]).removeClass('active');
            }
            let fullRes = imageLink.attr('href');
            let child = imageLink.children('img');
            child.attr('src', fullRes);
            $(imageLink).addClass('active');
            
            image.onload = function() {

            }
        }
    })

    $('.gallery-btn_next').click(function() {
        nextSlide();
    })

    $('.gallery-btn_prev').click(function() {
        prevSlide();
    })

    let fastBuy = new FastBuy();

    function nextSlide() {
        let track = $('#gallery-track');
        let thumbs = track.children('.thumb');
        let thumb = thumbs[0];
        let thumbHeight = $(thumb).innerHeight();
        let offset = track.position().top;
        let maximumOffset = ( (thumbs.length-4) * thumbHeight + 10) * -1;

        if (offset > maximumOffset) {
            let newValue = offset - (thumbHeight + 10);
            track.css({'top': newValue});
        }

    }

    function prevSlide() {
        let track = $('#gallery-track');
        let thumb = track.children('.thumb')[0];
        let thumbHeight = $(thumb).innerHeight();
        let offset = track.position().top;
        if (offset < 0) {
            let newValue = offset + (thumbHeight + 10);
            track.css({'top': newValue});
        }
    }

    function changeLocation() {
        if (DELIVERY !== undefined) {
            let city_name = locationStore.state.location.city_name;
            let city_code = locationStore.state.location.city_code;
            let data = {
                'kladr': city_code,
                'product': DELIVERY
            };
            geoApi.post('/api/delivery/one_product/', data).then(
                response => {
                    let data = response.data;

                    let curierPrice = data.curier.price;
                    let curierTimeMin = data.curier.time_min;
                    let curierTimeMax = data.curier.time_max;
                    let filteredPriceCurier = priceFilter(curierPrice);
                    let filteredDateCurier = timeFilter(curierTimeMin, curierTimeMax);

                    let pointsPrice = data.delivery_point.price;
                    let pointsTimeMin = data.delivery_point.time_min;
                    let pointsTimeMax = data.delivery_point.time_max;
                    let filteredPricePoints = priceFilter(pointsPrice, '');
                    let filteredDatePoints = timeFilter(pointsTimeMin, pointsTimeMax);

                    $('.delivery-product').html(

                        `
                        <p class="delivery-curier">
                        ${filteredPriceCurier} в г. ${city_name} курьером, ${filteredDateCurier}
                        </p>
                        <p class="delivery-points">
                        Пункты выдачи — от ${filteredPricePoints}, ${filteredDatePoints}
                        </p>
                        <p class="delivery-rupost">
                            Почтой России — <span class="price">300</span>, от 5 до 7 дней
                        </p>
                        `
                    )
                },
                response => {

                }
            )
        }
    }

})