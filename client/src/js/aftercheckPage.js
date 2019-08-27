import Cookies from 'js-cookie'


$(document).ready(function() {
    let admitadCookie = Cookies.get('tagtag_aid');
    if ( admitadCookie !== undefined ) {
        ADMITAD = window.ADMITAD || {};
        ADMITAD.Invoice = ADMITAD.Invoice || {};
        ADMITAD.Invoice.broker = "adm";     // параметр дедупликации (по умолчанию для admitad)
        ADMITAD.Invoice.category = "1";
        
        ADMITAD.Invoice.referencesOrder = ADMITAD.Invoice.referencesOrder || [];
    
        ADMITAD.Invoice.referencesOrder.push({
            orderNumber: PUBLIC_ID,
            orderedItem: PRODUCTS
        });
    
        ADMITAD.Tracking.processPositions();
    }
})