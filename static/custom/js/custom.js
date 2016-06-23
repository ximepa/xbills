var dashboard = {};
var global = {};


function formatBytes(bytes,decimals) {
   if(bytes == 0) return '0 Byte';
   var k = 1024; // or 1024 for binary
   var dm = decimals + 1 || 3;
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
   var i = Math.floor(Math.log(bytes) / Math.log(k));
   return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

dashboard.getCpu = function () {
    $.getJSON('?cpu', function (data) {
        $.each(data, function(index, value) {
            var cores = index +1;
            if (value.core > 40 && value.core < 60) {
                $('#core' + cores).css('width', data[index].core + '%').attr('aria-valuenow', data[index].core).removeClass('progress-bar-danger').addClass('progress-bar-warning');
                $('#core' + cores).text(data[index].core + '%');
            }
            else if (value.core > 65) {
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

var uid = "UID";

global.getPayNow = function () {
    $.getJSON('/admin/?pay_now', function (data) {
        if (uid != data.pay_now[2]) {
            $.each(data, function (index, value) {
                toastr.pay(value[0] + ' грн.  ' + value[1], value[2] + ' (UID: <a style="color: white" href="clients/' + value[3] + '"' + '>' + value[3] + '</a>' + ')', value[4],
                    {progressBar: true, timeOut: 40000, extendedTimeOut: 10000})
            })
        }
        uid = data.pay_now[2];
    })
};

var claim = "claim";

global.getClaimsNotifi = function () {
    $.getJSON('/admin/claims/?claim_notifi', function (data) {
        if (claim != data.claim[0]) {
            $.each(data, function (index, value) {
                toastr.claims(value[0], 'UID: <a style="color: white" href="clients/' + value[1] + '"' + '>' + value[1] + '</a>', value[2], value[3], value[4],
                    {timeOut: 0, onclick: null, extendedTimeOut: 0})
            })
        }
        claim = data.claim[0];
    })
    

};

dashboard.getMemory = function () {
    $.getJSON('?memory', function (data) {
        $('#uptime').text(data.uptime);
        $('#getMemory').css('width', data.memory + '%').attr('aria-valuenow', data.memory).removeClass('progress-bar-danger').addClass('progress-bar-warning');
        $('#getMemory').text(data.memory + '%');
        $('#getSwap').css('width', data.swap + '%').attr('aria-valuenow', data.swap).removeClass('progress-bar-danger').addClass('progress-bar-warning');
        $('#getSwap').text(data.swap + '%');
        $('#getMemoryTotal').text(formatBytes(data.total));
        $('#getMemoryUsed').text(formatBytes(data.used));
        $('#getMemoryFree').text(formatBytes(data.free));
        $('#getMemoryCached').text(formatBytes(data.cached));
        $('#getSwapTotal').text(formatBytes(data.stotal));
        $('#getSwapUsed').text(formatBytes(data.sused));
        $('#getSwapFree').text(formatBytes(data.sfree));
    })
};

// dashboard.getProc = function() {
//       function rowStyle(row, index) {
//           if (row.cpu > 35 && row.cpu < 50) {
//               return {
//                   classes: 'warning'
//               }
//           }
//           if (row.cpu > 50 && row.cpu < 200) {
//               return {
//                   classes: 'danger'
//               }
//           }
//           return {};
//       }
//
//     $(function() {
//         $('#get_proc').bootstrapTable({
//             url: '?process',
//             height: 300,
//             rowStyle: rowStyle,
//             sortName: 'cpu',
//             sortOrder: 'desc',
//             columns: [{
//                 field: 'pid',
//                 title: 'Pid'
//             }, {
//                 field: 'name',
//                 title: 'Name'
//             }, {
//                 field: 'status',
//                 title: 'Status'
//             }, {
//                 field: 'cpu',
//                 title: '% CPU',
//                 valign: 'top',
//                 sortable: true
//             }
//             ]
//         });
//     })
// };

// function refresh() {
//     setTimeout(function(){
//         $('#get_proc').bootstrapTable('destroy');
//         dashboard.getCpu();
//         // dashboard.getProc();
//         dashboard.getMemory();
//         dashboard.getPay();
//         dashboard.getPayNow();
//         dashboard.getClaimsNotifi();
//         refresh();
//     }, 10000);
// }
//
// $(document).ready(function(){
//     dashboard.getCpu();
//     // dashboard.getProc();
//     dashboard.getMemory();
//     dashboard.getPay();
//     dashboard.getPayNow();
//     dashboard.getClaimsNotifi();
//     refresh();
// });
