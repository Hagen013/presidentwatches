var MESSAGES_COUNT = 0;

class Message {

    constructor(payload) {
        MESSAGES_COUNT += 1;

        this.identifier = `message-${MESSAGES_COUNT}`;
        this.selector = `#message-${MESSAGES_COUNT}`;
        this.payload = payload;
        this.mouseOver = false;
        this.ticked = false;
        this.closing = false;

        this.show();
        this._bindMethods();
    }

    _bindMethods() {
        let self = this;

        this.triggerRemove()

        $(this.selector).mouseenter(function() {
            self.mouseOver = true;
        })

        $(this.selector).mouseleave(function() {
            self.mouseOver = false;
            self.triggerRemove(3000);
        })

        $(this.selector).find('.message-btn-2').click(function() {
            self.close();
        })
    }

    triggerRemove(time=4000) {
        let self = this;

        setTimeout(function() {
            self.hide()
        }, time)
        setTimeout(function() {
            self.destroy()
        }, time+1000)   
    }

    close() {
        let self = this;
        this.closing = true;
        $(this.selector).animate({top: '-100px', opacity: 0})
        setTimeout(function() {
            $(this.selector).remove();
        }, 1000)  
    }

    show() {
        $('body').append(`
        <div class="message ${this.payload.type}" id="${this.identifier}">
            <div class="message-title">
            ${this.payload.title}
            </div>
            <div class="message-text">
            ${this.payload.text}
            </div>
            <div class="message-buttons">
                ${this.payload.link}
                <div class="message-btn button_accent message-btn-2">
                ОК
                </div>
            </div>
        </div>`);

        $(this.selector).animate({top: '30px', opacity: 1})
    }

    hide() {
        if ( (!this.mouseOver) && (!this.closing) ) {
            $(this.selector).animate({top: '-100px', opacity: 0})
        } else {
            this.ticked = true;
        }
    }

    destroy() {
        if ( (!this.mouseOver) && (!this.closing) ) {
            $(this.selector).remove();
        }
    }

}


function message(payload) {

    new Message(payload);

}

export default message