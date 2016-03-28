window.gClicksOnCourses = false;

var slide_courses = function() {
    $('#icon-courses').click(function(event){
        if (!gClicksOnCourses) {
            $('.courses').animate({
                left: '0px'
            }, 200);
            $('.jumbotron').animate({
                left: '285px'
            }, 200);
        } else {
            $('.courses').animate({
                left: '-285px'
            }, 200);
            $('.jumbotron').animate({
                left: '0px'
            }, 200);
        }
        gClicksOnCourses = !gClicksOnCourses;
        event.stopPropagation();
    });

    $('body').click(function(){
        if (gClicksOnCourses) {
            $('.courses').animate({
                left: '-285px'
            }, 200);
            $('.jumbotron').animate({
                left: '0px'
            }, 200);
            gClicksOnCourses = !gClicksOnCourses;
        }
    });

    $('.courses').click(function(event){
        event.stopPropagation();
    });
};

var cycle_footer = function(){
        $('.footer_main').cycle({
            slideResize: true,
            containerResize: true,
            width: '100%',
            fit: 1,
            fx:      'scrollLeft',
            speed:    1000,
            timeout:  10000
        });
};

var main = function() {
    slide_courses();
    cycle_footer();
    close_message();
};


$(document).ready(main);
