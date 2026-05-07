
document.querySelectorAll(".carousel").forEach(carousel => {
    const items = carousel.querySelectorAll(".carousel-item");

    const prev = carousel.querySelectorAll(".carousel-control-prev-icon");

    const next = carousel.querySelectorAll(".carousel-control-next-icon");

    let loop = true;

    let current = 0;

    let upcoming = 0;

    let ready = true;

    function hide(direction){
        const direction_class = direction == 'right' ? "carousel-item-prev" : "carousel-item-next"
        const order_class = direction == 'right' ? "carousel-item-end" : "carousel-item-start"
        ready = false;
        $(carousel).trigger("slide$bs.carousel");
        $(items[current]).addClass(direction_class);
        $(items[current]).addClass(order_class);   //adds left or right to classes
        console.log(items[current].className);
        console.log(current)

        setTimeout(() => {
            ready = true
            $(items[current]).removeClass(direction_class);
            $(items[current]).removeClass(order_class);
            $(items[current]).removeClass("active");
            console.log(items[current].className + " end of hide, removed " +  direction_class);
            console.log(current)
            current = upcoming

        }, 400);
        
    }

    function show(direction){

        const direction_class = direction == 'right' ? 'carousel-item-prev' : 'carousel-item-next'
    
        $(items[upcoming]).addClass(direction_class);
        console.log(items[upcoming].className + " midshow");

        setTimeout(() => {
            $(items[upcoming]).addClass("active");
            $(items[upcoming]).removeClass(direction_class);
            
        }, 200);
        
    }

    $(prev).on('click', function(){
        if (ready!=true){
            return
        }

        if (current != 0){ 
            hide('left');
            upcoming = current - 1;
            show('right'); 
        }

        else{
            if (loop == true){
                hide('left');
                upcoming = items.length - 1;;
                show('right');
            }
        }
        
    });

    $(next).on('click', function(){
        if (ready!=true){
            return
        }
        
        //console.log("next" + carousel.id);
        if (current != items.length - 1){
            hide('right');
            upcoming = current + 1;
            show('left');
        }
        else{
            if (loop == true){

                console.log(items[0].className + " befire rm prev");
                $(items[0]).removeClass("carousel-item-prev");
                console.log(items[0].className + " after");

                hide('right');
                upcoming = 0
                show('left');
            }
        }
    });



});

