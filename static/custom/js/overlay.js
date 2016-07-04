/**
 * Created by ximepa on 20.07.15.
 */
$(document).ready(function() {

    $(document).ajaxSend(function(event, request, settings) {
        $('#overlay').show();
    });

    $(document).ajaxComplete(function(event, request, settings) {
        $('#overlay').hide();
    });
});