/**
 * Created by ximepa on 23.05.16.
 */
$(document).ready(function(){
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
    var body_class = $.cookie('body_class');
    if(body_class) {
    //    console.log('class');
        $('body').addClass(body_class);
    //        var currentHref = $(this).attr('href');
    //        if(currentHref == currentPage) {
    //            $(this).attr('class', body_class);
    //        }
    //    })
    }
    $('#hide-menu').on('click', function() {
        //$('body').toggleClass('hidden-menu');
        if ($('body').hasClass('hidden-menu')){
            $.cookie('body_class', '');
        } else {
            $.cookie('body_class', 'hidden-menu');
        }
    });
    $('.minifyme').on('click', function() {
        //$('body').toggleClass('hidden-menu');
        if ($('body').hasClass('minified')){
            $.cookie('body_class', '');
        } else {
            $.cookie('body_class', 'minified');
        }
    });
});