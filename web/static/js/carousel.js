
document.querySelectorAll(".carousel").forEach(carousel => {

    // CONSTANT DEFINITIONS //
    const items = carousel.querySelectorAll(".carousel-item");
    const prev = carousel.querySelectorAll(".carousel-control-prev-icon");
    const next = carousel.querySelectorAll(".carousel-control-next-icon");

    // VARIABLE DEFINITIONS //
    let current = 0;
    let upcoming = 0;
    let ready = true;
    let loop = false;
    if (Array.from(carousel.classList).includes("loop")){
        loop = true;
    }
    
    let animation = false; //when false, none of the animation related class changes are applied
    if (Array.from(carousel.classList).includes("animation")){
        animation = true;
    }
    
    /*
    * this function is used to hide a carousel item to either the left or right
    * side of the screen. Takes one parameter, string direction, which is either
    * 'left' or 'right'.
    */
    function hide(direction){
        ready = false;
        if (animation == true){
            //get classes from direction
            const direction_class = direction == 'right' ? "carousel-item-prev" : "carousel-item-next";
            const order_class = direction == 'right' ? "carousel-item-end" : "carousel-item-start";        

            //add classes
            $(items[current]).addClass(direction_class);
            $(items[current]).addClass(order_class);  

        //remove classes and update and change current index
            setTimeout(() => {
                ready = true;
                if (animation == true){
                    $(items[current]).removeClass(direction_class);
                    $(items[current]).removeClass(order_class);
                }
                $(items[current]).removeClass("active");
                current = upcoming
            }, 400);
        }
        else{
            $(items[current]).removeClass("active");
            current = upcoming
        }
    }

    /*
    * this function is used to show a carousel item from either the left or right
    * side of the screen. Takes one parameter, string direction, which is either
    * 'left' or 'right'.
    */
    function show(direction){
        if (animation == true){
            //get classes from direction and add class
            const direction_class = direction == 'right' ? 'carousel-item-prev' : 'carousel-item-next';
            $(items[upcoming]).addClass(direction_class);

            //remove classes
            setTimeout(() => {  
                $(items[upcoming]).removeClass(direction_class);
                $(items[upcoming]).addClass("active");            
            }, 200);
        }
        else{
            $(items[upcoming]).addClass("active");
            ready = true;
        }

        //update indicators
        indicator_set = carousel.querySelectorAll(".carousel-indicators")[0];
        if (indicator_set != undefined){
            indicators = indicator_set.querySelectorAll("li");
            for (i=0; i< indicators.length; i++) {
                if (i == upcoming){
                    $(indicators[i]).addClass("active");
                }
                else {
                    $(indicators[i]).removeClass("active");
                }
            }
        }
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
            upcoming = current - 1;
            hide('left');
            show('right'); 
        }
        else{
            // only wrap backwards if looping is allowed
            if (loop == true){
                upcoming = items.length - 1;
                hide('left');
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
            upcoming = current + 1;
            hide('right');
            show('left');
        }
        else{
            // only wrap backwards if looping is allowed
            if (loop == true){
                upcoming = 0
                hide('right');
                show('left');
            }
        }
    });

});

