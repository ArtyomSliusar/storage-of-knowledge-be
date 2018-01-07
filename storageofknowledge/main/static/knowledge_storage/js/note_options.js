
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


var save_comment = function(comment) {

        var r_id = document.getElementById("r_id").textContent;
        var t_id = document.getElementById("t_id").textContent;

        $.ajax({
            url: "/api/add_comment/",
            dataType: "json",
            type: "POST",
            data: {
                comment: comment,
                r_id: r_id,
                t_id: t_id
            },
            success: function (data) {
                var username = data['username'];
                var date = data['date'];



                var new_div_comment = document.createElement('div');
                $(new_div_comment).addClass("comment-notes");
                var new_span = document.createElement('span');
                $(new_span).addClass("tip tip-left");
                new_div_comment.appendChild(new_span);
                var new_div_message = document.createElement('div');
                $(new_div_message).addClass("message");
                new_div_comment.appendChild(new_div_message);
                new_div_message.innerHTML = "<p>" + username + "</p>" + "<p>" + date + "</p>" + "<p>" + comment + "</p>";

                $(new_div_comment).prependTo('.dialogbox');
                $('.status-box').val('');
                $('.comment-counter').text(2000);
                $('#comment_btn').addClass('disabled');
            },
            error: function (jqXHR) {
                var msg = '';
                if (jqXHR.status === 307) {
                    window.location.href = '/login/';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                if (msg) {
                    alert('Error occurred | ' + msg);
                }
            }
        });
};


var filter_user_notes = function() {
    $('#users_notes_main').click(function() {
        var checkbox = $(this);
        table = document.getElementById("main_table");
        filter_elements(table, checkbox);
    });
    $('#users_notes_secondary').click(function() {
        var checkbox = $(this);
        table = document.getElementById("secondary_table");
        filter_elements(table, checkbox);
    });
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
        var charactersLeft = 2000 - commentLength;
        $('.comment-counter').text(charactersLeft);
        if (charactersLeft < 0) {
            $('#comment_btn').addClass('disabled');
        } else if (charactersLeft == 2000) {
            $('#comment_btn').addClass('disabled');
        } else {
            $('#comment_btn').removeClass('disabled');
        }
    });
};


var main = function() {
    topic_autocompletion();
    add_comments();
    filter_user_notes();
};

$('#comment_btn').addClass('disabled');
$(document).ready(main);