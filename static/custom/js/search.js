showHouse = function(){
    var thisStreet = $('.search.street').dropdown('get value');
    var objSelf = this;
    $.ajax({
      type: "get",
      url: "/admin/search/?district",
      data: {
         method: "StreetID",
         StreetID: thisStreet
      },
      dataType: "json",
      success: function(objResponse){
         if (objResponse.success) {
            var artData = objResponse.results;
            var numArt = artData.length;
            $('.search.house .menu .item').remove();
            for(i=0;i < numArt;i++){
               var thisArtID = artData[i].value;
               var thisArtName = artData[i].name;
               $('.search.house .menu').append('<div class="item" data-value="' + thisArtID + '">' + thisArtName + '</div>');
         }
               $('.search.house').dropdown('set text',"Select art");
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

showStreet = function(){
    var thisDistrict = $('.search.district').dropdown('get value');
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
            if (objResponse.success) {
                var artData = objResponse.results;
                var numArt = artData.length;
                $('.search.street .menu .item').remove();
                for(i=0;i < numArt;i++){
                    var thisArtID = artData[i].value;
                    var thisArtName = artData[i].name;
                    $('.search.street .menu').append('<div class="item" data-value="' + thisArtID + '">' + thisArtName + '</div>');
                }
                $('.search.street').dropdown('set text',"Select art");
            } else {
                objSelf.ShowErrors(objResponse.ERRORS);
            }
        },
        error: function(objRequest, strError){
            console.error('qbjRequest: ' + objRequest);
            console.error('strError: ' + strError);
        }
    });
};

