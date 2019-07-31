import store from '@/store/index.js'
import state from '@/state/index.js'
import api from '@/api/index.js'
import { SortingController } from './controllers/sortingController.js'
import Filter from '@/components/Filter.js'
import priceSlider from '@/components/priceSlider.js'

import getRedirectionUrl from '@/utils/getRedirectionUrl'
import removeQueryParameter from '@/utils/removeQueryParameter'
import getParameterByName from '@/utils/getParameterByName'
import updateQueryString from '@/utils/updateQueryString.js';

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

    // мобильные фильтры
    // оптимизировать таким образом, чтобы работало только для мобильного разрешения
    
    function dublicateDesktopFilters() {
        let $drawerFiltersList = $('.drawer-filters-list');
        let mobFilters = $drawerFiltersList.find('.filter');
        if (mobFilters.length === 0) {
            $drawerFiltersList.append(filters.clone());
        }
    }

    function getFacetesCounts() {
        let self = this;
        let url = `/search/facetes/${this.key}/count/`;
        let params = {};
        for (let key in store.state.facetes.active) {
            params[key] = store.state.facetes.active[key].join(',')
        }
        api.get(url, {params: params})
            .then(response => {
                let count = response.data.hits.total;
                let url = getRedirectionUrl();
                let $submitButton = $('#filters-submit');
                $submitButton.html(`ПОКАЗАТЬ ${count} ТОВАРОВ`);
                $submitButton.attr('href', url);
                $submitButton.css('display', 'inline-block');
                $('#drawer-filters-clear-btn').addClass('active');
            })
            .catch(error => {
                console.log(error);
            })
    }

    function getOptionName(option) {
        console.log(option)
        let sortingText = 'По популярности';
        switch (option) {
            case 'price':
                sortingText = 'По цене <i class="icon icon_arrow-up"></i>'
                break
            case '-price':
                sortingText = 'По цене <i class="icon icon_arrow-down"></i>'
                break
            case 'scoring':
                sortingText = 'По популярности'
                break
            case 'created_at':
                sortingText = 'По новизне'
                break
            case 'sale_percentage':
                sortingText = 'По скидкам'
                break
        }
        return sortingText
    }

    function createMobileFilters() {
        // Сортировочка
        let sortingOption = getParameterByName('sort_by');
        let sortingText = 'По популярности';
        if (sortingOption === null) {
            sortingOption = 'scoring'
        } else {
            sortingText = getOptionName(sortingOption);
        }
        $('#drawer-sorting-link').html(sortingText);
        let sortingOptions = $('.sorting-list-item');
        for (let i=0; i<sortingOptions.length; i++) {
            let $currentOption = $(sortingOptions[i]);
            let data = $currentOption.attr('data-option');
            if (data === sortingOption) {
                $currentOption.addClass('active');
            } else {
                $currentOption.removeClass('active');
            }
        }

        $('.sorting-list-item').click(function() {
            let data = this.getAttribute('data-option');
            let newSortingtext = getOptionName(data);
            $('#drawer-sorting-link').html(sortingText);
            let currentQuery = location.search;
            currentQuery = updateQueryString(currentQuery, 'sort_by', data);
            currentQuery = removeQueryParameter(currentQuery, 'page');
            document.location.search = currentQuery;
        })

        // Фильтры
        dublicateDesktopFilters();
        let mobileFilters = $('.drawer-filters-list').find('.filter');
        for (let i=0; i<mobileFilters.length; i++) {
            let filterSelector = mobileFilters[i];
            let filter = new Filter(filterSelector, getFacetesCounts);
        }
    }

    if (window.innerWidth < 1032) {
        createMobileFilters();
    }
    state.device.registerListener(function() {
        if (window.innerWidth < 1032) {
            createMobileFilters();
        }
    });

    function clearFilters() {
        // console.log('clearing filters');
        // store.commit('clearActiveOptions');
        // let url = getRedirectionUrl();
        // console.log(url);
        //window.location.href = url;
    }
    
    // $('.drawer-filters-clear-btn, .drawer-filters-clear').click(function() {
    //     clearFilters();
    // })
    //

    new SortingController('#sorting-bar');
    new priceSlider();

    $(".tag__close").click(function() {
        let $parent = $(this).parent();
        if ( !$parent.hasClass('tag-price') ) {
            let attribute = $parent.attr('data-attribute');
            let value = Number($parent.attr('data-value'));
            store.commit('removeActiveOption', {key: attribute, value: value});
            let url = getRedirectionUrl();
            window.location = url;
        } else {
            let param = $parent.attr('data-param');
            let query = document.location.search;
            query = removeQueryParameter(query, param);
            document.location.search = query;
        }
    })
    
})

// FILTERS BREADCRUMBS