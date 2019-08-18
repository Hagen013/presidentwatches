window.onload = function() {
    
    let images = document.getElementsByClassName('promo-card-image');

    for (let i=0; i<images.length; i++) {
        let imgLarge = new Image();
        imgLarge.src = images[i].dataset.large;

        imgLarge.onload = function () {

            images[i].classList.add('active');
            images[i].style.backgroundImage = `url(${imgLarge.src})`;
        };
    };
}