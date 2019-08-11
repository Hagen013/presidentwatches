let mapping = {
    '#cart': '#sidebar-cart-link',
    '#favorites': '#sidebar-favorites-link',
    '#viewed': '#sidebar-viewed-link'
}

export default function toggleSidebar(tabSelector) {
    $('#page-overlay').addClass('active');
    $('#sidebar').addClass('active');
    $('.sidebar-link').each(function(index) {
        $(this).removeClass('active');
    })
    $('.sidebar-pane').each(function(index) {
        $(this).removeClass('active');
    });
    $(tabSelector).addClass('active');
    $(mapping[tabSelector]).addClass('active');
}