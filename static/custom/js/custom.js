/**
 * Created by ximepa on 23.05.16.
 */


var dashboard = {};
//
// dashboard.getProc = function () {
//
//         $("#get_proc").dataTable({
//         ajax: "?process"
//         })
//
// };

dashboard.getProc = function () {
    $(function() {
        $('#get_proc').bootstrapTable({
            url: '?process',
            search: true,
            pageSize: 10,
            columns: [{
                field: 'pid',
                title: 'Pid',
            }, {
                field: 'name',
                title: 'Name'
            }, {
                field: 'cpu',
                title: '% CPU',
                valign: 'bottom'
            }
            ]
        });
    })
};

$(document).ready(function(){
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

    // $(function() {
		// var columnObj = jQuery('.sortable');
    //
		// if (columnObj.length > 0) {
		// 	columnObj
		// 		.sortable({
		// 			connectWith: '.panel-heading',
		// 			forcePlaceholderSize: true,
		// 			placeholder: 'panel-heading',
		// 			opacity: '0.5 '
    //
		// 		});
		// }
    //
    // });
    //
    //
    // function restoreSorted(){
    //
    //
    // }



});