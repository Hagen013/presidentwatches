import Cookies from 'js-cookie'

export default {
    setLocation(state, payload) {
        Cookies.set('city_name', payload.name);
        Cookies.set('city_code', payload.code);
        state.location = {
            city_code: payload.code,
            city_name: payload.name
        };
    }
}
