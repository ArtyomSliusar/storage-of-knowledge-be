



var close_message = function(){
    $('.messages').click(function(){
        $('.messages').remove();
    });
};



var main = function() {
    close_message();
};


$(document).ready(main);