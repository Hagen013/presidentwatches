import store from '@/store/index.js';
import locationStore from '@/store/location/index.js'
import favoritesStore from '@/store/favorites/index.js'
import geoApi from '@/api/geo'
import { priceFilter, timeFilter } from '@/utils/filters.js'
import toggleSidebar from '@/utils/toggleSidebar.js'

import FastBuy from '@/components/FastBuy.js';

$(document).ready(function() {

    if (window.innerWidth < 968) {
        $("[data-fancybox]").fancybox({

        });
    } else {
        $("[data-fancybox]").fancybox({
            thumbs : {
                autoStart   : true,
                hideOnClose : false,
                transitionEffect: "slide",
            },
        });
    }

    let thumbnails = $('.product-front__img-link');
    for (let i=0; i<thumbnails.length; i++) {
        if (thumbnails[i].href.indexOf('youTube') !== -1) {
            let href = thumbnails[i].href;
            let slug = /youTube-thumb-(.*?)-/.exec(href)[1];
            thumbnails[i].href = `href="https://www.youtube.com/watch?v=${slug}`
            $(thumbnails[i]).html(`
            <iframe width="100%" height="100%" src="https://www.youtube.com/embed/${slug}" 
                frameborder="0" allow="accelerometer;
                encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
            `)
        }
    }

    $('#add-to-cart').click(function() {
        store.dispatch('addToCart', PRODUCT);
        $('#add-to-cart').replaceWith(`
        <a class="button button_big button_accent product-main__button float-left"
            href="/cart/"
        >
            ОФОРМИТЬ ЗАКАЗ
        </a>
        `)
        console.log(window.innerWidth);
        if (window.innerWidth < 1500) {
            console.log("TSOY")
            toggleSidebar('#cart');
        }
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
    
    $('.product-like').click(function() {
        toggleFavorite(this);
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

    function toggleFavorite(button) {
        let $button = $(button);
        let payload = {
            pk: PRODUCT.pk
        }

        if ( $button.hasClass('active') ) {
            favoritesStore.dispatch('removeFromFavorites', payload);
        } else {
            favoritesStore.dispatch('addToFavorites', payload);
        }
    }

    function renderFavorites() {
        if (PRODUCT.pk in favoritesStore.state.favorites.items) {
            $('.product-like').addClass('active')
        } else {
            $('.product-like').removeClass('active')
        }
    }

    favoritesStore.events.subscribe('stateChange', () => renderFavorites());

    // Работа с мобильными вкладками
    $('.panel-title').click(function(e) {
        e.preventDefault();
        let $this = $(this);
        let $panel = $($this.parents('.panel'));

        if ($this.hasClass('active')) {
            $this.removeClass('active');
        } else {
            $this.addClass('active');
        }

        $panel.find('.collapse').slideToggle(300);
    })

    function scrollTo(selector) {
        if (window.innerWidth <= 768) {
            $('html, body').animate({ scrollTop: $(selector).offset().top-64}, 1000);
        } else {
            $('html, body').animate({ scrollTop: $(selector).offset().top-80}, 500);
        }
    }

    // Быстрые скроллы
    function transitToDescription() {
        let $tabsNav = $('.tabs-nav');
        let links = $tabsNav.find('.tabs-link');
        let tabs = $('.tab-pane');

        for (let i=0; i<links.length; i++) {
            $(links[i]).removeClass('active')
        }

        for (let i=0; i<tabs.length; i++) {
            $(tabs[i]).removeClass('active')
        }

        $('#descriptionLink').addClass('active');
        $('#description').addClass('active');
        scrollTo('#description');
    }

    function transitToReviews() {
        if (window.innerWidth <= 768) {
            let $title = $('#collapseReviewsTitle');
            let $panel = $title.parents('.panel');

            if ($title.hasClass('active')) {
                $panel.find('.collapse').slideToggle(300);
            } else {
                $title.addClass('active');
            }
            $panel.find('.collapse').slideToggle(300);
            scrollTo('#collapseReviewsTitle');
        } else {
            let $tabsNav = $('.tabs-nav');
            let links = $tabsNav.find('.tabs-link');
            let tabs = $('.tab-pane');

            for (let i=0; i<links.length; i++) {
                $(links[i]).removeClass('active')
            }

            for (let i=0; i<tabs.length; i++) {
                $(tabs[i]).removeClass('active')
            }

            $('#reviewsTabLink').addClass('active');
            $('#reviews').addClass('active');
            scrollTo('#reviews');
        }
    }

    $('.product-main__reviews-count').click(function() {
        transitToReviews();
    })

    $('.product-card__show-descr').click(function() {
        transitToDescription();
    })

})