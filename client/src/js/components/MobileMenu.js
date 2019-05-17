export default class MobileMenu {

    constructor(selector) {
        let self = this;
        this._cacheDom(selector);
        this._bindMethods();
        
    }

    _cacheDom(selector) {
        this.$element = $(selector);
    }

    _bindMethods() {
        this.$element.find('.nav-list-link').click(function(e) {
            e.preventDefault();
            let target = this.getAttribute('data-target');
            let $targetElement = $(target);
            $targetElement.css('display', 'block');
            setTimeout(() => {
                $targetElement.children('.drawer-content').addClass('active');
            }, 10);

            $('.drawer-backspace').click(function() {
                let $content = $(this).parent();
                $content.removeClass('active');
                $content.parent().css('display', 'none'); 
            })
        })
    }

}