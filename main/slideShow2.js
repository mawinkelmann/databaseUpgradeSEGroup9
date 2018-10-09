//var $slides = $('.slideItem');
//var $images = $('.slideItem img');
var maxWidth = 700;
var maxHeight = 400;

//$images.each(function(index) {
//    if($(this).width() > maxWidth) {maxWidth = $(this).width();}
//    if($(this).height() > maxHeight) {maxHeight = $(this).height();}
//});

//$images.each(function(index) {
//    var ratio = maxWidth / $(this).width();
//    if(($(this).height() * ratio) < maxHeight) {$(this).height(maxHeight + 'px');}
//});
//
//console.log('W: ' + maxWidth + " H: " + maxHeight);
//
//$('#slideShow').width(maxWidth + 'px');
//$('#slideShow').height(maxHeight + 'px');
//$('#slideShow').css("overflow", "hidden");
//
//slideShow();
//
//function slideShow() {
//    $slides.hide();
//    index++;
//    if(index > $slides.length) {
//        index = 1;
//    }
//    $slides[index - 1].style.display = "block";
//    setTimeout(slideShow, 6500);
//}

var index = 1;
var timeoutHandle;
displaySlideshow(index);

// Next/previous controls
function advanceSlide(n) {
  clearTimeout(timeoutHandle);
  displaySlideshow(index += n);
}

// Thumbnail image controls
function selectSlide(n) {
  clearTimeout(timeoutHandle);
  displaySlideshow(index = n);
}

function displaySlideshow(n) {
  var i;
  var $slides = $('.slides');
  var $dots = $('.slideshowDot');
  if (n > $slides.length) {index = 1} 
  if (n < 1) {index = $slides.length}
  for (i = 0; i < $slides.length; i++) {
      $slides[i].style.display = "none"; 
  }
  for (i = 0; i < $dots.length; i++) {
      $dots[i].className = $dots[i].className.replace(" dotActive", "");
  }
  $slides[index-1].style.display = "block"; 
  $dots[index-1].className += " dotActive";
    
  timeoutHandle = setTimeout(function(){ displaySlideshow(index += 1); }, 6500);
}