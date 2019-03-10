$(document).ready(function() {

    var STATE = {
        device: {
            _mode: 'mobile',
            _listeners: [],

            set widthMode(value) {
                this._mode = value;
                for (let index in this._listeners) {
                    this._listeners[index](value);
                }
            },
            get widthMode() {
                return this._mode
            },
            registerListener: function(listener) {
                this._listeners.push(listener);
            }
        }
    }

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


    // STICKY
    let offsetTop = $('.sticky').offset().top;

    function scrollFunction() {
        let windowTop = $(window).scrollTop();
        if (offsetTop < windowTop) {
            $('.sticky').css('position', 'fixed');
        } else {
            $('.sticky').css('position', 'relative')
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

    $('.sidebar-link').click(function(e) {
        e.preventDefault();
        let href = this.getAttribute('href');
        $('.sidebar-link').each(function(index) {
            $(this).removeClass('active');
        })
        $(this).addClass('active');
        $('.sidebar-pane').each(function(index) {
            $(this).removeClass('active');
        });
        $(href).addClass('active');

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

    // MOBILE MENU
    function openMobileMenu() {
        $('#mobile-menu').css('display', 'block');
        setTimeout(function() {
            $('#mobile-menu-container').addClass('active');
        }, 10);
    }
    function closeMobileMenu() {
        $('#mobile-menu').css('display', 'none');
    }
    $('#hamburger').click(function(e) {
        e.preventDefault();
        openMobileMenu();
    })
    $('.menu-left-close').click(function(e) {
        $('#mobile-menu-container').removeClass('active');
        e.preventDefault();
        closeMobileMenu();
    })
    // END MOBILE MENU

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
    
    // AUTH MODAL END


    // TABS
    // перенести в отдельный файл
    $('.tabs-link').click(function(e) {
        e.preventDefault();
        let href = this.getAttribute('href');
        let links = $(this).closest('ul').find('.tabs-link');
        $(links).each(function(index) {
            $(this).removeClass('active');
        })
        $(this).addClass('active');
        let panes = $('.tab-pane');
        panes.each(function(index) {
            $(this).removeClass('active');
        })
        $(href).addClass('active');
    })
    // END TABS
})