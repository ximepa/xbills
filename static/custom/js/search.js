$( document ).ready(function() {
    $('#district').dropdown({
        apiSettings: {
            url: '/admin/search/?district'
        }
    });
    $('#street').dropdown(
        console.log($('#district').val()),
    {

        // apiSettings: {
        //     url: '/admin/search/?district'
        // }
    });
    $('#house').dropdown({
        apiSettings: {
            url: '/admin/search/?district'
        }
    });
});

