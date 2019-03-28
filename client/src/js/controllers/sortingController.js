import updateQueryString from '../utils/updateQueryString.js';
import removeQueryParameter from '../utils/removeQueryParameter.js'

export class SortingController {

    constructor(selector) {
        let self = this;
        let items = $(selector).find('.sorting-item');
        $(items).click(function(e) {
            self.setActiveOption(this, items);
        })
    }

    setActiveOption(element, items) {
        let sortingOption = element.getAttribute('data-option');
        let wrapElement = $(element);

        if ( wrapElement.hasClass('active') ) {
            if ( wrapElement.hasClass('inc-dec') ) {
                if ( wrapElement.hasClass('decrement') ) {
                    wrapElement.removeClass('decrement');
                    this.sortingRedirect(sortingOption);
                }
                else {
                    sortingOption = '-' + sortingOption;
                    wrapElement.addClass('decrement')
                    this.sortingRedirect(sortingOption);
                }
            } else {

            }     
        } else {
            this.clearActiveOptions(items);
            wrapElement.addClass('active');
            this.sortingRedirect(sortingOption);
        }

    }

    clearActiveOptions(items) {
        for (let i=0; i<items.length; i++) {
            $(items[i]).removeClass('active');
        }
    }

    sortingRedirect(sortingOption) {
        let currentQuery = location.search;
        currentQuery = updateQueryString(currentQuery, 'sort_by', sortingOption);
        currentQuery = removeQueryParameter(currentQuery, 'page');
        document.location.search = currentQuery;
    }
}