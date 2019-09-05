import Cookies from 'js-cookie'


window.onload = function() {

    setTimeout(function() {
        let admitadCookie = Cookies.get('tagtag_aid');
        if ( admitadCookie !== undefined ) {
            let ADMITAD = window.ADMITAD || {};
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
    
        // Отправка данных в Яндекс.Метрика
        let params = {
            order_id: PUBLIC_ID,
            order_price: TOTAL,
            currency: "RUR",
            exchange_rate: 1,
            goods:[]
        }
    
        for (let i=0; i<G_ITEMS.length; i++) {
            params.goods.push({
                name: G_ITEMS[i]['name'],
                price: G_ITEMS[i]['price'],
                quantity: G_ITEMS[i]['quantity']
            })
        }
    
        yaCounter14657887.reachGoal('orderConfirmed', params);
        //

        console.log(dataLayer);
        // Отправка данных в аналитику
        dataLayer.push({
            "event": "orderConfirmed",
            "ecommerce": {
                "currencyCode": "RUB",
                "purchase": {
                    "actionField": {
                        "id": PUBLIC_ID
                    },
                    "products": G_ITEMS
                }
            }
        });
    }, 100)
    //

}