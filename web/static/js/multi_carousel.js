function updateScroll(){
    let scroll_size = 3;
    if (window.innerWidth <= 900){
        scroll_size = 2;
    }
    if (window.innerWidth <= 650){
        scroll_size = 1;
    }
    return scroll_size;
}

document.querySelectorAll(".carousel").forEach(carousel => {

    // CONSTANT DEFINITIONS //
    const items = carousel.querySelectorAll(".carousel-item");
    const inner = carousel.querySelectorAll(".carousel-inner");
    const prev = carousel.querySelectorAll(".carousel-control-prev-icon");
    const next = carousel.querySelectorAll(".carousel-control-next-icon");

    let scroll_pos = 0;
    let current = 0;
    let scroll_size = updateScroll();
    let card_width = $(items).width()+40;

    $( window ).resize(function() {
        if(scroll_size != updateScroll()) {
            scroll_pos = 0
            current = 0;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
        }
        scroll_size = updateScroll();
        card_width = $(items).width()+40;
    });



    $(next).on('click', function(){

        if (current < items.length-scroll_size){ 
            scroll_pos += card_width;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
            current += 1;
        }
    });

    $(prev).on('click', function(){
        if (current > 0){ 
            scroll_pos -= card_width;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
            current -= 1;
        }
    });

});
