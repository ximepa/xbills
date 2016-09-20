var dashboard = {};
var global = {};
$( document ).ready(function() {
    //$('.menu-toggle-button').click(function(){
    //    $('.sidebar').sidebar('setting', {dimPage: false}).sidebar('toggle');
    //});
    //$('.sidebar').sidebar('setting', {dimPage: false}).sidebar({context: '.visible.example .bottom.segment'});
    $('.ui.dropdown').dropdown();
    $('.menu .item').tab();
    $('.sticky').sticky();
    $('.popup').popup();
    $('#sideBar').accordion({
        onOpen: function () {
            console.log($('#sideBar'))
        },
        onOpening:function (event, ui) {
            console.log(event)
            console.log(ui)
        }
    //    exclusive: false
    });
    $('#session').popup({
        popup : $('#browse'),
        on    : 'click',
        inline     : false,
        hoverable  : false,
        position   : 'bottom left',
        delay: {
            show: 300,
            hide: 800
        }
    });



    if (document.getElementById("services") != null) {
	document.getElementById("services").style.display = getCookie('services');
    }

    $('#table_group td').on('click', function () {
        var dimmer = $('body');
        dimmer.dimmer('show')
        $.ajax({
            url: "/admin/group/?user_list=" + $(this).parent()[0].childNodes[1].innerText,
            cache: false,
            success: function(html){
                $("#content1").html(html);
                dimmer.dimmer('hide');
            }
        });
    })
});

function servicesToggle() {
    $('#services').toggle();
    setCookie('services', $("#services").css('display'))
}

function setCookie(cname, value) {
    $.cookie(cname, value, { path:'/' } );

}

function getCompany(id) {
    $.getJSON('/admin/company/?company_id=' + id, function (data) {
        var table = document.getElementById("table_test");
            // var orderArrayHeader = ["Login","UID","Company","Credit"];
            // var tthead = document.createElement('thead');
            // table.appendChild(tthead);
            // for(var n=0;n<orderArrayHeader.length;n++){
            //     tthead.appendChild(document.createElement("th")).appendChild(document.createTextNode(orderArrayHeader[n]));
            // }
            // alert(table.tHead.rows.length);

        if (table.rows.length == 0) {
        } else {
            for(var i = table.rows.length; i > 0;i--) {
                table.deleteRow(i - 1);
            }
        }
        $.each(data, function (index, value) {
            var row = table.insertRow();
            row.insertCell(0).innerHTML = value.fields.login;
            row.insertCell(1).innerHTML = '<a href=/admin/clients/' + value.pk + '>' + value.pk +'</a>';
            row.insertCell(2).innerHTML = value.fields.company;
            row.insertCell(3).innerHTML = value.fields.credit;
        });
        $('#company_modal').modal('show')
    });
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
}


function formatBytes(bytes,decimals) {
   if(bytes == 0) return '0 Byte';
   var k = 1024; // or 1024 for binary
   var dm = decimals + 1 || 3;
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
   var i = Math.floor(Math.log(bytes) / Math.log(k));
   return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

var uid = "UID";
global.getPayNow = function () {
    $.getJSON('/admin/?pay_now', function (data) {
        if (uid && getCookie('pay_uid') != data.pay_now[3]) {
            $.each(data, function (index, value) {
                toastr.pay(value[0] + ' грн.  ' + value[1], value[2] + ' (UID: <a style="color: blue" href="clients/' + value[3] + '"' + '>' + value[3] + '</a>' + ')', value[4],
                    {progressBar: true, timeOut: 40000, extendedTimeOut: 10000})
            })
        }
        uid = data.pay_now[3];
	setCookie('pay_uid', data.pay_now[3])
    })
};

function comments_add (theLink, Message, CustomMsg) {
    console.log(Message);
  Q=prompt(Message);

  if (Q == '' || Q == null) {
  	var is_confirmed = alert('Enter comments');
  }
  else {
    Q=' &comments='+Q;
    theLink.href += Q;
      console.log(Q)
  }

  return is_confirmed;
}


// var claim = "claim";
// global.getClaimsNotifi = function () {
//    $.getJSON('/admin/claims/?claim_notifi', function (data) {
//        if (claim && getCookie('cuid') != data.claim[1]) {
//            $.each(data, function (index, value) {
//                toastr.claims(value[0], 'UID: <a style="color: white" href="clients/' + value[1] + '"' + '>' + value[1] + '</a>', value[2], value[3], value[4],
//                    {timeOut: 0, onclick: null, extendedTimeOut: 0})
//            })
//        }
//        claim = data.claim[1];
// 	setCookie('cuid', data.claim[1]);
//    })
//
// };
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
