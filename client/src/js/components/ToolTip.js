import { debounce } from 'debounce'


export default class ToolTip {

    constructor(element) {
        let self = this;
        this.$element = $(element);
        this.linkOver = false;
        this.textOver = false;

        this.hide = debounce(function() {
            if (self.textOver === false) {
                self.$element.find('.tip').css('display', 'none');
            }
        }, 400);

        this._bindMethods();
    }

    _bindMethods() {

        let self = this;

        this.$element.find('.tip-link').hover(function() {
            if (window.innerWidth >= 768) {
                $('.tip').css('display', 'none');
                this.linkOver = true;
                self.$element.find('.tip').css('display', 'block');
            }
        });

        this.$element.find('.tip').hover(function() {
            self.textOver = true;
        })

        this.$element.find('.tip').mouseleave(function() {
            self.textOver = false;
        })

        this.$element.mouseleave(function() {
            self.hide();
        });

    }

}
