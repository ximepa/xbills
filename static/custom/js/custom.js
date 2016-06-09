var dashboard = {};

dashboard.getCpu = function () {
    $.getJSON('?cpu', function (data) {
        $.each(data, function(index, value) {
            var cores = index +1;
            if (value.core > 40 && value.core < 59) {
                $('#core' + cores).css('width', data[index].core + '%').attr('aria-valuenow', data[index].core).removeClass('progress-bar-danger').addClass('progress-bar-warning');
                $('#core' + cores).text(data[index].core + '%');
            }
            else if (value.core > 60) {
                $('#core' + cores).css('width', data[index].core + '%').attr('aria-valuenow', data[index].core).removeClass('progress-bar-warning').addClass('progress-bar-danger');
                $('#core' + cores).text(data[index].core + '%');
            }
            else {
                $('#core' + cores).css('width', data[index].core + '%').attr('aria-valuenow', data[index].core).removeClass('progress-bar-warning progress-bar-danger');
                $('#core' + cores).text(data[index].core + '%');
            }
        });
    });
};

dashboard.getPay = function () {
    $.getJSON('?pay', function (data) {
        $('#day_sum').text(data.pay_day[0].sum__sum);
        $('#day_sum_count').text(data.pay_day[1]);
        $('#week_sum').text(data.pay_week[0].sum__sum);
        $('#week_sum_count').text(data.pay_week[1]);
        $('#month_sum').text(data.pay_month[0].sum__sum);
        $('#month_sum_count').text(data.pay_month[1]);
    })
};

dashboard.getMemory = function () {
    $.getJSON('?memory', function (data) {
        $('#getMemory').css('width', data.memory + '%').attr('aria-valuenow', data.memory).removeClass('progress-bar-danger').addClass('progress-bar-warning');
        $('#getMemory').text(data.memory + '%');
    })
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
        dashboard.getMemory();
        dashboard.getPay();
        refresh();
    }, 10000);
}

$(document).ready(function(){
    dashboard.getProc();
    dashboard.getCpu();
    dashboard.getUptime();
    dashboard.getMemory();
    dashboard.getPay();
    refresh();
});
