import SimpleBar from 'simplebar';

import api from '@/api/index.js'
import SidebarCart from '@/components/sidebarCart'
import SidebarLastSeen from '@/components/sidebarLastSeen'
import SidebarFavorites from '@/components/sidebarFavorites'
import SearchBox from '@/components/SearchBox'
import LocationSearch from '@/components/LocationSearch'
import MobileMenu from '@/components/MobileMenu'
import Likes from '@/components/Likes'
import message from '@/lib/message'

import STATE from '@/state/index.js';
import store from '@/store/index.js';
import toggleSidebarTab from '@/utils/toggleSidebarTab'
import validateEmail from '@/utils/validateEmail'


$(document).ready(function() {

    let resolutions = {
        tablet: 768,
        desktop: 1032,
        wide: 1500,
        maximum: 1730,
    }
    
    // PROCESSING MEDIA QUERIES
    let mq = {
        tablet: window.matchMedia(`(max-width: ${resolutions.tablet-1}px)`),
        desktop: window.matchMedia(`(max-width: ${resolutions.desktop-1}px)`),
        wide: window.matchMedia(`(max-width: ${resolutions.wide-1}px)`),
        maximum: window.matchMedia(`(max-width: ${resolutions.maximum-1}px)`)
    }
    
    function setToMobile() {
        STATE.device.widthMode = 'mobile';
    }

    function setToTablet() {
        STATE.device.widthMode = 'tablet';
    }

    function setToDesktop() {
        STATE.device.widthMode = 'dekstop';
    }

    function setToWide() {
        STATE.device.widthMode = 'wide';
    }

    function setToMaximum() {
        STATE.device.widthMode = 'maximum';
    }

    function checkDeviceWidth() {
        let width = window.innerWidth;
        if (width < resolutions.tablet) {
            setToMobile();
        } else if (width < resolutions.desktop) {
            setToTablet();
        } else if (width < resolutions.wide) {
            setToDesktop();
        } else if (width < resolutions.maximum) {
            setToWide();
        } else {
            setToMaximum();
        }
    }
    checkDeviceWidth();

    for (let key in mq) {
        mq[key].addListener(checkDeviceWidth);
    }
    // END MEDIA QUERIES


    // Components and controllers

    let headerInputBox = document.getElementById('header-input-box');
    let mobileInputBox = document.getElementById('mobile-input-box');

    const sidebarCart = new SidebarCart();
    const lastSeen = new SidebarLastSeen();
    const favorites = new SidebarFavorites();
    const searchBox = new SearchBox(headerInputBox);
    const mobileSearchBox = new SearchBox(mobileInputBox);
    const locationSearch = new LocationSearch();
    const mobileMenu = new MobileMenu('#mobile-menu-container');
    const likes = new Likes();

    // End components

    // STICKY
    let offsetTop = $('.sticky').offset().top;
    let mobileHeaderOffsetTop = 0;

    function scrollFunction() {
        let windowTop = $(window).scrollTop();
        if (offsetTop < windowTop) {
            $('.sticky').css('position', 'fixed');
        } else {
            $('.sticky').css('position', 'relative')
        }
        if (mobileHeaderOffsetTop < windowTop) {
            $('#header-mobile').css('position', 'fixed');
        } else {
            $('#header-mobile').css('position', 'absolute');
        }
    }
    scrollFunction();

    $(window).scroll(function() {
        scrollFunction();
    })
    // END STICKY

    // SIDEBAR
    function showSidebar() {
        $('#page-overlay').addClass('active');
        $('#sidebar').addClass('active');
    }

    function hideSidebar() {
        $('#sidebar').removeClass('active');
        $('#page-overlay').removeClass('active');
    }

    $('.sidebar-link, .control-button_tablet').click(function(e) {
        e.preventDefault();
        let href = this.getAttribute('href');
        toggleSidebarTab(href);

        if (STATE.device.widthMode !== 'maximum') {
            showSidebar();
        }
    })

    $('#page-overlay').click(hideSidebar);

    STATE.device.registerListener(function(val) {
        if ( (val === 'maximum') || (val === 'tablet') ) {
            hideSidebar();
        }
    })
    // END SIDEBAR

    // SEARCH-MODAL
    function openSearchModal() {
        $('#search-modal').css('display', 'block');
    }
    function closeSearchModal() {
        $('.search-modal').css('display', 'none');
    }
    $('#search-mobile').click(function(e) {
        e.preventDefault();
        openSearchModal();
    })
    $('.search-modal-overlay').click(function(e) {
        e.preventDefault();
        closeSearchModal();
    })
    // END SEARCH-MODAL

    // AUTH MODAL
    function openAuthModal() {
        $('#auth-modal').css('display', 'block');
        setTimeout(function() {
            $('#auth-modal-container').addClass('active');
        }, 10);
    }
    function closeAuthModal() {
        $('#auth-modal').css('display', 'none');
        $('#auth-modal-container').removeClass('active');
        closeResetForm();
    }
    function openResetForm() {
        $('#reset-passw-drawer').addClass('active');
    }
    function closeResetForm() {
        $('#reset-passw-drawer').removeClass('active');
    }
    $('.header-auth').click(function(e) {
        e.preventDefault();
        openAuthModal();
    })
    $('#auth-overlay').click(function(e) {
        e.preventDefault();
        closeAuthModal();
    })
    $('#auth-modal-close').click(function(e) {
        closeAuthModal();
    })
    $('#reset-passw').click(function(e) {
        e.preventDefault();
        openResetForm();
    })
    $('#reset-passw-cancel').click(function(e) {
        e.preventDefault();
        closeResetForm();
    })
    $('#reset-submit').click(function(e) {
        let emailValue = $('#reset-email').val();
        if (validateEmail(emailValue)) {
            api.post('/users/passwordreset/', {email: emailValue}).then(
                response => {
                    message({
                        type: 'success',
                        title: 'Новый пароль выслан',
                        text: 'Проверьте указанный почтовый ящик и следуйте инструкции',
                        link: ''
                    })
                    closeAuthModal();
                },
                response => {
                    message({
                        type: 'fail',
                        title: 'Произошла ошибка',
                        text: 'Пожалуйста свяжитесь с оператором',
                        link: ''
                    })
                }
            )
        } else {
            message({
                type: 'fail',
                title: 'Введите валидный Email',
                text: 'предоставленные данные не подходят',
                link: ''
            })
        }
    })
    // AUTH MODAL END


    // TABS
    // перенести в отдельный файл
    $('.tabs-link').click(function(e) {
        e.preventDefault();
        let href = this.getAttribute('href');
        let tabs = $(this).closest('ul');
        let links = tabs.find('.tabs-link');
        let target = tabs.attr('href');
        console.log(tabs);
        console.log(target);
        $(links).each(function(index) {
            $(this).removeClass('active');
        })
        $(this).addClass('active');
        let panes = $(target).find('.tab-pane');
        panes.each(function(index) {
            $(this).removeClass('active');
        })
        $(href).addClass('active');
    })
    // END TABS

    // CUSTOM SCROLLBAR
    let scrollable = document.getElementsByClassName('scrollable');

    for (let i=0; i<scrollable.length; i++) {
        new SimpleBar(scrollable[i], { autoHide: false })
    }
    // END CUSTOM SCROLLBAR

    // MOBILE SORTING AND FILTERING
    function showDrawer(selector) {
        let drawer = $(selector);
        drawer.css('display', 'block');
        setTimeout(() => {
            drawer.children('.drawer-content').addClass('active');
        }, 10);
    }
    function hideDrawer(selector) {
        let drawer = $(selector);
        drawer.css('display', 'none');
        drawer.children('.drawer-content').removeClass('active')
    }
    $('.drawer-btn').click(function(e) {
        e.preventDefault();
        let target = this.getAttribute('href');
        showDrawer(target);
    })
    $('.drawer-close').click(function(e) {
        e.preventDefault();
        let target = this.getAttribute('href');
        hideDrawer(target);
    })
    $('.drawer-overlay').click(function() {
        let parent = $(this).parent();
        hideDrawer(parent);
    })
    // END MOBILE SORTING AND FILTERING

    function validateEmail(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    $('#subscribe').click(function() {
        let inputValue = $('#subscribe-email').val();

        if (validateEmail(inputValue)) {
            api.post('users/subscribes/', {email: inputValue}).then(
                response => {
                    message({
                        type: 'success',
                        title: 'Спасибо!',
                        text: 'Подписка оформлена',
                        link: ''
                    })
                    let rrApiBox = (window["rrApiOnReady"] = window["rrApiOnReady"] || []);
                    rrApiBox.push(function() { rrApi.setEmail(inputValue);})
                },
                response => {
                    message({
                        type: 'fail',
                        title: 'Ошибка',
                        text: 'Введите подходящий email',
                        link: ''
                    })
                }
            )
        } else {
            message({
                type: 'fail',
                title: 'Ошибка',
                text: 'Введите подходящий email',
                link: ''
            })
        }

    })

    $('.register-submit').click(function() {
        let form = $(this).parents('.form');
        let email = $(form).find('.input-email')[0].value;
        if (validateEmail(email)) {
            let rrApiBox = (window["rrApiOnReady"] = window["rrApiOnReady"] || []);
            rrApiBox.push(function() { rrApi.setEmail(email);})
        }
        setTimeout(function(){
            $(form).submit()
        }, 100)
    })

    window.rrAddToBasket = function(pk, qnt) {

    }

    window.rrAddToFavourite = function(pk) {

    }

})