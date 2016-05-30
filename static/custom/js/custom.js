/**
 * Created by ximepa on 23.05.16.
 */
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
    $(function() {

        //add id's to the li elements so after sorting we can save the order in localstorage
        $( "#draggablePanelList>li" ).each(function(index, domEle){ $(domEle).attr('id', 'item_'+index)});

        $( "#draggablePanelList" ).sortable({
          placeholder: "ui-state-highlight",
          update: function(event, ui) {
            localStorage.setItem("sorted",  $("#draggablePanelList").sortable("toArray") );
          }
        });

        restoreSorted();

      });


      function restoreSorted(){

          var sorted = localStorage["sorted"];
          if(sorted == undefined) return;

          var elements = $("#draggablePanelList");
          var sortedArr = sorted.split(",");

          for (var i = 0; i < sortedArr.length; i++){
              var el = elements.find("#" + sortedArr[i]);
              $("#draggablePanelList").append(el);
          };

      }
});