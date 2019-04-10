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

export default STATE;
