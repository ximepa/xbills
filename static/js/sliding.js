$(document).ready(function() {
    (function($, window, document){
        var panelSelector = '[data-perform="panel-collapse"]';
        $(panelSelector).each(function() {
            var $this = $(this),
                    parent = $this.closest('.panel'),
                    wrapper = parent.find('.panel-wrapper'),
                    collapseOpts = {toggle: false};
            if( ! wrapper.length) {
                wrapper = parent.children('.panel-heading').nextAll().wrapAll('<div/>').parent().addClass('panel-wrapper');
                collapseOpts = {};
            }
            wrapper.collapse(collapseOpts).on('hide.bs.collapse', function() {
                //$this.children('i').removeClass('fa-minus').addClass('fa-plus');
            }).on('show.bs.collapse', function() {
                //$this.children('i').removeClass('fa-plus').addClass('fa-minus');
            });
        });
        $(document).on('click', panelSelector, function (e) {
            e.preventDefault();
            var parent = $(this).closest('.panel');
            var wrapper = parent.find('.panel-wrapper');
            wrapper.collapse('toggle');
        });
    }(jQuery, window, document));});
