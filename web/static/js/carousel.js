
document.querySelectorAll(".carousel").forEach(carousel => {
    const items = carousel.querySelectorAll(".carousel-item");

    const prev = carousel.querySelectorAll(".carousel-control-prev");

    const next = carousel.querySelectorAll(".carousel-control-next");

    let loop = true;

    let current = 0;

    let ready = true;

    function hide(direction){
        
        const direction_class = direction == 'right' ? 'carousel-item-prev' : 'carousel-item-next'
        const order_class = direction == 'right' ? 'carousel-item-end' : 'carousel-item-start'
        ready = false;
        $(carousel).trigger("slide$bs.carousel");
        $(items[current]).addClass(direction_class);
        $(items[current]).addClass(order_class);   //adds left or right to classes
        console.log(items[current].className);
        console.log(items[0].className);
        
        setTimeout(() => {
            ready = true
            $(items[current]).removeClass("active").removeClass(direction_class).removeClass(order_class);
        }, 200);
        
    }

    function show(direction){
        const direction_class = direction == 'right' ? 'carousel-item-prev' : 'carousel-item-next'
        $(items[current]).addClass(direction_class);
        setTimeout(() => {
            console.log(items[current].className);
            $(items[current]).addClass("active");
            $(items[current]).removeClass(direction_class);
            ready = true
        }, 200);
        
    }

    $(prev).on('click', function(){
        if (ready!=true){
            return
        }
        console.log("previous" + carousel.id);
        if (current != 0){
            hide('left');
            current -= 1;
            show('right');
        }
        else{
            if (loop == true){
                hide('left');
                current = items.length - 1;;
                show('right');
            }
        }
        
    });

    $(next).on('click', function(){
        if (ready!=true){
            return
        }
        console.log("next" + carousel.id);
        if (current != items.length - 1){
            hide('right');
            current += 1;
            show('left');
        }
        else{
            if (loop == true){
                
                hide('right');
                current = 0
                show('left');
            }
        }
    });

    items.forEach(item => {
        console.log($(item).offset());
    })



});


// internet code i should understand before writing my own jqueury version
/*
const carousel = document.getElementById('carouselExampleControls')
const items = carousel.querySelectorAll('.carousel-item');
let currentItem = 0;
let isActive = true;

function setCurrentItem(index) {
  currentItem = (index + items.length) % items.length;
}

function hideItem(direction) {
  isActive = false;
  items[currentItem].classList.add(direction);
  items[currentItem].addEventListener('animationend', function() {
    this.classList.remove('active', direction);
  });
}

function showItem(direction) {
  items[currentItem].classList.add('next', direction);
  items[currentItem].addEventListener('animationend', function() {
    this.classList.remove('next', direction);
    this.classList.add('active');
    isActive = true;
  });
}

document.getElementById('carouselPrev').addEventListener('click', function(e) {
  e.preventDefault()
  if (isActive) {
    hideItem('to-right');
    setCurrentItem(currentItem - 1);
    showItem('from-left');
  }
});

document.getElementById('carouselNext').addEventListener('click', function(e) {
  e.preventDefault()
  if (isActive) {
    hideItem('to-left');
    setCurrentItem(currentItem + 1);
    showItem('from-right');
  }
});

*/