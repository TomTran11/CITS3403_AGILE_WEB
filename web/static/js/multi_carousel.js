

let carousel_width = $('.carousel-inner')[0].scrollWidth;
let card_width = $('.carousel-item').width()+40;

let scroll_pos = 0;


$('.carousel-control-next').on('click', function(){
    scroll_pos += card_width;
    $('.carousel-inner').animate({scrollLeft: scroll_pos}, 600);
});

$('.carousel-control-prev').on('click', function(){
    scroll_pos -= card_width;
    $('.carousel-inner').animate({scrollLeft: scroll_pos}, 600);
});
