//     $('#district').dropdown('setting',{
//          onChange : showArt()
//          });
//     $('#street').dropdown(
//         // console.log($('#district').val()),
//
//     {
//
//         apiSettings: {
//             url: '/admin/search/?district'
//         }
//     });
//     // $('#street').api()
//     $('#house').dropdown({
//         apiSettings: {
//             url: '/admin/search/?district'
//         }
//     });
//
//

showHouse = function(){
    console.log('street')
   //  var thisStreet = $('#street').dropdown('get value');
   //  console.log('street')
   //
   // var objSelf = this;
   // $.ajax({
   //    type: "get",
   //    url: "/admin/search/?district",
   //    data: {
   //       method: "StreetD",
   //       StreetD: thisStreet
   //    },
   //    dataType: "json",
   //    success: function(objResponse){
   //        console.log(objResponse)
   //       if (objResponse.success) {
   //          var artData = objResponse.results;
   //          var numArt = artData.length;
   //          $('#houseMenu .item').remove();
   //          for(i=0;i < numArt;i++){
   //             var thisArtID = artData[i].value;
   //             var thisArtName = artData[i].name;
   //             //console.warn(thisArtist + ' - ' + thisArtName);
   //             $('#streetMenu').append('<div class="item" data-value="' + thisArtID + '">' + thisArtName + '</div>');
   //
   //          }
   //             $('#house').dropdown();
   //             $('#house').dropdown('set text',"Select art");
   //       }
   //       else {
   //           console.log(objSelf)
   //           objSelf.ShowErrors(objResponse.ERRORS);
   //       }
   //    },
   //    error: function(objRequest, strError){
   //       console.error('qbjRequest: ' + objRequest);
   //       console.error('strError: ' + strError);
   //    }
   // });

};

showStreet = function(){
    var thisDistrict = $('#district').dropdown('get value');

   var objSelf = this;
   $.ajax({
      type: "get",
      url: "/admin/search/?district",
      data: {
         method: "DistrictID",
         DistrictID: thisDistrict
      },
      dataType: "json",
      success: function(objResponse){
          console.log(objResponse)
         if (objResponse.success) {
            var artData = objResponse.results;
            var numArt = artData.length;
            $('#streetMenu .item').remove();
            for(i=0;i < numArt;i++){
               var thisArtID = artData[i].value;
               var thisArtName = artData[i].name;
               //console.warn(thisArtist + ' - ' + thisArtName);
               $('#streetMenu').append('<div class="item" data-value="' + thisArtID + '">' + thisArtName + '</div>');

            }
               $('#street').dropdown();
               $('#street').dropdown('set text',"Select art");
         }
         else {
             console.log(objSelf)
             objSelf.ShowErrors(objResponse.ERRORS);
         }
      },
      error: function(objRequest, strError){
         console.error('qbjRequest: ' + objRequest);
         console.error('strError: ' + strError);
      }
   });

};

