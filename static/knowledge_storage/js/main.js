var parent_sibling_by_id = function(node, id_name) {
    var parent;
	if (node === null || id_name === '') return;
	parent = node.parentNode;

	while (parent.tagName !== "HTML") {
        required_node = $(parent).siblings(id_name);
        if (required_node.length) {
            return required_node[0];
		}
		parent = parent.parentNode;
	}
	return null;
};


var process_like_dislike = function(obj, action) {
    var row = parent_by_tag(obj, 'tr');
    var resource_id = row.getAttribute("id");
    var type_id = parent_sibling_by_id(row, '#t_id').innerText;

    $.ajax({
            url: "/api/like_dislike/",
            dataType: "json",
            data: {
                resource_id: resource_id,
                type_id: type_id,
                action: action
            },
            success: function (data) {
                var like_delta = data['like'];
                var dislike_delta = data['dislike'];
                if (action==='like') {
                    $(obj).find("span")[0].innerText = (parseInt(obj.innerText, 10) + parseInt(like_delta, 10)).toString();
                    var obj_sibling = child_by_class(row, ".dislike");
                    $(obj_sibling).find("span")[0].innerText = (parseInt(obj_sibling.innerText, 10) + parseInt(dislike_delta, 10)).toString();
                } else if (action==='dislike') {
                    $(obj).find("span")[0].innerText = (parseInt(obj.innerText, 10) + parseInt(dislike_delta, 10)).toString();
                    var obj_sibling = child_by_class(row, ".like");
                    $(obj_sibling).find("span")[0].innerText = (parseInt(obj_sibling.innerText, 10) + parseInt(like_delta, 10)).toString();
                }

                if ($(obj).hasClass('pressed') && $(obj_sibling).hasClass('plain')) {
                    $(obj).toggleClass('pressed');
                    $(obj).toggleClass('plain');
                }
                else if ($(obj).hasClass('plain') && $(obj_sibling).hasClass('pressed')) {
                    $(obj).toggleClass('pressed');
                    $(obj).toggleClass('plain');
                    $(obj_sibling).toggleClass('pressed');
                    $(obj_sibling).toggleClass('plain');
                }
                else {
                    $(obj).toggleClass('pressed');
                    $(obj).toggleClass('plain');
                }
            },
            error: function (jqXHR) {
                var msg = '';
                if (jqXHR.status === 307) {
                    window.location.href = '/login/';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (jqXHR.responseText === 'condition') {
                    msg = 'Server like-dislike condition not specified.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                if (msg) {
                    alert('Error occurred | ' + msg);
                }
            }
        });
};


var like = function() {
    $('.like').click(function() {
        process_like_dislike(this, 'like');
    });
};


var dislike = function() {
    $('.dislike').click(function() {
        process_like_dislike(this, 'dislike');
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


var child_by_class = function(node, cls) {
    return $(node).find(cls)[0];
};


var parent_by_tag = function(node, tagname) {
    var parent;
	if (node === null || tagname === '') return;
	parent  = node.parentNode;
	tagname = tagname.toUpperCase();

	while (parent.tagName !== "HTML") {
		if (parent.tagName === tagname) {
			return parent;
		}
		parent = parent.parentNode;
	}
	return parent;
};


var filter_elements = function(table, checkbox) {
    var i = 0;
    if (checkbox.is(':checked')) {
        current_user = document.getElementById("current_user");
        for (i; i < table.rows.length; i++) {
            author_cell = child_by_class(table.rows[i], '.author');
            if (!author_cell) {continue;}
            if (author_cell.innerText !== current_user.value) {
                 table.rows[i].style.display = 'none';
            }
        }
    } else {
        for (i; i < table.rows.length; i++) {
            if (table.rows[i].style.display === 'none') {
                table.rows[i].style.display = '';
            }
        }
    }
};


function refresh() {
    var e=document.getElementById("refreshed");
    if (!e) {return}
    if(e.value=="no")e.value="yes";
    else{e.value="no";location.reload();}
}


var main = function() {
    like();
    dislike();
    refresh();
};

$(document).ready(main);