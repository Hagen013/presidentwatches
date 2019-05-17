export default class MobileMenu {

    constructor(selector) {
        let self = this;
        this._cacheDom(selector);
        this._bindMethods();
    }

    _cacheDom(selector) {
        this.$menu = $('#mobile-menu');
        this.$element = $(selector);
    }

    _bindMethods() {

        let self = this;

        // Отображение нужного Drawer'a
        this.$element.find('.nav-list-link').click(function(e) {

            e.preventDefault();
            let target = this.getAttribute('data-target');
            let $targetElement = $(target);
            $targetElement.css('display', 'block');
            setTimeout(() => {
                $targetElement.children('.drawer-content').addClass('active');
            }, 10);

        })

        // Закрытие на кнопку "Назад"
        $('.drawer-backspace').click(function() {
            let $content = $(this).parent();
            $content.removeClass('active');
            $content.parent().css('display', 'none'); 
        })

        // Открытие по клику на Бургер
        $('#hamburger').click(function(e) {
            e.preventDefault();
            self.openMobileMenu();
        })

        // Закрытие по клику на кнопку "Закрыть"
        $('.menu-left-close').click(function(e) {
            $('#mobile-menu-container').removeClass('active');
            e.preventDefault();
            self.closeMobileMenu();
        })

    }

    openMobileMenu() {
        let self = this;
        this.$menu.css('display', 'block');
        setTimeout(function() {
            console.log(self.$menu);
            self.$element.addClass('active');
        }, 10);
    }

    closeMobileMenu() {
        this.$menu.css('display', 'none');
        this.$element.find('.drawer-content').removeClass('active');
        // Закрытие всех мобильных подменю
        $('.drawer-categories').css('display', 'none');
    }

}
