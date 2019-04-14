export default class Tags {

    constructor(elememt) {
        let tags = $(elememt).children('.tag');
        for (let i; i<tags.length; i++) {
            let tag = tags[i];
            $(tag).find('.tag__close').click(function() {
                console.log('tag');
            })
        }
    }

}
