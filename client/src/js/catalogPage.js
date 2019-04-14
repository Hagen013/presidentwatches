import store from '@/store/index.js'

import { SortingController } from './controllers/sortingController.js'
import Filter from '@/components/Filter.js'
import Tag from '@/components/Tags'


new SortingController('#sorting-bar');


$(document).ready(function() {
    NODE_VALUES = NODE_VALUES.replace(/&#34;/g, '"');
    NODE_VALUES = JSON.parse(NODE_VALUES);
    store.commit('setBaseFacetes', NODE_VALUES);

    let filters = $('.filter');
    
    for (let i=0; i<filters.length; i++) {
        let filterSelector = filters[i];
        let filter = new Filter(filterSelector);
    }    
})

// FILTERS BREADCRUMBS