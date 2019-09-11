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
            currency: "RUB",
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

        let rrItems = [];
        for (let i=0; i<G_ITEMS.length; i++) {
            rrItems.push({
                id: G_ITEMS[i].id,
                qnt: G_ITEMS[i].quantity,
                price: G_ITEMS[i].price
            })
        }

        (window["rrApiOnReady"] = window["rrApiOnReady"] || []).push(function() {
            try { 
            rrApi.order({
                transaction: String(PUBLIC_ID),
                items: rrItems
            });
            } catch(e) {} 
        });

        if (CUSTOMER_EMAIL !== null) {
            (window["rrApiOnReady"] = window["rrApiOnReady"] || []).push(function() { rrApi.setEmail(CUSTOMER_EMAIL);});
        }
    
    }, 100)
    //

}