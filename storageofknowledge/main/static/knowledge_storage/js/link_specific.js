
var delete_link = function() {
    $('.delete_link').click(function() {
        result = confirm('Are you sure you want to delete this link?');
        if (!result) {return;}
        var link_row = parent_by_tag(this, 'tr');
        var l_id = link_row.getAttribute("id");
        var type_id = parent_sibling_by_id(link_row, '#t_id').innerText;

            $.ajax({
                url: "/api/delete_link/",
                dataType: "json",
                type: "POST",
                data: {
                    l_id: l_id,
                    type_id: type_id
                },
                success: function () {
                    table = parent_by_tag(link_row, 'table');
                    rowIndex = document.getElementById(l_id).rowIndex;
                    table.deleteRow(rowIndex);
                },
                error: function (jqXHR) {
                    var msg = '';
                    if (jqXHR.status === 307) {
                        window.location.href = '/login/';
                    } else if (jqXHR.status == 404) {
                        msg = 'Requested page not found. [404]';
                    } else if (jqXHR.status == 500) {
                        msg = 'Internal Server Error [500].';
                    } else if (jqXHR.status == 403) {
                        msg = 'User has not enough rights [403].';
                    } else {
                        msg = 'Uncaught Error.\n' + jqXHR.responseText;
                    }
                    if (msg) {
                        alert('Error occurred | ' + msg);
                    }
                }
            });
    });
};


var filter_user_links = function() {
    $('#users_only_links').click(function() {
        var checkbox = $(this);
        table = document.getElementsByTagName("table")[0];
        filter_elements(table, checkbox);
    });
};


var main = function() {
    filter_user_links();
    delete_link();
};



$(document).ready(main);