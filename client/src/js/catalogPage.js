import store from '@/store/index.js'
import { SortingController } from './controllers/sortingController.js'
import Filter from '@/components/Filter.js'
import priceSlider from '@/components/priceSlider.js'

import getRedirectionUrl from '@/utils/getRedirectionUrl'


$(document).ready(function() {
    let tags = TAGS.replace(/&#34;/g, '"');
    let coreValues = CORE_VALUES.replace(/&#34;/g, '"');
    tags = JSON.parse(tags);
    coreValues = JSON.parse(coreValues);
    store.commit('setActiveFacetes', tags);
    store.commit('setBaseFacetes', coreValues);

    let filters = $('.filter');
    
    for (let i=0; i<filters.length; i++) {
        let filterSelector = filters[i];
        let filter = new Filter(filterSelector);
    }

    new SortingController('#sorting-bar');
    new priceSlider();

    $(".tag__close").click(function() {
        let $parent = $(this).parent();
        let attribute = $parent.attr('data-attribute');
        let value = Number($parent.attr('data-value'));
        store.commit('removeActiveOption', {key: attribute, value: value});
        let url = getRedirectionUrl();
        window.location = url;
    })
    
})

// FILTERS BREADCRUMBS