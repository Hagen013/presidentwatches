import getParameterByName from '@/utils/getParameterByName'
import updateQueryString from '@/utils/updateQueryString'
import removeQueryParameter from '@/utils/removeQueryParameter'


export default class PriceFilter {

    constructor() {

        let self = this;
        self.locked = false;
        let price_gte = getParameterByName('price__gte');
        let price_lte = getParameterByName('price__lte');

        price_gte = price_gte === null ? PRICE_MIN : parseInt(price_gte);
        price_lte = price_lte === null ? PRICE_MAX : parseInt(price_lte);
        this.price_gte = price_gte;
        this.price_lte = price_lte;

        $("#slider-range").slider({
            range: true,
            orientation: "horizontal",
            min: PRICE_MIN,
            max: PRICE_MAX,
            values: [price_gte, price_lte],
            step: 10,
    
            slide: function (event, ui) {
                if (ui.values[0] == ui.values[1]) {
                    return false;
                }
                
                $("#min_price").val(ui.values[0]);
                $("#max_price").val(ui.values[1]);
            },

            change: function(event, ui) {
                if (self.locked) {
                    self.locked = false;
                } else {
                    let changed = false;
                    if (ui.values[0] !== price_gte) {
                        changed = true;
                    } else if (ui.values[1] !== price_lte) {
                        changed = true;
                    }
                    if (changed) {
                        self.redirect(ui.values[0], ui.values[1]);
                    }
                }
            }

        });

        $("#min_price,#max_price").on('change', function () {
        
            self.locked = true;
            let minPrice = parseInt($("#min_price").val());
            let maxPrice = parseInt($("#max_price").val());
            
            if (minPrice > maxPrice) {
                let temp = maxPrice;
                maxPrice = minPrice;
                minPrice = temp;
            }

            minPrice = minPrice < PRICE_MIN ? PRICE_MIN : minPrice;
            maxPrice = maxPrice > PRICE_MAX ? PRICE_MAX : maxPrice;

            $('#min_price').val(minPrice);
            $('#max_price').val(maxPrice);

            $("#slider-range").slider({
                values: [minPrice, maxPrice]
            });
              
        });


    }

    redirect(leftValue, rightValue) {
        let query = document.location.search;

        if (leftValue === PRICE_MIN) {
            query = removeQueryParameter(query, 'price__gte');
        } else {
            query = updateQueryString(query, 'price__gte', leftValue);
        }

        if (rightValue === PRICE_MAX) {
            query = removeQueryParameter(query, 'price__lte');
        } else {
            query = updateQueryString(query, 'price__lte', rightValue);
        }
        document.location.search = query;
    }

}

        