import { SortingController } from './controllers/sortingController.js'

new SortingController('#sorting-bar');

$('.filter-heading').click(function() {
    let parent = this.parentElement;
    $(parent).toggleClass('active');
})

function getFacetes(key) {
    console.log('facetes');
    let url = `/api/v0/search/facetes/${key}/`;
    fetch(url).then(
        response => {
            console.log('success');
            console.log(response);
        },
        response => {
            console.log('success');
            console.log(response);
        }
    )
}