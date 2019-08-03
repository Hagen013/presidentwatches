
$(document).ready(function() {

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

})