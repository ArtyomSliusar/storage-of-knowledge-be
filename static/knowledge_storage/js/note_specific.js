
var skip_confirm = function() {
    window.onbeforeunload = null;
};


//Find the button set null value to click event and alert will not appear for that specific button
var save_btn = document.getElementById('save_button');
$(save_btn).click(skip_confirm);
window.CKEDITOR.on('instanceReady', function(){
    var save_wysiwyg = document.getElementsByClassName('cke_button__save')[0];
    $(save_wysiwyg).click(skip_confirm);
});


window.onbeforeunload = function() {
    return 'All unsaved changes will be lost!';
};






