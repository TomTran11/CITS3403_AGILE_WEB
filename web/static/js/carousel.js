
document.querySelectorAll(".carousel").forEach(carousel => {
    const items = carousel.querySelectorAll(".carousel-item");

    const buttons = carousel.querySelectorAll(".carousel-item");

    const prev = carousel.querySelectorAll(".carousel-control-prev");

    const next = carousel.querySelectorAll(".carousel-control-next");

    $(prev).on('click', function(){
        console.log("previous" + carousel.id)
    })

    $(next).on('click', function(){
        console.log("next" + carousel.id)
    })

    


});
