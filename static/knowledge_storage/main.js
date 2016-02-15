
//var change_page = function() {
//
//    $('.arrow-next').click(function () {
//        var currentSlide = $('.active-slide');
//        var nextSlide = currentSlide.next();
//        if (nextSlide.length == 0) {
//            nextSlide = $('.slide').first();
//        };
//        currentSlide.fadeOut(600).removeClass('active-slide');
//        nextSlide.fadeIn(600).addClass('active-slide');
//
//        var currentDot = $('.active-dot');
//        nextDot = currentDot.next();
//        if (nextDot.length == 0) {
//            nextDot = $('.dot').first();
//        };
//        currentDot.removeClass('active-dot');
//        nextDot.addClass('active-dot');
//    });
//
//    $('.arrow-prev').click(function () {
//        var currentSlide = $('.active-slide');
//        var prevSlide = currentSlide.prev();
//        if (prevSlide.length == 0) {
//            prevSlide = $('.slide').last();
//        };
//        currentSlide.fadeOut(600).removeClass('active-slide');
//        prevSlide.fadeIn(600).addClass('active-slide');
//
//        var currentDot = $('.active-dot');
//        prevDot = currentDot.prev();
//        if (prevDot.length == 0) {
//            prevDot = $('.dot').last();
//        };
//        currentDot.removeClass('active-dot');
//        prevDot.addClass('active-dot');
//    });
//};

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


var select_row = function() {
    $(".active_row").click(function () {
        window.location = $(this).find('a').attr('href');
    }).hover(function () {
        $(this).toggleClass('hover');
    });
};


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


var save_comment = function(comment) {

        var note_id_text = document.getElementById("note_id").textContent;
        var regex = /\d+/g;
        var note_id = note_id_text.match(regex);
        if (note_id.length != 1) {
            alert("Wrong note number.")
        }
        else {
            $.ajax({
                url: "/api/add_comment/",
                dataType: "json",
                type: "POST",
                data: {
                    comment: comment,
                    note_id: note_id[0]
                },
                success: function (data) {
                    //var newElement = document.createElement('p');
                    //newElement.setAttribute("id", "log_record");
                    //newElement.innerHTML = "User: '" + data['user_id'] + "' set parameter: '" + data['param_id'] + "' value: '"
                    //    + data['value_id'] + "' for terminal: '" + data['term_id'] + "' datetime: '" + data['added'] + "'";
                    //document.getElementById("logs").appendChild(newElement);
                    var username = data['username'];
                    var date = data['date'];
                    //u = '<p>document.write(username)</p>';
                    //d = '<p>document.write(date)</p>';
                    //c = '<p>document.write(comment)</p>';
                    var newElement = document.createElement('li');
                    newElement.innerHTML = "<p>" + username + "</p>" + "<p>" + date + "</p>" + "<p>" + comment + "</p>";
                    a = $('.comment-notes');
                    $(newElement).prependTo('.comment-notes');
                    $('.status-box').val('');
                    $('.comment-counter').text(5000);
                    $('#comment_btn').addClass('disabled');
                },
                error: function () {
                    alert("Error occurred");
                }
            });
        }
};


var add_comments = function() {
    var comment_btn = $('#comment_btn');
    comment_btn.click(function() {
        if(!comment_btn.hasClass('disabled')) {
            var comment = $('.status-box').val();
            save_comment(comment);
        }
    });

    $('.status-box').keyup(function() {
        var commentLength = $(this).val().length;
        var charactersLeft = 5000 - commentLength;
        $('.comment-counter').text(charactersLeft);
        if (charactersLeft < 0) {
            $('#comment_btn').addClass('disabled');
        } else if (charactersLeft == 5000) {
            $('#comment_btn').addClass('disabled');
        } else {
            $('#comment_btn').removeClass('disabled');
        }
    });
};



//function loadParams(term_id) {
//  var xhttp = new XMLHttpRequest();
//  xhttp.onreadystatechange = function() {
//    if (xhttp.readyState == 4 && xhttp.status == 200) {
//     //document.getElementById("jstree_demo_div").appendChild(xhttp.responseText);
//     var newElement = document.createElement('div');
//     newElement.setAttribute("id", "param_value");
//     var oldElement = document.getElementById('param_value');
//     newElement.innerHTML = xhttp.responseText;
//     if (oldElement) {
//         document.getElementById("container").replaceChild(newElement, oldElement);
//     } else {
//         document.getElementById("container").appendChild(newElement);
//     }
//     change_param();
//    }
//  };
//  xhttp.open("GET", "/api/show_network_tree/?id="+term_id, true);
//  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
//  xhttp.send();



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
    select_row();
    close_message();
    topic_autocompletion();
    add_comments();
};

$('#comment_btn').addClass('disabled');
$(document).ready(main);