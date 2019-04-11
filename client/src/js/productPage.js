import SidebarCart from '@/components/sidebarCart.js'
import store from '@/store/index.js';
import state from '@/state/index.js';

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

})
