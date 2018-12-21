// Функция для извлечения из куков CSRF токена
// требуется для общения с Django по ajax


export default function csrfToken() {
    var result = null,
        cookie_key = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document
            .cookie
            .split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, cookie_key.length + 1) == (cookie_key + '=')) {
                result = decodeURIComponent(cookie.substring(cookie_key.length + 1));
                break;
            }
        }
    }
    return result;
};
