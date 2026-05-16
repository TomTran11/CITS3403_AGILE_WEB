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
    let running = 0;

    $( window ).resize(function() {
        if (running == 1){
            return
        }
        running = 1;
        setTimeout(function (){
            scroll_pos = 0;
            current = 0;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
            scroll_size = updateScroll();
            card_width = $(items).width()+40;
            console.log($(window).width(), current, card_width, scroll_size);
            running = 0

        }, 500);
        
    });



    $(next).on('click', function(){
        console.log("next")
        if (current < items.length-scroll_size){ 
            scroll_pos += card_width;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
            current += 1;
            console.log("moved")
        }
    });

    $(prev).on('click', function(){
        console.log("prev")
        if (current > 0){ 
            scroll_pos -= card_width;
            $(inner).animate({scrollLeft: scroll_pos}, 600);
            current -= 1;
            console.log("moved")
        }
    });

});
