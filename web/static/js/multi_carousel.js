function updateAll(items){
    let card_width = $(items).width()+40;
    let scroll_size = 3;
    if (window.innerWidth <= 900){
        scroll_size = 2;
    }
    if (window.innerWidth <= 650){
        scroll_size = 1;
    }
    return [card_width, scroll_size];
}

document.querySelectorAll(".carousel").forEach(carousel => {

    // CONSTANT DEFINITIONS //
    const items = carousel.querySelectorAll(".carousel-item");
    const inner = carousel.querySelectorAll(".carousel-inner");
    const prev = carousel.querySelectorAll(".carousel-control-prev-icon");
    const next = carousel.querySelectorAll(".carousel-control-next-icon");

    let scroll_pos = 0;
    let current = 0;
    let updates = updateAll(items);
    card_width = updates[0]; scroll_size = updates[1];


    $(next).on('click', function(){
        updates = updateAll(items);
        card_width = updates[0]; scroll_size = updates[1];
        if (current < items.length-scroll_size){ 
            scroll_pos += card_width;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
            current += 1;
        }
    });

    $(prev).on('click', function(){
        updates = updateAll(items);
        card_width = updates[0]; scroll_size = updates[1];
        if (current > 0){ 
            scroll_pos -= card_width;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
            current -= 1;
        }
    });

});
