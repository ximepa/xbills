var dashboard = {};

dashboard.getCpu = function () {
    $.getJSON('?cpu', function (data) {
        $.each(data, function(index, value) {
            var cores = index +1;
            if (value.core > 40 && value.core < 59) {
                $('#core' + cores).css('width', data[index].core + '%').attr('aria-valuenow', data[index].core).removeClass('progress-bar-danger').addClass('progress-bar-warning');
            }
            else if (value.core > 60) {
                $('#core' + cores).css('width', data[index].core + '%').attr('aria-valuenow', data[index].core).removeClass('progress-bar-warning').addClass('progress-bar-danger');
            }
            else {
                $('#core' + cores).css('width', data[index].core + '%').attr('aria-valuenow', data[index].core).removeClass('progress-bar-warning progress-bar-danger');
            }
        });
    });
};
dashboard.getUptime = function () {
    $.getJSON('?uptime', function (data) {
        $('#uptime').text(data.uptime);
    });
};

dashboard.getProc = function() {
      function rowStyle(row, index) {
          if (row.cpu > 35 && row.cpu < 50) {
              return {
                  classes: 'warning'
              }
          }
          if (row.cpu > 50 && row.cpu < 200) {
              return {
                  classes: 'danger'
              }
          }
          return {};
      }

    $(function() {
        $('#get_proc').bootstrapTable({
            url: '?process',
            height: 300,
            rowStyle: rowStyle,
            sortName: 'cpu',
            sortOrder: 'desc',
            columns: [{
                field: 'pid',
                title: 'Pid'
            }, {
                field: 'name',
                title: 'Name'
            }, {
                field: 'status',
                title: 'Status'
            }, {
                field: 'cpu',
                title: '% CPU',
                valign: 'top',
                sortable: true
            }
            ]
        });
    })
};

function refresh() {
    setTimeout(function(){
        $('#get_proc').bootstrapTable('destroy');
        dashboard.getCpu();
        dashboard.getProc();
        dashboard.getUptime();
        refresh();
    }, 10000);
}

$(document).ready(function(){
    dashboard.getProc();
    dashboard.getCpu();
    dashboard.getUptime();
    refresh();
});
