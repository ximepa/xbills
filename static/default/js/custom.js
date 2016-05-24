/**
 * Created by ximepa on 23.05.16.
 */
$(document).ready(function(){
    //console.log(location.pathname);
    //$(function() {
    //  $('nav a[href^="/' + location.pathname + '"]').addClass('linked');
    //});
    $(function(){
        var current = location.pathname;
        $('.navbar a').each(function(){
            var $this = $(this);
            // if the current path is like this link, make it active
            if($this.attr('href') == current){
                $this.addClass('linked');
            }
        });
        if ($('.dropdown-menu a').hasClass('linked')){
            $('#client-menu').addClass('linked');
        }
    });
    //var body_class = $.cookie('linked');
    //if(body_class) {
    //    console.log('class');
    //    var currentPage = location.pathname;
    //    $('a-nav').each(function() {
    //        var currentHref = $(this).attr('href');
    //        if(currentHref == currentPage) {
    //            $(this).attr('class', body_class);
    //        }
    //    })
    //} else {
    //    console.log('no class');
    //}
    //$('.a-nav').on('click', function() {
    //    $(this).toggleClass('linked');
    //    $.cookie('linked', $('body').attr('class'));
    //});
});