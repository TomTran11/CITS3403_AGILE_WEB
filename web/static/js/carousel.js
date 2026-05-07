
document.querySelectorAll(".carousel").forEach(carousel => {

    // CONSTANT DEFINITIONS //
    const items = carousel.querySelectorAll(".carousel-item");
    const prev = carousel.querySelectorAll(".carousel-control-prev-icon");
    const next = carousel.querySelectorAll(".carousel-control-next-icon");

    // VARIABLE DEFINITIONS //
    let current = 0;
    let upcoming = 0;
    let ready = true;
    let loop = true;
    
    /*
    * this function is used to hide a carousel item to either the left or right
    * side of the screen. Takes one parameter, string direction, which is either
    * 'left' or 'right'.
    */
    function hide(direction){
        //get classes from direction
        const direction_class = direction == 'right' ? "carousel-item-prev" : "carousel-item-next"
        const order_class = direction == 'right' ? "carousel-item-end" : "carousel-item-start"
        ready = false;

        //add classes
        $(items[current]).addClass(direction_class);
        $(items[current]).addClass(order_class);  

        //remove classes and update and change current index
        setTimeout(() => {
            ready = true
            $(items[current]).removeClass(direction_class);
            $(items[current]).removeClass(order_class);
            $(items[current]).removeClass("active");
            current = upcoming
        }, 400);
    }

    /*
    * this function is used to show a carousel item from either the left or right
    * side of the screen. Takes one parameter, string direction, which is either
    * 'left' or 'right'.
    */
    function show(direction){
        //get classes from direction and add class
        const direction_class = direction == 'right' ? 'carousel-item-prev' : 'carousel-item-next'
        $(items[upcoming]).addClass(direction_class);

        //remove classes
        setTimeout(() => {
            $(items[upcoming]).addClass("active");
            $(items[upcoming]).removeClass(direction_class);
            
        }, 200);
    }

    /*
    * this function moves carousel items on click of previous button
    */
    $(prev).on('click', function(){
        //return if not ready
        if (ready!=true){
            return
        }
        if (current != 0){ 
            hide('left');
            upcoming = current - 1;
            show('right'); 
        }
        else{
            // only wrap backwards if looping is allowed
            if (loop == true){
                hide('left');
                upcoming = items.length - 1;;
                show('right');
            }
        }
        
    });

    /*
    * this function moves carousel items on click of next button
    */
    $(next).on('click', function(){
        //return if not ready
        if (ready!=true){
            return
        }
        if (current != items.length - 1){
            hide('right');
            upcoming = current + 1;
            show('left');
        }
        else{
            // only wrap backwards if looping is allowed
            if (loop == true){
                hide('right');
                upcoming = 0
                show('left');
            }
        }
    });

});

