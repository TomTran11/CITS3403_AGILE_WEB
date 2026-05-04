
document.querySelectorAll(".carousel").forEach(carousel => {
    const items = carousel.querySelectorAll(".carousel-item");

    const prev = carousel.querySelectorAll(".carousel-control-prev");

    const next = carousel.querySelectorAll(".carousel-control-next");

    let current = 0;

    let ready = true;

    function hide(direction){
        ready = false
        $(items[current]).addClass(direction); //adds left or right to classes
        $(items[current]).removeClass("active"); //removes active from classes
        console.log(items[current].className);
    }

        function show(direction){
        ready = false
        $(items[current]).addClass(direction); //adds left or right to classes
        $(items[current]).addClass("active"); //adds active to classes
        console.log(items[current].className);
    }

    $(prev).on('click', function(){
        console.log("previous" + carousel.id)
        if (current != 0){
            hide('left')
            current -= 1;
            show('right')
        }
        
    });

    $(next).on('click', function(){
        console.log("next" + carousel.id)
        if (current != items.length - 1){
            hide('right')
            current += 1;
            show('left')
        }
    });

    items.forEach(item => {
        console.log($(item).offset())
    })



});


