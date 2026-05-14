document.querySelectorAll(".carousel").forEach(carousel => {

    // CONSTANT DEFINITIONS //
    const items = carousel.querySelectorAll(".carousel-item");
    const inner = carousel.querySelectorAll(".carousel-inner");
    const prev = carousel.querySelectorAll(".carousel-control-prev-icon");
    const next = carousel.querySelectorAll(".carousel-control-next-icon");

    let carousel_width = $(inner)[0].scrollWidth;
    let card_width = $(items).width()+40;
    let scroll_pos = 0;
    let current = 0


    $(next).on('click', function(){
        if (current < items.length-3){ 
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
