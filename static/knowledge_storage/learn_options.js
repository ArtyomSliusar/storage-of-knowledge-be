
var change_page = function() {

    $('.arrow-next').click(function () {
        var currentSlide = $('.active-slide');
        var nextSlide = currentSlide.next();
        if (nextSlide.length == 0) {
            nextSlide = $('.slide').first();
        };
        currentSlide.fadeOut(600).removeClass('active-slide');
        nextSlide.fadeIn(600).addClass('active-slide');

        var currentDot = $('.active-dot');
        nextDot = currentDot.next();
        if (nextDot.length == 0) {
            nextDot = $('.dot').first();
        };
        currentDot.removeClass('active-dot');
        nextDot.addClass('active-dot');
    });

    $('.arrow-prev').click(function () {
        var currentSlide = $('.active-slide');
        var prevSlide = currentSlide.prev();
        if (prevSlide.length == 0) {
            prevSlide = $('.slide').last();
        };
        currentSlide.fadeOut(600).removeClass('active-slide');
        prevSlide.fadeIn(600).addClass('active-slide');

        var currentDot = $('.active-dot');
        prevDot = currentDot.prev();
        if (prevDot.length == 0) {
            prevDot = $('.dot').last();
        };
        currentDot.removeClass('active-dot');
        prevDot.addClass('active-dot');
    });
};

var close_message = function(){
    $('.messages').click(function(){
        $('.messages').remove();
    });
};


var topic_autocompletion = function() {
  $("#id_topic").autocomplete({
    source: function(request, response) {
            $.ajax({
                url: "/api/get_topics/",
                dataType: "json",
                data: {
                    term : request.term,
                    subject : $("#id_subject").val()
                },
                success: function(data) {
                    response(data);
                }
            });
        },
    minLength: 2,
  });
};


//var times = 0;
//function add_page_history() {
//    times++;
//    location.hash = times;
//}
//
//window.onhashchange = function() {
//    if (location.hash.length > 0) {
//        times = parseInt(location.hash.replace('#',''),10);
//    } else {
//        times = 0;
//    }
//};


var main = function() {
    change_page();
    close_message();
    topic_autocompletion();
};


$(document).ready(main);